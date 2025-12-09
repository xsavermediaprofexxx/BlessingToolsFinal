import streamlit as st
from PIL import Image
from io import BytesIO
import zipfile, random, string

def random_string(n=12):
    return ''.join(random.choices(string.ascii_letters+string.digits,k=n))

def run_image_spoofer():
    st.subheader("Image Spoofer")

    files = st.file_uploader("Upload Images", 
                             type=["jpg","jpeg","png","webp"], 
                             accept_multiple_files=True, 
                             key="files_spf")

    v = st.number_input("Variants", 1, 20, 5, key="variants_spf")

    if st.button("Start Spoofing", key="start_spoofer"):
        if not files:
            st.error("Upload images.")
            return
        
        zb=BytesIO()
        z=zipfile.ZipFile(zb,'w')
        total=len(files)*v
        c=0
        prog=st.progress(0)
        
        for f in files:
            img=Image.open(f).convert("RGB")
            for _ in range(v):
                out=BytesIO()
                new=img.rotate(random.uniform(-1,1))
                new.save(out,"JPEG")
                z.writestr(random_string()+".jpg", out.getvalue())
                c+=1
                prog.progress(int((c/total)*100))

        z.close()
        st.download_button("Download Spoofed ZIP", zb.getvalue(), "spoofed.zip", key="dl_spoof_zip")
