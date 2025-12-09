import streamlit as st
import requests, pandas as pd
from io import BytesIO

def run_caption_scraper():
    st.subheader("Reddit Caption Scraper")
    s1 = st.text_input("Subreddit 1")
    s2 = st.text_input("Subreddit 2")
    subs=[x for x in [s1,s2] if x.strip()!='']
    tf=st.selectbox("Time Filter",["day","week","month","all"])
    pl=st.number_input("Post Limit",1,200,50)
    fmt=st.selectbox("Output Format",["Excel","Notepad"])
    if st.button("Start"):
        if not subs:
            st.error("Enter subreddits.")
            return
        rows=[]
        total=len(subs)*pl
        c=0
        prog=st.progress(0)
        for sb in subs:
            url=f"https://www.reddit.com/r/{sb}/top.json?t={tf}&limit={pl}"
            r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
            posts=r.json().get("data",{}).get("children",[])
            for p in posts:
                d=p['data']
                rows.append([sb,d.get("title",""),d.get("selftext","")])
                c+=1
                prog.progress(int((c/total)*100))
        if fmt=="Excel":
            df=pd.DataFrame(rows,columns=["Subreddit","Title","Caption"])
            bio=BytesIO()
            df.to_excel(bio,index=False)
            st.download_button("Download Excel",bio.getvalue(),"captions.xlsx")
        else:
            t=""
            for r in rows:
                t+=r[1]+"\n"+r[2]+"\n"+"-"*40+"\n"
            st.download_button("Download TXT",t,"captions.txt")
