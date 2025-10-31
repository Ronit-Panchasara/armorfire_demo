import re
from PIL import Image
import requests
import base64
import streamlit as st
import time
import os
import pathlib
import itertools

st.set_page_config(page_title="Approval Armorfire", layout="wide", page_icon="https://www.armorfire.in/public/frontend/webp/fav-2.webp")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_base64_of_bin_file(image_path):
    # Add a check to confirm the file exists
    if not os.path.exists(image_path):
        st.error(f"Error: File not found at {image_path}")
        # Optionally, raise the error or return a default value
        raise FileNotFoundError(f"File not found: {image_path}") 
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')

# Dynamically determine the current script's directory
# This gets the absolute path to the directory containing the current script
code_dir = pathlib.Path(__file__).parent.resolve()

# Construct the image path relative to the script's directory
# Replace "your_image_folder/your_image.png" with your actual path and file name
# For example, if your image is in a folder named 'images'
img_path = code_dir / "img" / "hero-bg.jpg" 

# Make sure the path is a string for the open() function
img_path_str = str(img_path)

# Call the function
try:
    img_base64 = get_base64_of_bin_file(img_path_str) # Use the absolute path string
    # Rest of your app logic using img_base64
except FileNotFoundError as e:
    st.error(e)

# Original lines from traceback for context
# File "/mount/src/armorfire_demo/index.py", line 29, in <module>
# img_base64 = get_base64_of_bin_file(img_path)
# File "/mount/src/armorfire_demo/index.py", line 23, in get_base64_of_bin_file
# with open(image_path, "rb") as f:
# --- Active page ---
active_page = "Approvals"

