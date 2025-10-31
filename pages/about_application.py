from PIL import Image
import requests
import base64
import streamlit as st
import time


st.set_page_config(page_title="About Armorfire", layout="wide", page_icon="https://www.armorfire.in/public/frontend/webp/fav-2.webp")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_base64_of_bin_file(image_path):
    """Reads an image file and returns a base64 string."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Background image ---
img_path = r"C:/RONIT/Template/interior-design-website-template-free/img/hero-bg.jpg"
img_base64 = get_base64_of_bin_file(img_path)

# --- Active page ---
active_page = "About"

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
    .block-container {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        /* Remove any fixed attachment */
        background-attachment: scroll; 
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
                Our <span>Application</span>
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
    st.markdown("""
        <style>
            .core-container {
                text-align: center !important;
                padding: 50px 40px !important; /* Slightly reduced padding */
            }
            .core-title {
                color: #0D6C68 !important;
                font-size: 2.5rem !important;
                font-weight: 700 !important;
                margin-bottom: 10px !important; /* Reduced margin */
                font-family: 'Space Grotesk', sans-serif !important;
            }
            .core-quote {
                font-size: 1.5rem !important;
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: bold !important; /* Bold instead of italic */
                margin-bottom: 15px !important; /* Reduced margin */
                margin-top: 15px !important;
                line-height: 1.3 !important; /* Tighter spacing */
                border-top:4px solid white !important;
                padding: 15px !important;
            }
            .core-text {
                font-size: 16px !important;
                max-width: 100% !important;
                margin: 0 auto !important;
                font-family: 'Space Grotesk', sans-serif !important;
                line-height: 1.3 !important; /* Reduced line spacing */
            }

            /* Responsive Design */
            @media (max-width: 768px) {
                .core-title {
                    font-size: 36px !important;
                }
                .core-quote, .core-text {
                    font-size: 16px !important;
                    line-height: 1.3 !important;
                    padding: 0 10px !important;
                }
            }
        </style>

        <div class="core-container">
            <h1 class="core-title">Application</h1>
            <p class="core-quote">Application of our products is in all sector like Highrise & residential building, Villa & Bungalows, All types of inductries (Automobile, Oil & Gas, IT, healthcare, renewable energy, agriculture etc.)</p>
            <p class="core-text">
                Armor Fire offers tailored fire safety solutions across diverse industries. With over two decades of experience, we specialize in developing unique firefighting solutions for critical applications. Our expertise extends to retail and commercial spaces, manufacturing and industrial units, transportation hubs, hospitality venues, educational institutions, healthcare facilities, and residential complexes. From safeguarding businesses and valuable assets to prioritizing the safety of students, patients, and residents, our comprehensive solutions ensure protection and operational continuity in various environments.
            </p>
        </div>
    """, unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <style>
    .core-value-container {
        text-align: center !important;
        padding: 50px 5% !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .core-value-title {
        color: #0D6C68 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 40px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .core-grid {
        display: flex !important;
        gap: 25px !important;
        justify-content: center !important;
        align-items: stretch !important;
        flex-wrap: wrap !important;
    }

    .core-value-column {
        position: relative !important;
        overflow: hidden !important;
        border-radius: 16px !important;
        flex: 1 1 30% !important;
        height: 380px !important;
        min-width: 300px !important;
        box-shadow: 0 0 15px rgba(0,0,0,0.1) !important;
        transition: all 0.4s ease !important;
        cursor: pointer !important;
        background: #f9f9f9 !important;
    }

    .core-value-column img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        transition: all 0.5s ease !important;
        border-radius: 16px !important;
    }

    .overlay {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: rgba(13,108,104,0.0) !important;
        color: white !important;
        opacity: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding: 25px !important;
        border-radius: 16px !important;
        transition: all 0.5s ease !important;
        text-shadow: 0 0 15px rgba(0,0,0,0.3) !important;
    }

    .overlay h2 {
        font-size: 1.5rempx !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    .overlay p {
        font-size: 16px !important;
        line-height: 1.5 !important;
        max-width: 85% !important;
    }

    .core-value-column:hover img {
        transform: scale(1.1) !important;
        filter: blur(3px) brightness(0.7) !important;
    }

    .core-value-column:hover .overlay {
        opacity: 1 !important;
        background: rgba(13,108,104,0.85) !important;
    }

    @media (max-width: 900px) {
        .core-grid {
            flex-direction: column !important;
            align-items: center !important;
        }
        .core-value-column {
            width: 100% !important;
            height: 320px !important;
        }
    }
    </style>

    <div class="core-value-container">
        <h1 class="core-value-title">Applications</h1>
        <div class="core-grid">
            <div class="core-value-column">
                <img src="	https://www.armorfire.in/public/frontend/webp/g/1.webp" alt="Oil & Gas, Petrochemical">
                <div class="overlay">
                    <h2>Oil & Gas, Petrochemical</h2>
                    <p>Armor Fire</p>
                </div>
            </div>
            <div class="core-value-column">
                <img src="	https://www.armorfire.in/public/frontend/webp/g/2.webp" alt="Power Plants">
                <div class="overlay">
                    <h2>Power Plants</h2>
                    <p>Armor Fire</p>
                </div>
            </div>
            <div class="core-value-column">
                <img src="https://www.armorfire.in/public/frontend/webp/g/3.webp" alt="Commercial & Residential Buildings, Hotels and Airports">
                <div class="overlay">
                    <h2>Commercial & Residential Buildings, Hotels and Airports</h2>
                    <p>Armor FIre</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div class="core-value-container">
        <div class="core-grid">
            <div class="core-value-column">
                <img src="https://www.armorfire.in/public/frontend/webp/g/4.webp" alt="Data Centers">
                <div class="overlay">
                    <h2>Data Centers</h2>
                    <p>Armor Fire</p>
                </div>
            </div>
            <div class="core-value-column">
                <img src="	https://www.armorfire.in/public/frontend/webp/g/5.webp" alt="Manufacturing">
                <div class="overlay">
                    <h2>Manufacturing</h2>
                    <p>Armor Fire</p>
                </div>
            </div>
            <div class="core-value-column">
                <img src="https://www.armorfire.in/public/frontend/webp/g/6.webp" alt="Special Projects">
                <div class="overlay">
                    <h2>Special Projects</h2>
                    <p>Armor FIre</p>
                </div>
            </div>
        </div>
    </div>
    """,unsafe_allow_html=True)    

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
