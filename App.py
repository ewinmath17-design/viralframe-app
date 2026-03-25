import streamlit as st
from PIL import Image
import io
import time
from utils.image_processor import remove_background, create_story_canvas
from utils.video_maker import create_ken_burns_video

# --- UI CONFIGURATION ---
st.set_page_config(layout="wide", page_title="ViralFrame", page_icon="🚀")

st.title("🚀 ViralFrame: AI Story & Ads Generator")
st.markdown("Ubah foto mentah produk menjadi aset visual Meta Ads/Reels (9:16) yang estetik dalam sekali klik.")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Pengaturan Kampanye")
    
    uploaded_product = st.file_uploader("1. Upload Foto Produk Mentah (JPG/PNG)", type=["jpg", "jpeg", "png"])
    uploaded_logo = st.file_uploader("2. Upload Logo Brand (Opsional)", type=["png", "jpg"])
    
    bg_style = st.selectbox(
        "3. Pilih Nuansa Latar Belakang",
        ["Minimalist White", "Premium Dark", "Vibrant Gradient"]
    )
    
    output_mode = st.radio("4. Format Output", ["Image (PNG)", "Video (MP4 - Efek Zoom)"])
    
    generate_btn = st.button("✨ Generate Aset Visual", type="primary", use_container_width=True)

# --- MAIN AREA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Original Photo")
    if uploaded_product:
        st.image(uploaded_product, use_column_width=True)
    else:
        st.info("Silakan upload foto produk di sidebar.")

with col2:
    st.subheader("🔥 AI Generated Result")
    
    if generate_btn:
        if not uploaded_product:
            st.error("Upload foto produk terlebih dahulu sebelum menekan Generate!")
        else:
            with st.spinner("Mengekstraksi produk dan merakit kanvas..."):
                try:
                    # Proses Gambar
                    product_bytes = uploaded_product.getvalue()
                    product_extracted = remove_background(product_bytes)
                    
                    logo_img = None
                    if uploaded_logo:
                        logo_img = Image.open(uploaded_logo)
                    
                    final_canvas = create_story_canvas(product_extracted, bg_style, logo_img)
                    
                    # Output berdasarkan mode
                    if output_mode == "Image (PNG)":
                        st.image(final_canvas, use_column_width=True)
                        
                        # Tombol Download Gambar
                        buf = io.BytesIO()
                        final_canvas.save(buf, format="PNG")
                        st.download_button(
                            label="📥 Download High-Res Image",
                            data=buf.getvalue(),
                            file_name="viralframe_story.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    elif output_mode == "Video (MP4 - Efek Zoom)":
                        with st.spinner("Merender efek sinematik... (Ini memakan waktu beberapa detik)"):
                            video_path = create_ken_burns_video(final_canvas, duration=3)
                            
                            # Menampilkan video di Streamlit
                            video_file = open(video_path, 'rb')
                            video_bytes = video_file.read()
                            st.video(video_bytes)
                            
                            # Tombol Download Video
                            st.download_button(
                                label="📥 Download Meta Ads Video",
                                data=video_bytes,
                                file_name="viralframe_ads.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")

# --- AI HOOK GENERATOR (Mockup/Placeholder) ---
st.markdown("---")
st.subheader("✍️ AI Ads Copywriter")
col_hook1, col_hook2 = st.columns([3, 1])

with col_hook1:
    product_usp = st.text_input("Apa keunggulan utama produk ini? (Misal: Cokelat mete asli tanpa pengawet)")
with col_hook2:
    st.write("") # Spacer
    st.write("") # Spacer
    hook_btn = st.button("Generate Hook")

if hook_btn and product_usp:
    # Ini adalah Mockup. Di versi rilis, Anda bisa mengganti ini dengan call ke API LLM (Gemini/OpenAI)
    st.success(f"""
    **Opsi 1 (FOMO/Urgency):** "Stop scrolling! Stok {product_usp} makin menipis. Klik link untuk amankan diskon 50% hari ini!"
    
    **Opsi 2 (Problem-Solution):** "Sering ngemil tapi takut bahan kimia? Cobain sensasi {product_usp}. Beli 2 Gratis 1 sekarang!"
    """)
