import streamlit as st
import requests, pandas as pd
from io import BytesIO

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/json",
}

def run_caption_scraper():
    st.subheader("Reddit Caption Scraper")

    s1 = st.text_input("Subreddit 1", key="sub1")
    s2 = st.text_input("Subreddit 2", key="sub2")
    subs=[x for x in [s1,s2] if x.strip()!='']

    tf = st.selectbox("Time Filter", ["day","week","month","all"], key="tf_caption")
    pl = st.number_input("Post Limit", 1, 200, 50, key="pl_caption")
    fmt = st.selectbox("Output Format", ["Excel","Notepad"], key="fmt_caption")

    if st.button("Start Scraping", key="start_caption"):
        if not subs:
            st.error("Enter subreddits first.")
            return

        rows=[]
        total=len(subs)*pl
        c=0
        prog=st.progress(0)

        for sb in subs:
            url=f"https://www.reddit.com/r/{sb}/top.json?t={tf}&limit={pl}"

            try:
                r = requests.get(url, headers=HEADERS, timeout=10)

                # Validate HTTP response
                if r.status_code != 200:
                    st.error(f"Cannot access r/{sb} (status {r.status_code})")
                    continue

                # Prevent JSONDecodeError
                try:
                    data = r.json()
                except Exception:
                    st.error(f"Reddit returned non-JSON response for r/{sb}. Possibly rate-limited.")
                    continue

                posts = data.get("data", {}).get("children", [])

                if not posts:
                    st.warning(f"No posts found for r/{sb}")
                    continue

                for p in posts:
                    d = p["data"]
                    rows.append([sb, d.get("title",""), d.get("selftext","")])
                    c += 1
                    prog.progress(int((c/total)*100))

            except Exception as e:
                st.error(f"Error scraping r/{sb}: {e}")
                continue

        if not rows:
            st.error("No data scraped.")
            return

        # Output download
        if fmt=="Excel":
            df = pd.DataFrame(rows, columns=["Subreddit","Title","Caption"])
            bio = BytesIO()
            df.to_excel(bio, index=False)
            st.download_button("Download Excel", bio.getvalue(), "captions.xlsx", key="dl_cap_excel")

        else:
            text=""
            for row in rows:
                text += f"{row[1]}\n{row[2]}\n{'-'*40}\n"
            st.download_button("Download TXT", text, "captions.txt", key="dl_cap_txt")
