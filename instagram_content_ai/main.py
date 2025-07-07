import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
import html

# Load .env and get your original API_KEY
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    st.error("❌ API key not found. Please set API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit page settings
st.set_page_config(page_title="Instagram AI Content Generator", page_icon="📸")
st.title("📸 Instagram Content AI Generator")

# --- Image Upload ---
uploaded_image = st.file_uploader("Optional: Upload an image to inspire the content", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(uploaded_image, use_container_width=True)

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()
else:
    image_bytes = None

# --- Prompt Input ---
prompt = st.text_area("Enter your idea or topic:", height=150)

# --- Generate Content ---
if st.button("Generate Content"):
    if prompt.strip() == "":
        st.warning("Please enter something in the text box.")
    else:
        with st.spinner("Generating caption and hashtags..."):
            caption_prompt = f"Write a creative, engaging Instagram caption for: {prompt}"
            caption_response = model.generate_content(caption_prompt)
            caption = caption_response.text.strip()

            hashtags_prompt = f"Generate 10 trendy and relevant Instagram hashtags for: {prompt}"
            hashtags_response = model.generate_content(hashtags_prompt)
            hashtags = hashtags_response.text.strip()

        st.success("✅ Here's your AI-generated Instagram content:")
        st.markdown("**📸 Caption:**")
        st.text_area("Generated Caption", caption, height=100, key="caption_area")

        # Escape caption safely
        safe_caption = html.escape(caption).replace('\n', '&#10;')

        st.components.v1.html(f"""
            <textarea id="captionText" style="display:none;">{safe_caption}</textarea>
            <button onclick="
                const caption = document.getElementById('captionText').value;
                navigator.clipboard.writeText(caption)
                    .then(() => alert('✅ Caption copied!'))
                    .catch(err => alert('❌ Failed to copy caption'));
            " 
            style="padding:8px 16px; background-color:#4CAF50; color:white; border:none; border-radius:5px; margin-top:5px;">
                📋 Copy Caption
            </button>
        """, height=60)

        st.subheader("🔥 Hashtags:")
        st.text_area("Generated Hashtags", hashtags, height=100, key="hashtags_area")

        # Escape hashtags safely
        safe_hashtags = html.escape(hashtags).replace('\n', '&#10;')

        st.components.v1.html(f"""
            <textarea id="hashtagText" style="display:none;">{safe_hashtags}</textarea>
            <button onclick="
                const text = document.getElementById('hashtagText').value;
                navigator.clipboard.writeText(text)
                    .then(() => alert('✅ Hashtags copied!'))
                    .catch(err => alert('❌ Failed to copy hashtags'));
            " 
            style="padding:8px 16px; background-color:#2196F3; color:white; border:none; border-radius:5px; margin-top:5px;">
                📋 Copy Hashtags
            </button>
        """, height=60)
