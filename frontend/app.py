import streamlit as st
import requests
from PIL import Image
import io
import json

st.set_page_config(
    page_title="BrandGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.upload-box {
    border: 2px dashed #cccccc;
    border-radius: 5px;
    padding: 25px;
    text-align: center;
    margin: 10px 0;
    transition: all 0.3s;
}
.upload-box:hover {
    border-color: #666666;
}
.score-card {
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.score-4 { background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); color: white; }
.score-3 { background: linear-gradient(135deg, #8BC34A 0%, #689F38 100%); color: white; }
.score-2 { background: linear-gradient(135deg, #FFC107 0%, #FFA000 100%); color: black; }
.score-1 { background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); color: white; }
.score-0 { background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%); color: white; }
.checklist-item {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# connect to backend
BACKEND_URL = "http://backend:8000"  # Change where you are hosting


def upload_to_backend(file_bytes, endpoint):
    try:
        response = requests.post(
            f"{BACKEND_URL}/{endpoint}",
            files={"file": file_bytes}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection failed: {str(e)}")
        return None

def render_file_upload(label, file_types):
    uploaded_file = st.file_uploader(
        label=label,
        type=file_types,
        accept_multiple_files=False,
        key=f"upload_{label}"
    )
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")
        return uploaded_file
    return None

def display_scorecard(score, details):
    score_mapping = {
        4: ("Perfect Compliance", "Your asset meets all brand guidelines"),
        3: ("Good", "Minor adjustments needed"),
        2: ("Needs Work", "Several issues to address"),
        1: ("Poor", "Significant rework required"),
        0: ("Failed", "Doesn't meet basic requirements")
    }
    
    with st.container():
        st.markdown(f"""
        <div class="score-card score-{score}">
            <h2>{score}/4</h2>
            <h3>{score_mapping[score][0]}</h3>
            <p>{score_mapping[score][1]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Detailed Analysis", expanded=True):
            for category, data in details.items():
                st.markdown(f"**{category.replace('_', ' ').title()}**")
                st.progress(data["score"], 
                            text=f"{'✅' if data['score'] else '❌'} {data['explanation']}")


def main():
    st.title("🛡️ BrandGuard AI")
    st.markdown("Upload your brand guidelines and marketing assets to check compliance")
    st.divider()
    
    # Upload 
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Step 1: Brand Guidelines")
            brand_kit = render_file_upload("Brand Kit (PDF)", ["pdf"])
        
        with col2:
            st.subheader("Step 2: Marketing Asset")
            image = render_file_upload("Creative Asset", ["jpg", "png", "jpeg"])
    
    # Analysis 
    if st.button("🔍 Analyze Compliance", type="primary", use_container_width=True):
        if brand_kit and image:
            with st.spinner("Analyzing with AI..."):
                brand_data = upload_to_backend(brand_kit.getvalue(), "upload/brand-kit")
                result = requests.post(
                    f"{BACKEND_URL}/check-compliance",
                    files={
                        "brand_kit": brand_kit.getvalue(),
                        "image": image.getvalue()
                    }
                ).json()
            
            # Results
            st.divider()
            st.subheader("📋 Compliance Report")
            
            # Side-by-Side Preview
            col_a, col_b = st.columns(2)
            with col_a:
                img = Image.open(io.BytesIO(image.getvalue()))
                st.image(img, caption="Uploaded Asset", use_container_width=True)
            
            with col_b:
                with st.expander("📜 Extracted Brand Rules", expanded=True):
                    rules = brand_data["brand compliance data"]

                    # fonts in the brand kit
                    fonts = rules.get("fonts", [])
                    if fonts:
                        st.markdown("**Font Styles:**")
                        for font in fonts:
                            st.markdown(f"<p style='font-family:\"{font}\"; font-size:18px; margin:0;'>{font}</p>",
                                unsafe_allow_html=True)
                    else:
                        st.info("No fonts found in brand kit.")

                    # primary colors of logo
                    primary_colors = rules.get("primary_colors", [])
                    if primary_colors:
                        st.markdown("**Primary Brand Colors:**")
                        for color in primary_colors:
                            st.markdown(f"""
                            <div style='display:flex; align-items:center; margin-bottom:10px;'>
                                <div style='width:30px; height:30px; background-color:{color}; border-radius:4px; margin-right:10px;'></div>
                                <code>{color}</code>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No primary colors found.")

                    # safe zone
                    safe_zone = rules.get("safe_zone")
                    if safe_zone:
                        st.markdown("**Safe Zone:**")
                        st.success(f"Logo safe zone: {safe_zone}")
                    else:
                        st.info("No safe zone data found.")

            # scorecard
            if result["status"] == "success":
                report = result["report"]
                display_scorecard(report["score"], report["details"])
            else:
                st.error("Analysis failed. Please try again.")
        else:
            st.warning("Please upload both files to proceed")

if __name__ == "__main__":
    main()