# --- CSS ---
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

    /* --- Background image fixed --- */
    html, body, .stApp {{
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
    /* --- Menu styles --- */
    .menu {{
        display: flex;
        gap: 2rem;
        flex-wrap: nowrap;
        font-family: 'Space Grotesk', sans-serif;
    }}

    .menu a {{
        text-decoration: none;
        font-size: 18px;
        font-weight: normal;
        color: black;
        transition: 0.3s;
    }}

    .menu a.active {{
        color: #0D6C68; 
        font-weight: 700;
    }}

    .menu a:hover {{
        color: #0D6C68;
    }}

    /* --- Main title --- */
    .my-title {{
        font-size: 3rem !important;        /* same size as your previous h1 */
        margin: 50px 0 0 0 !important;     /* top margin only, no bottom margin */
        padding: 0 !important;
        font-weight: 300 !important;
        text-align: center !important;
        font-family: 'Space Grotesk', sans-serif !important; 
    }}

    .my-title span {{
        color:#0D6C68 !important;
        font-weight: 300 !important;
    }}

    /* --- Box under title --- */
    .box {{
        font-size:20px !important;
        margin: 0 auto !important;          /* remove top margin */
        width: 500px !important;
        height: 60px !important;
        padding: 16px 48px !important;
        border: 4px solid white !important;
        font-weight: 400 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        text-align: center !important;
        display: flex !important;                
        justify-content: center !important;      
        align-items: center !important;   
    }}
    </style>
    """,
    unsafe_allow_html=True
)

pages = {
    "Home": "/index",
    "About": "/about_application",  # 👈 Redirects to about_application.py
    "Products & Solutions": "/products",
    "Blog": "/blog",
    "Certifications": "/certification",
    "Approvals": "/approval",
    "Testing Facility": "/testing"
}

menu_html = '<div style="display:flex; justify-content:space-between; align-items:center; width:100%;">'

# Logo
menu_html += """
    <a href='/' target='_self'>
        <img src='https://www.armorfire.in/public/frontend/assets/images/armorfire-blacklogo.png'
             style='width:160px; height:88px; transition:0.3s;'>
    </a>
"""

# Menu items
menu_html += '<div class="menu">'
for page, link in pages.items():
    active_class = "active" if page == active_page else ""
    menu_html += f'<a href="{link}" class="{active_class}" target="_self">{page}</a>'
menu_html += '</div></div>'

st.markdown(menu_html, unsafe_allow_html=True)

# --- White horizontal line below header ---
st.markdown(
    """
    <hr style="
        border: none;         
        height: 2px;          
        background-color: white; 
        width: 100%;           
        margin-left: 0;       
        margin-right: 0;      
    ">
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown(
        """
            <p class="my-title">
                Our <span>Approvals</span>
            </p>
            <div class="box">
                Formerly Mahadev Casting
            </div>
            """,
            unsafe_allow_html=True
        )
    
# --- White horizontal line below header ---
st.markdown(
    """
    <hr style="
        border: none;         
        height: 2px;          
        background-color: white; 
        width: 100%;           
        margin-left: 0;       
        margin-right: 0;      
    ">
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown(
        """
        <style>
        .cert-section {
            padding: 70px 7%;
            font-family: 'Space Grotesk', sans-serif;
            text-align: center;
        }

        .cert-title {
            color: #0D6C68 !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 40px !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }

        /* Make it a fixed 3x3 grid */
        .cert-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 60px;
            justify-items: center;
            align-items: stretch;
        }

        .cert-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: rgba(255,255,255,0.9);
            padding: 35px 25px;
            border-radius: 18px;
            height: 320px; /* Larger container height */
            width: 100%;
            max-width: 320px;
            box-shadow: 0px 6px 15px rgba(0,0,0,0.12);
            transition: all 0.3s ease-in-out;
        }

        .cert-item:hover {
            transform: translateY(-10px);
            box-shadow: 0px 10px 25px rgba(13,108,104,0.3);
        }

        .cert-item img {
            height: 150px;
            width: auto;
            margin-bottom: 20px;
            transition: transform 0.3s ease-in-out, filter 0.3s ease-in-out;
        }

        .cert-item:hover img {
            transform: scale(1.08);
            filter: brightness(1.1);
        }

        .cert-item p {
            margin: 0;
            color: #0D6C68;
            font-weight: 600;
            font-size: 1.5rem;
        }

        @media (max-width: 900px) {
            .cert-grid { grid-template-columns: repeat(2, 1fr); }
            .cert-item { height: 280px; max-width: 280px; }
        }

        @media (max-width: 600px) {
            .cert-grid { grid-template-columns: repeat(1, 1fr); }
            .cert-item { height: 260px; max-width: 260px; }
            .cert-title { font-size: 30px; }
        }
        </style>

        <div class="cert-section">
            <h2 class="cert-title">Our Approvals</h2>
            <div class="cert-grid">
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/331752721271.webp" alt="CPWD BHOPAL">
                    <p>CPWD BHOPAL</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/671752721284.webp" alt="CPWD CHANDIGARH">
                    <p>CPWD CHANDIGARH</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/401752721304.webp" alt="CPWD CHENNAI">
                    <p>CPWD CHENNAI</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/901752721318.webp" alt="CPWD HAYDERABAD">
                    <p>CPWD HAYDERABAD</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/851752721336.webp" alt="CPWD LUCKNOW">
                    <p>CPWD LUCKNOW</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/651752721398.webp" alt="CPWD Bhubaneswar">
                    <p>CPWD Bhubaneswar</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/401752721584.jpg" alt="MPPWD">
                    <p>MPPWD</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/471752721613.jpg" alt="PWD KERELA">
                    <p>PWD KERELA</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/481752723854.webp" alt="CPWD Ghandhinagar">
                    <p>CPWD Ghandhinagar</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/31752723921.webp" alt="CPWD Lucknow">
                    <p>CPWD Lucknow</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/291752724047.jpg" alt="PWD Lucknow">
                    <p>PWD Lucknow</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/181752720980.png" alt="CIDCO">
                    <p>CIDCO</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/841752721044.jpg" alt="GOVERNMENT OF ANDHRA PRADESH ROADS AND BUILDINGS DEPARTMENT">
                    <p>GOVERNMENT OF ANDHRA PRADESH ROADS AND BUILDINGS DEPARTMENT</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/401752722112.jpg" alt="MHADA">
                    <p>MHADA</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/771752724001.png" alt="High Speed Rail">
                    <p>High Speed Rail</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/741752721107.png" alt="assystem">
                    <p>assystem</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/401752721187.png" alt="BRIHANMUMBAI MUNICIPAL CORPORATION">
                    <p>BRIHANMUMBAI MUNICIPAL CORPORATION</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/631752721776.jpeg" alt="Design Tree Consulatants">
                    <p>Design Tree Consulatants</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/871752721906.png" alt="IREPS">
                    <p>IREPS</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/151752724263.jpeg" alt="Western Railway">
                    <p>Western Railway</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/631752721982.png" alt="ELCON">
                    <p>ELCON</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/721752722071.jpeg" alt="KITCOL">
                    <p>KITCOL</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/871752722195.png" alt="Sampath Kumar Associates Pvt Ltd – MEP S & S Consulting Engineers">
                    <p>Sampath Kumar Associates Pvt Ltd – MEP Services Consultants</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/221752724366.png" alt="S & S Consulting Engineers">
                    <p>S & S Consulting Engineers</p>
                </div>
                <div class="cert-item">
                    <img src="https://www.armorfire.in/public/upload/approvals/image/761752724558.jpeg" alt="stat consultancy pvt ltd">
                    <p>stat consultancy pvt ltd</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.container():
    st.markdown(
        """
        <style>
        .footer-container {
            background-color: #0D6C68;
            padding: 60px 5% 30px 5%;
            border-radius: 20px 20px 0 0;
            transition: all 0.4s ease-in-out;
            font-family: 'Space Grotesk', sans-serif;
            color: white;
        }
        .footer-container:hover {
            background-color: #118b84;
            box-shadow: 0px 8px 25px rgba(13, 108, 104, 0.5);
            transform: scale(1.01);
        }
        .footer-row {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;
        }
        .footer-column {
            flex: 1;
            min-width: 240px;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 25px 20px;
            border-radius: 12px;
            transition: all 0.3s ease-in-out;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
        }
        .footer-column:hover {
            background-color: white;
            color: #0D6C68 !important;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
            transform: translateY(-5px);
        }
        .footer-column:hover h3,
        .footer-column:hover p {
            color: #0D6C68 !important;
        }

        /* === FIXED: IMAGE WRAPPER === */
        .footer-image-wrapper {
            position: relative;
            width: 150px;
            height: 70px; /* define height to avoid overlap */
            margin-bottom: 15px;
        }

        .footer-image-wrapper img {
            position: absolute;
            top: 0;
            left: 0;
            width: 150px;
            height: auto;
            transition: opacity 0.4s ease-in-out, transform 0.35s ease-in-out;
        }

        .footer-image-wrapper img.hover-img {
            opacity: 0;
        }

        .footer-column:hover .footer-image-wrapper img.main-img {
            opacity: 0;
            transform: translateY(-3px);
        }
        .footer-column:hover .footer-image-wrapper img.hover-img {
            opacity: 1;
            transform: translateY(-3px);
        }

        .logo-strip {
            background-color: #0B5E5A;
            text-align: center;
            padding: 25px 5%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 40px;
            border-radius: 0 0 20px 20px;
        }
        .logo-strip img {
            height: 60px;
            width: auto;
            transition: transform 0.28s ease-in-out, filter 0.28s ease-in-out, opacity 0.28s ease-in-out;
            filter: none;
            opacity: 0.95;
        }
        .logo-strip img:hover {
            transform: scale(1.06);
            filter: brightness(1.12);
            opacity: 1;
        }
        @media (max-width: 900px) {
            .footer-row {
                flex-direction: column;
                align-items: center;
            }
            .footer-column {
                width: 100%;
            }
        }
        </style>

        <!-- === FOOTER SECTION === -->
        <div class="footer-container">
            <div class="footer-row">
                <div class="footer-column">
                    <div class="footer-image-wrapper">
                        <img src="https://www.armorfire.in/public/frontend/assets/images/armorfire-whitelogo.png" class="main-img" alt="Armor Fire">
                        <img src="https://www.armorfire.in/public/frontend/assets/images/armorfire-blacklogo.png" class="hover-img" alt="Armor Fire Hover">
                    </div>
                    Armor Steel Industries Private Limited<br>(Formerly Mahadev Casting)<br><br>
                    <h3 style="font-size:24px;">Reach Us</h3>
                    <p style="font-size:16px;">Plot No. 43/44/45, JK Diamond Industrial Area, B/h, Madhuvan Restaurant,
                       Village - Lothada, Rajkot - Kotdasangani State Highway, Rajkot - 360022, Gujarat, India</p>
                </div>
                <div class="footer-column">
                    <h3 style="font-size:24px;">Send Mail</h3>
                    <p style="font-size:16px;"><b>Sales & Mrkt:</b><br>ho@armorfire.co.in</p><br>
                    <h3 style="font-size:24px;">Contact No.</h3>
                    <p style="font-size:16px;"><b>Customer Care Service:</b><br>+91 93160 27689<br>
                       <b>Sales inquiry:</b><br>+91 99251 37672<br>+91 93161 56590</p>
                </div>
                <div class="footer-column">
                    <h3 style="font-size:24px;">Our Products</h3>
                    <p style="font-size:16px;">Fire Hydrant Valve<br><br>RRL Fire Hose Pipe<br><br>Branch Pipe<br><br>
                       Hose Reel Drum<br><br>Fire Fighting Equipment</p>
                </div>
                <div class="footer-column">
                    <h3 style="font-size:24px;">Quick Links</h3>
                    <p style="font-size:16px;">Company<br><br>Downloads<br><br>Blog<br><br>Career<br><br>
                       Privacy & Policy<br><br>News / Gallery / Media<br><br>Office Presence</p>
                </div>
            </div>
        </div>

        <div class="logo-strip">
            <img src="https://www.armorfire.in/public/frontend/webp/s/2.webp" alt="Logo 1">
            <img src="https://www.armorfire.in/public/frontend/webp/s/3.webp" alt="Logo 2">
            <img src="https://www.armorfire.in/public/frontend/webp/s/4.webp" alt="Logo 3">
            <img src="https://www.armorfire.in/public/frontend/webp/s/5.webp" alt="Logo 4">
            <img src="https://www.armorfire.in/public/frontend/webp/s/6.webp" alt="Logo 5">
            <img src="https://www.armorfire.in/public/frontend/webp/s/7.webp" alt="Logo 6">
            <img src="https://www.armorfire.in/public/frontend/webp/s/1.webp" alt="Logo 7">
        </div>
        """,
        unsafe_allow_html=True
    )
