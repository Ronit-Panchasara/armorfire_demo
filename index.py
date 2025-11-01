import re
# redeploy fix
from PIL import Image
import os
import requests
import base64
import pathlib
import streamlit as st
import streamlit.components.v1 as components
import time
import itertools

st.set_page_config(page_title="Armorfire", layout="wide", page_icon="https://www.armorfire.in/public/frontend/webp/fav-2.webp")

img_path = os.path.join("img", "hero-bg.jpg")

def get_base64_of_bin_file(image_path):
    if not os.path.exists(image_path):
        st.error(f"Error: File not found at {image_path}")
        raise FileNotFoundError(f"File not found: {image_path}") 
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')
code_dir = pathlib.Path(__file__).parent.resolve()

img_path = code_dir / "img" / "hero-bg.jpg" 

img_path_str = str(img_path)

try:
    img_base64 = get_base64_of_bin_file(img_path_str) 
except FileNotFoundError as e:
    st.error(e)

# --- Active page ---
active_page = "Home"

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


slider_html = """
<style>
/* Remove Streamlit padding */
.block-container { padding: 0 !important; margin: 0 !important; }

/* Full-browser-width slider */
.slider-container {
  position: relative;
  border-radius: 15px;
  width: 100vw;
  height: 90vh;
  left: 50%;
  margin-left: -50vw;
  overflow: hidden;
  z-index: 1;
}

/* Slides */
.slides {
  display: flex;
  transition: transform 1s ease-in-out;
  height: 100%;
}
.slides img {
  width: 100vw;
  height: 90vh;
  object-fit: cover;
  display: block;
}

/* Buttons */
.button-container {
  position: absolute;
  top: 50%;
  width: 96%;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  padding: 0 25px;
  z-index: 10;
  pointer-events: none;
}
.button {
  background-color: #0D6C68;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 50px;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  font-family: 'Space Grotesk', sans-serif;
  pointer-events: all;
}
.button:hover { background-color: #3d8986; transform: scale(1.08); }

/* Dots */
.dots {
  position: absolute;
  bottom: 24px;            /* slightly up from the very bottom for nicer spacing */
  width: 100%;
  text-align: center;
  z-index: 20;
}
.dot {
  height: 12px;
  width: 12px;
  margin: 0 6px;
  background-color: rgba(255,255,255,0.6);
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.25s, transform 0.2s;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.25);
  border: 2px solid rgba(0,0,0,0.08);
}
.dot.active {
  background-color: #0D6C68;
  transform: scale(1.15);
}

/* Responsive */
@media (max-width: 768px) {
  .slider-container { height: 60vh; }
  .slides img { height: 60vh; }
  .button { font-size: 16px; padding: 8px 16px; }
  .button-container { width: 94%; padding: 0 10px; }
}
</style>

<div class="slider-container">
  <div class="slides" id="slides">
    <img src="https://www.armorfire.in/public/upload/homebannerimg/3917541188753.jpg" alt="slide1">
    <img src="https://www.armorfire.in/public/upload/homebannerimg/317541104013.jpg" alt="slide2">
    <img src="https://www.armorfire.in/public/upload/homebannerimg/8517541103913.jpg" alt="slide3">
    <!-- clone first for seamless loop -->
    <img src="https://www.armorfire.in/public/upload/homebannerimg/3917541188753.jpg" alt="clone">
  </div>

  <div class="button-container">
    <button class="button" onclick="manualPrev()">⟵</button>
    <button class="button" onclick="manualNext()">⟶</button>
  </div>

  <!-- Dots: one dot per real slide -->
  <div class="dots" id="dots">
    <span class="dot active" data-index="0"></span>
    <span class="dot" data-index="1"></span>
    <span class="dot" data-index="2"></span>
  </div>
</div>

<script>
const slides = document.getElementById('slides');
const dotEls = document.querySelectorAll('.dot');
const totalSlidesWithClone = slides.children.length; // includes clone
const realCount = totalSlidesWithClone - 1;         // real slides count
let index = 0;
let autoTimer = null;
const TRANSITION_DURATION = 1000; // ms, must match CSS transition

// helper: set active dot (based on real slide index)
function setActiveDot(realIndex) {
  dotEls.forEach((d, i) => d.classList.toggle('active', i === realIndex));
}

// move to next slide (right only)
function nextSlide() {
  index++;
  slides.style.transition = 'transform 1s ease-in-out';
  slides.style.transform = `translateX(-${index * 100}vw)`;

  // update dots for normal slides and the clone (show first dot while on clone)
  const visibleDot = index % realCount;
  setActiveDot(visibleDot);

  // if we've moved onto the cloned slide, reset to real first slide (0) after transition
  if (index === totalSlidesWithClone - 1) {
    setTimeout(() => {
      slides.style.transition = 'none';
      slides.style.transform = 'translateX(0)';
      index = 0;
      // ensure dots show first
      setActiveDot(0);
      // force reflow then re-enable transition (avoids flash)
      void slides.offsetWidth;
      slides.style.transition = 'transform 1s ease-in-out';
    }, TRANSITION_DURATION);
  }
}

// manual navigation handlers
function manualNext() {
  // if currently at clone reset instantly to real last slide position before moving
  if (index === totalSlidesWithClone - 1) {
    slides.style.transition = 'none';
    slides.style.transform = `translateX(-0vw)`;
    index = 0;
    void slides.offsetWidth;
    slides.style.transition = 'transform 1s ease-in-out';
  }
  nextSlide();
  resetAuto();
}

function manualPrev() {
  // move backward within real slides only
  // if at 0, jump to last real slide instantly, then animate back one
  if (index === 0) {
    slides.style.transition = 'none';
    slides.style.transform = `translateX(-${(realCount - 1) * 100}vw)`; // show last real
    index = realCount - 1;
    void slides.offsetWidth;
    slides.style.transition = 'transform 1s ease-in-out';
  } else {
    index = Math.max(0, index - 1);
  }
  slides.style.transform = `translateX(-${index * 100}vw)`;
  setActiveDot(index % realCount);
  resetAuto();
}

// clickable dots: jump to selected real slide
dotEls.forEach(dot => {
  dot.addEventListener('click', (e) => {
    const target = Number(e.currentTarget.getAttribute('data-index'));
    index = target;
    slides.style.transition = 'transform 1s ease-in-out';
    slides.style.transform = `translateX(-${index * 100}vw)`;
    setActiveDot(target);
    resetAuto();
  });
});

// autoplay
function startAuto() {
  autoTimer = setInterval(nextSlide, 3500);
}
function resetAuto() {
  clearInterval(autoTimer);
  startAuto();
}

// initialize
setActiveDot(0);
startAuto();
</script>
"""

components.html(slider_html, height=850, scrolling=False)

# --- Main Header Section Below the Banner ---
st.markdown(
        """
            <p class="my-title">
                To <span>Grow & Secure</span><br>
                Lives with <span>Shield</span> of Quality
            </p>
            <div class="box">
                Formerly Mahadev Casting
            </div>
            """,
            unsafe_allow_html=True
        )


# with st.container():
#     st.markdown("""
#         <style>
#         .four-column-container {
#             display: flex;
#             justify-content: space-between;
#             gap: 20px;
#             margin-top: 40px;
#         }
#         .four-column-box {
#             flex: 1;
#             height: 220px; /* fixed equal height for all boxes */
#             background: rgba(0, 0, 0, 0.45);
#             border-radius: 15px;
#             color: white;
#             font-family: 'Space Grotesk', sans-serif !important;
#             font-size: 22px !important;
#             font-weight: 500 !important;
#             text-align: center;
#             padding: 20px;
#             display: flex;
#             align-items: center;        /* vertical center */
#             justify-content: center;    /* horizontal center */
#             box-shadow: 0 0 15px rgba(0,0,0,0.3);
#             transition: all 0.3s ease;
#         }
#         .four-column-box:hover {
#             background: rgba(13,108,104,0.6);
#             transform: translateY(-6px);
#         }

#         /* --- Responsive layout for mobile --- */
#         @media (max-width: 900px) {
#             .four-column-container {
#                 flex-direction: column;
#             }
#             .four-column-box {
#                 height: 180px;
#                 margin-bottom: 20px;
#             }
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # --- 4 boxes layout ---
#     st.markdown("""
#         <div class="four-column-container">
#             <div class="four-column-box">Morality & Responsibility</div>
#             <div class="four-column-box">Customer First, Customer is God</div>
#             <div class="four-column-box">Never-Ending Growth with “Armor Fire”</div>
#             <div class="four-column-box">Transparency With Armor Fire</div>
#         </div>
#     """, unsafe_allow_html=True)


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
                margin-top:50px !important;
                margin-bottom: 10px !important; /* Reduced margin */
                font-family: 'Space Grotesk', sans-serif !important;
            }
            .core-quote {
                font-size: 1.5rem !important;
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: bold !important; /* Bold instead of italic */
                margin-bottom: 15px !important; /* Reduced margin */
                line-height: 1.3 !important; /* Tighter spacing */
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
            <h1 class="core-title">CORE PURPOSE</h1>
            <p class="core-quote">"To Grow & Secure Lives with Shield of Quality"</p>
            <p class="core-text">
                This ideology reflects Armor Fire unwavering commitment to protecting lives and assets 
                through innovation and service, while fostering continuous growth — for our customers, 
                partners, employees, vendors and society at large.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""          
<style>
.core-value-container {{
    text-align: center !important;
    padding: 50px 5% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

.core-value-title {{
    color: #0D6C68 !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 40px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

.core-grid {{
    display: flex !important;
    gap: 20px !important;
    justify-content: center !important;
    align-items: stretch !important;  /* ensures equal height */
}}

.core-value-column {{
    background: rgba(13,108,104,0.05) !important;
    padding: 25px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;  /* equal width for all */
}}

.core-value-column:hover {{
    background: #0D6C68 !important;
}}

.core-value-column:hover .core-value-subtitle,
.core-value-column:hover .core-value-text {{
    color: white !important;
}}

.core-value-subtitle {{
    color: #0D6C68 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}}
span:hover {{
    color:white;
}}
.core-value-text {{
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #000 !important;
    flex-grow: 1 !important;  /* ensures equal height */
    text-align: left !important;        
}}

@media (max-width: 900px) {{
    .core-grid {{
        flex-direction: column !important;
    }}
}}
</style>

<div class="core-value-container">
    <h1 class="core-value-title">CORE VALUE</h1>
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle"><img width="50" height="50" src="https://img.icons8.com/ios-filled/50/scales--v1.png" alt="scales--v1"/>Morality & Responsibility</h2>
            <p class="core-value-text">
                Given By <b>Armor Fire</b>: We are guided by integrity, honesty, and fairness — doing what's right even when no one is watching. 
                We take full ownership of our commitments, ensuring safety, quality, and reliability in every product and service we deliver.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle"><img width="50" height="50" src="https://img.icons8.com/ios/50/helping-hand.png" alt="helping-hand"/>Customer First, Customer is God</h2>
            <p class="core-value-text">
                <b>At Armor Fire</b>, we treat every customer with the same care and commitment as we put into every product we build. 
                To us, the customer is not just important — the customer is everything.<br><br>
                <b>Our promise is built on:</b><br>
                <span>✔</span> Premium Quality<br><span>✔</span> Timely Delivery<br><span>✔</span> Customer Respect<br><br>
                Just like our name, Armor Fire, we stand strong — protecting what matters, and serving our customers with dedication and honor.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle"><img width="50" height="50" src="https://img.icons8.com/ios-glyphs/30/positive-dynamic.png" alt="positive-dynamic"/> Never-Ending Growth with “Armor Fire”</h2>
            <p class="core-value-text">
                We believe in evolving every day — personally, professionally, and technologically. 
                We invest in our team's learning and leadership to unlock their full potential. 
                Our ambition is to expand our impact locally and globally without ever compromising our core values.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="core-value-column">
            <h2 class="core-value-subtitle"><img width="64" height="64" src="https://img.icons8.com/laces/64/user.png" alt="user"/>R&D and Hard Work</h2>
            <p class="core-value-text" style="font-family: 'Space Grotesk', sans-serif;">
            <b>Here in Armor Fire....</b> We lead with research and development to stay at the forefront of fire safety technology. We believe in consistent, disciplined hard work no shortcuts. We under take challenges with data, creativity, and relentless determination.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="core-value-column">
            <h2 class="core-value-subtitle"><img width="50" height="50" src="https://img.icons8.com/metro/26/search.png" alt="search"/>Transparency With Armor Fire</h2>
            <p class="core-value-text" style="font-family: 'Space Grotesk', sans-serif;">
                We uphold honesty and clarity in all internal and external communications. We share information openly to build trust with customers, partners, employees and vendors. Our operations are built on truth, not maneuver what you see is what you get with <b>Armor Fire.</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
with st.container():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    .bhag-title {
        text-align: center !important;
        color: #0D6C68 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-top: 15px !important;
        margin-bottom: 0 !important;
    }

    .bhag-text {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        text-align: justify !important;
        margin-top: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <hr style="
        border: none;         
        height: 4px;          
        background-color: white; 
        width: 100%;           
        margin-left: 0;       
        margin-right: 0;      
    ">
    """,
    unsafe_allow_html=True
)

with st.container():
    left_column, right_column = st.columns([3, 7])  # 30:70 ratio
    with left_column:
        st.markdown("<h1 class='bhag-title'>Big Hairy Audacious Goal (BHAG)</h1>", unsafe_allow_html=True)
    with right_column:
        st.markdown("""
            <div class='bhag-text'>
            “ To Become a World Pioneer Brand with ₹5,000 Crore Market Capitalization by 31st March 2045 ”
            <br><br>
            At Armor Fire, we don’t just aim high — we aim beyond. Our BHAG is a bold declaration of our long-term ambition:
            <ul>
                <li>To establish Armor Fire as a globally recognized pioneer in fire safety innovation and service excellence.</li>
                <li>To achieve a market capitalization of ₹5,000 Crores by 31st March 2045.</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <style>
            .core-container {
                text-align: center !important;
                padding: 50px 40px !important;
                margin-top:5px !important;
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
                line-height: 1.3 !important; /* Tighter spacing */
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
            <h1 class="core-title">Vivid Description</h1>
            <p class="core-quote">The Future of Armor Fire: Vision 2045</p>
            <p class="core-text">
                By the year 2045, Armor Fire will rise as the world's most trusted all-in-one firefighting solutions provider a name that reflection innovation, reliability, and global leadership in fire safety.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""          
<style>
.core-value-container {{
    text-align: center !important;
    padding: 50px 5% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

.core-value-title {{
    color: #0D6C68 !important;
    font-size: 36px !important;
    font-weight: 700 !important;
    margin-bottom: 40px !important;
}}

.core-grid {{
    display: flex !important;
    gap: 20px !important;
    justify-content: center !important;
    align-items: stretch !important;  /* ensures equal height */
}}

.core-value-column {{
    background: rgba(13,108,104,0.05) !important;
    padding: 25px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;  /* equal width for all */
}}

.core-value-column:hover {{
    background: #0D6C68 !important;
}}

.core-value-column:hover .core-value-subtitle,
.core-value-column:hover .core-value-text {{
    color: white !important;
}}

.core-value-subtitle {{
    color: #0D6C68 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}}
span:hover {{
    color:white;
}}
.core-value-text {{
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #000 !important;
    flex-grow: 1 !important;  /* ensures equal height */
    text-align: left !important;
}}

@media (max-width: 900px) {{
    .core-grid {{
        flex-direction: column !important;
    }}
}}
</style>

<div class="core-value-container">
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle">A Headquarters That Embodies Our Vision</h2>
            <p class="core-value-text">
                <span>✔</span> Our 100-acre state-of-the-art campus will be a beacon of excellence, housing<br><br>
                <span>✔</span> Advanced manufacturing units<br><br>
                <span>✔</span> Cutting-edge R&D laboratories<br><br>
                <span>✔</span> World-class training academies<br><br>
                <span>✔</span> Green energy infrastructure<br><br>
                <span>✔</span> This campus will reflect our unwavering commitment to sustainability, s         afety, and scalable growth.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Global Presence, Local Strength</h2>
            <p class="core-value-text">
                <span>✔</span> Regional headquarters and warehouses in Dubai and key African nations will serve as strategic hubs for international operations.<br><br>
                <span>✔</span> In India, four zonal mega-warehouses (North, South, East, West) will ensure rapid delivery and seamless service.<br><br>
                <span>✔</span> Our products will be exported to over 60 countries, establishing Armor Fire as a globally respected brand.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Comprehensive Product Ecosystem</h2>
            <p class="core-value-text">
                <span>✔</span> We will offer the full spectrum of GROOVE Fire Fighting Systems, including:<br><br>
                <span>✔</span> Basic extinguishers<br><br>
                <span>✔</span> AI-powered suppression systems<br><br>
                <span>✔</span> Smart alarms<br><br>
                <span>✔</span> Industrial-scale fire protection solutions<br><br>
                <span>✔</span> Our R&D division will lead the charge in developing next-generation fire safety technologies, setting new industry benchmarks.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""          
<style>
.core-value-container {{
    text-align: center !important;
    padding: 50px 5% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

.core-value-title {{
    color: #0D6C68 !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 40px !important;
}}

.core-grid {{
    display: flex !important;
    gap: 20px !important;
    justify-content: center !important;
    align-items: stretch !important;  /* ensures equal height */
}}

.core-value-column {{
    background: rgba(13,108,104,0.05) !important;
    padding: 25px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;  /* equal width for all */
}}

.core-value-column:hover {{
    background: #0D6C68 !important;
}}

.core-value-column:hover .core-value-subtitle,
.core-value-column:hover .core-value-text {{
    color: white !important;
}}

.core-value-subtitle {{
    color: #0D6C68 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}}
span:hover {{
    color:white;
}}
.core-value-text {{
    text-align: left !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #000 !important;
    flex-grow: 1 !important;  /* ensures equal height */
}}

@media (max-width: 900px) {{
    .core-grid {{
        flex-direction: column !important;
    }}
}}
</style>

<div class="core-value-container">
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle">A Thriving Workforce of 2,000+</h2>
            <p class="core-value-text">
                <span>✔</span> Our team will include 2,000+ passionate professionals—engineers, innovators, safety experts, visionary leaders and adviser.<br><br>
                <span>✔</span> We will recruit top talent from India’s premier institutions like the IIMs, IITs and leading world’s institutions.<br><br>
                <span>✔</span> Our in-house leadership development programs will nurture future-ready professionals.<br><br>
                <span>✔</span> Employee achievements will be celebrated with international trips and recognition programs.<br><br>
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Market Leadership & Recognition</h2>
            <p class="core-value-text">
                <span>✔</span> <b>Armor Fire</b> will proudly be listed on the Main Board of the Stock Market (IPO), marking a major milestone in our journey in world.<br><br>
                <span>✔</span> Our success story will be featured in global media, showcasing our innovation and impact.<br><br>
                <span>✔</span> We will build a robust network of <b>500+ distributors</b> across India and Abroad, ensuring unmatched reach and service.<br><br>
                <span>✔</span><b> Certified Excellence with</b><br>
                <span>•</span> ISO
                <span>•</span> BIS
                <span>•</span> CE<br><br>
                <span>✔</span><b> We Will Grow Up with Of</b><br>
                <span>•</span> UL
                <span>•</span> LPCB
                <span>•</span> FM,etc
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Social Responsibility</h2>
            <p class="core-value-text">
                <span>✔</span> We will establish and run our own NGO, dedicated to fire safety awareness, disaster relief, and community development.<br><br>
                <span>✔</span> Our commitment to social impact will be as strong as our commitment to innovation.<br><br>
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <hr style="
        border: none;         
        height: 4px;          
        background-color: white; 
        width: 100%;           
        margin-left: 0;       
        margin-right: 0;      
    ">
    """,
    unsafe_allow_html=True
)

# st.markdown(
#     """
#     <style>
#     .cert-container {
#         background-color: white;
#         padding: 30px;
#         border-radius: 15px;
#         box-shadow: 0 0 15px rgba(0,0,0,0.1);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# --- Container with background ---
with st.container():
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

    .custom2-header {
        color: black !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem !important;
        text-align: left !important;
        margin-bottom: 0 !important;
        display: inline-block;
        border-bottom: 4px solid white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.markdown('<div class="cert-container">', unsafe_allow_html=True)
    st.markdown('<p class="custom2-header">OUR CERTIFICATIONS</p><br><br>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5,c6 = st.columns(6)
    with c1:
        st.image("https://www.armorfire.in/public/frontend/webp/certification/c2.webp", width=150)
    with c2:
        st.image("https://www.armorfire.in/public/frontend/webp/certification/gst.webp", width=150)
    with c3:
        st.image("https://www.armorfire.in/public/frontend/webp/certification/zed-bronze.webp", width=150)
    with c4:
        st.image("https://www.armorfire.in/public/frontend/webp/certification/msme.webp", width=150)
    with c5:
        st.image("https://www.armorfire.in/public/frontend/webp/certification/ISO.webp", width=150)
    with c6:
        st.image("https://www.armorfire.in/public/frontend/webp/certification/import-export.webp", width=150)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

    .custom-header {
        color: black !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem !important;
        text-align: left !important;
        margin-bottom: 0 !important;
        display: inline-block;
        border-bottom: 4px solid white !important;
    }
    .stMarkdown .custom-title {
        color: #0D6C68 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        text-align: left !important;
        margin-top: 5px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Content ---
with st.container():
    st.markdown('<p class="custom-header">OUR MANUFACTURED RANGE</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-title">Explore What We Manufacture</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="cert-container">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5,c6 = st.columns(6)
    with c1:
        st.image("https://www.armorfire.in/public/upload/productimg/731756471488.jpg", width=180)
    with c2:
        st.image("https://www.armorfire.in/public/upload/productimg/321754397118.jpg", width=185)
    with c3:
        st.image("https://www.armorfire.in/public/upload/productimg/71754384068.JPG", width=150)
    with c4:
        st.image("https://www.armorfire.in/public/upload/productimg/301704784429.jpg", width=150)
    with c5:
        st.image("https://www.armorfire.in/public/upload/productimg/871704794017.jpg", width=165)
    with c6:
        st.image("https://www.armorfire.in/public/upload/productimg/221704784686.jpg", width=137)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

    .custom-header {
        color: black !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem !important;
        text-align: left !important;
        margin-bottom: 0 !important;
        display: inline-block;
        border-bottom: 4px solid white !important;
    }
    .stMarkdown .custom-title {
        color: #0D6C68 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        text-align: left !important;
        margin-top: 5px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Content ---
with st.container():
    st.markdown('<p class="custom-header">OUR SUPPLY</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-title">SUPPLY TO PUBLIC SECTOR</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="cert-container">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5,c6 = st.columns(6)
    with c1:
        st.image("https://www.armorfire.in/public/frontend/webp/client/4.webp", width=350)
    with c2:
        st.image("https://www.armorfire.in/public/frontend/webp/client/1.webp", width=350)
    with c3:
        st.image("https://www.armorfire.in/public/frontend/webp/client/2.webp", width=350)
    with c4:
        st.image("https://www.armorfire.in/public/frontend/webp/client/3.webp", width=350)
    with c5:
        st.image("https://www.armorfire.in/public/frontend/webp/client/5.webp", width=350)
    with c6:
        st.image("https://www.armorfire.in/public/frontend/webp/client/6.webp", width=350)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <hr style="
        border: none;         
        height: 4px;          
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
            .core-title2 {
                color: #0D6C68 !important;
                font-size: 2.5rem !important;
                font-weight: 700 !important;
                margin-bottom: -40px !important; /* Reduced margin */
                margin-top: 30px !important; /* Reduced margin */
                font-family: 'Space Grotesk', sans-serif !important;
            }
        </style>

        <div class="core-container">
            <h1 class="core-title2">Our Fire Protection Equipment and Systems</h1>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""          
<style>
.core-value-container {{
    text-align: center !important;
    padding: 50px 5% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

.core-value-title {{
    color: #0D6C68 !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 40px !important;
}}

.core-grid {{
    display: flex !important;
    gap: 20px !important;
    justify-content: center !important;
    align-items: stretch !important;  /* ensures equal height */
}}

.core-value-column {{
    background: rgba(13,108,104,0.05) !important;
    padding: 25px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;  /* equal width for all */
}}

.core-value-column:hover {{
    background: #0D6C68 !important;
}}

.core-value-column:hover .core-value-subtitle,
.core-value-column:hover .core-value-text {{
    color: white !important;
}}

.core-value-subtitle {{
    color: #0D6C68 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}}
span:hover {{
    color:white;
}}
.core-value-text {{
    text-align: left !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #000 !important;
    flex-grow: 1 !important;  /* ensures equal height */
}}
button {{
    background-color: #0D6C68;      /* main brand color */
    color: white;                   /* text color */
    border: none;                   /* remove default border */
    padding: 12px 25px;             /* more spacious padding */
    border-radius: 12px;            /* rounded corners */
    cursor: pointer;                /* pointer on hover */
    font-weight: 600;               /* bold text */
    font-size: 16px;
    transition: all 0.3s ease;      /* smooth hover transition */
    box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* subtle shadow */
}}

button:hover {{
    background-color: white;        /* inverted on hover */
    color: #0D6C68;                /* text color changes to brand */
    box-shadow: 0 6px 15px rgba(13,108,104,0.3); /* bigger shadow on hover */
    transform: translateY(-3px);    /* slight lift effect */
}}

@media (max-width: 900px) {{
    .core-grid {{
        flex-direction: column !important;
    }}
}}
</style>

<div class="core-value-container">
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle"> Fire Fighting Equipment</h2>
            <img src="https://www.armorfire.in/public/frontend/assets/images/products/fire-equipment.jpg" width="100%" height="100%"><br>
            <p class="core-value-text">
                Stay ready for any emergency with our top-of-the-line fire-fighting equipment. Planned for dependability, our equipments are crafted to meet the highest safety standards, providing swift action when it matters most.
            </p>
            <button>Learn More</button>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Fire Hydrant Systems</h2>
            <img src="https://www.armorfire.in/public/frontend/assets/images/products/double-hydrant-valve.jpg"><br>
            <p class="core-value-text">
                Secure robust fire protection with our advanced fire hydrant systems, created to provide a great water supply for quick and effective fire suppression, protecting both lives and property.
            </p>
            <button>Learn More</button>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle"> Water Spray Nozzles & Branch Pipes</h2>
            <img src="https://www.armorfire.in/public/frontend/assets/images/products/image-2.jpg" width="100%" height="100%"><br>
            <p class="core-value-text">
                Supply targeted fire control with our premium water spray nozzles and branch pipes. Built for precision, they’re important for efficient fire suppression in high-risk conditions.
            </p>
            <button>Learn More</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""  
<div class="core-value-container">
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle"> Hose Reel Drum</h2>
            <img src="https://www.armorfire.in/public/frontend/assets/images/products/hose-reel-drum.jpg" width="100%" height="100%"><br>
            <p class="core-value-text">
                Designed for convenience and efficiency, our hose reel drums ensure quick access and secure storage of fire hoses, ready for immediate use during emergencies.
            </p>
            <button>Learn More</button>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Fire Extinguishers</h2>
            <img src="https://www.armorfire.in/public/frontend/assets/images/products/fire-extinguishers.jpg"><br>
            <p class="core-value-text">
                Our universal fire extinguishers are suited for various fire types, providing fast, effective suppression in points of urgent need. Prepare your space with trusted security.
            </p>
            <button>Learn More</button>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle"> Fire Sprinklers</h2>
            <img src="https://www.armorfire.in/public/frontend/assets/images/products/fire-sprinklers.jpg" width="100%" height="100%"><br>
            <p class="core-value-text">
                Improve security with our state-of-the-art fire sprinklers, created to see and stop flames at the earliest signs of fire, delivering an automated, efficient response.
            </p>
            <button>Learn More</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# st.markdown(
#     """
#     <hr style="
#         border: none;         
#         height: 4px;          
#         background-color: white; 
#         width: 100%;           
#         margin-left: 0;       
#         margin-right: 0;      
#     ">
#     """,
#     unsafe_allow_html=True
# )

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
                border-bottom: 4px solid white !important;
            }
            .core-quote2 {
                font-size:1.5rem !important;
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: bold !important; /* Bold instead of italic */
                margin-bottom: 15px !important; /* Reduced margin */
                line-height: 1.3 !important; /* Tighter spacing */
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
            <h1 class="core-title">Armor Fire</h1>
            <p class="core-quote2">Protecting Lives, Securing Futures, One Flame at a Time.</p>
        </div>
    """, unsafe_allow_html=True)
    

st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

# Counters with big number words as background
st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
<style>
.counters-wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 50px;
  position: relative;
  font-family: 'Space Grotesk', sans-serif !important;
  padding: 50px 0;
}
.counters-wrapper::before {
  content: 'Numbers';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 300px;
  color: rgba(13,108,104,0.1); /* faint decorative background */
  white-space: nowrap;
  pointer-events: none;
  z-index: 0;
}
.counter-container {
  text-align: center;
  flex: 1;
  position: relative;
  z-index: 1; /* keep counters above background */
}
.counter-icon {
  width: 80px;
  height: 80px;
  background-color: #0D6C68;
  border-radius: 50%;
  display: inline-block;
  margin-bottom: 15px;
  background-size: 50%;
  background-repeat: no-repeat;
  background-position: center;
}
.counter-number {
  font-size: 70px;
  color: #0D6C68;
  margin: 0;
}
.counter-label {
  font-size: 1.5rem;
}
</style>
</head>
<body>

<div class="counters-wrapper">
  <div class="counter-container">
    <div class="counter-icon" style="background-image: url('https://www.armorfire.in/public/frontend/webp/icon/Year.webp');"></div>
    <h1 id="counter-experience" class="counter-number" data-speed="1500">0+</h1>
    <span class="counter-label"><b>Years</b><br> Of Experience</span>
  </div>

  <div class="counter-container">
    <div class="counter-icon" style="background-image: url('https://www.armorfire.in/public/frontend/webp/icon/Project.webp');"></div>
    <h1 id="counter-products" class="counter-number" data-speed="1500">0+</h1>
    <span class="counter-label"><b>Our Products</b><br>Products with 100% Satisfaction</span>
  </div>

  <div class="counter-container">
    <div class="counter-icon" style="background-image: url('https://www.armorfire.in/public/frontend/webp/icon/Team.webp');"></div>
    <h1 id="counter-team" class="counter-number" data-speed="1500">0+</h1>
    <span class="counter-label"><b>Team</b><br> Top Expert Team</span>
  </div>
</div>

<script>
function animateCounter(counterId, target) {
  const counter = document.getElementById(counterId);
  const speed = parseInt(counter.getAttribute("data-speed"));
  let count = 0;
  const increment = target / (speed / 20);

  const timer = setInterval(() => {
    count += increment;
    if (count >= target) {
      count = target;
      clearInterval(timer);
    }
    counter.textContent = Math.floor(count) + "+";
  }, 20);
}

const counters = [
  { id: "counter-experience", target: 15 },
  { id: "counter-products", target: 50 },
  { id: "counter-team", target: 250 }
];

counters.forEach(c => {
  const element = document.getElementById(c.id).parentElement;
  let started = false;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !started) {
        started = true;
        animateCounter(c.id, c.target);
      }
    });
  }, { threshold: 0.6 });

  observer.observe(element);
});
</script>

</body>
</html>
""", height=400)

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
                border-bottom: 4px solid white !important;
            }
            .core-quote2 {
                font-size:1.5rem !important;
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: bold !important; /* Bold instead of italic */
                margin-bottom: 15px !important; /* Reduced margin */
                line-height: 1.3 !important; /* Tighter spacing */
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
            <h1 class="core-title">Why Choose Us as the Best Fire Fighting Equipment Manufacturers in India <br>?</h1>
            <p class="core-quote2">Armor Fire is a professional Fire Fighting equipment supplier in India. We have delivered huge products all over the world and set a legacy. Here are unique qualities that make us the top Fire Fighting equipment manufacturers in India to provide Fire Fighting equipment</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""          
<style>
.core-value-container {{
    text-align: center !important;
    padding: 50px 5% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}
.core-value-title {{
    color: #0D6C68 !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 40px !important;
}}
.core-grid {{
    display: flex !important;
    gap: 20px !important;
    justify-content: center !important;
    align-items: stretch !important;  /* ensures equal height */
}}
.core-value-column {{
    background: rgba(13,108,104,0.05) !important;
    padding: 25px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;  /* equal width for all */
}}
.core-value-column:hover {{
    background: #0D6C68 !important;
}}
.core-value-column:hover .core-value-subtitle,
.core-value-column:hover .core-value-text {{
    color: white !important;
}}
.core-value-subtitle {{
    color: #0D6C68 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    display: flex !important;
    gap: 10px !important;
}}
span:hover {{
    color:white;
}}
.core-value-text {{
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #000 !important;
    text-align: left !important;
    flex-grow: 1 !important;  /* ensures equal height */
}}
@media (max-width: 900px) {{
    .core-grid {{
        flex-direction: column !important;
    }}
}}
</style>

<div class="core-value-container">
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Product Development</h2>
            <p class="core-value-text">
                We at Armor Fire, have a dedicated team to develop and manufacture the fire fighting equipment. We produce the products as per customers' requirements and their drawings.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Customized</h2>
            <p class="core-value-text">
                We have our in-house machinery factory, that provides you fire fighting equipment directly, ensuring seamless customization based on your specifications.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Capacity</h2>
            <p class="core-value-text">
                Our comprehensive production capabilities permit us to provide a vast variety of fire-fighting equipment, meeting large-scale customer demands with efficiency.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""          
<style>
.core-value-container {{
    text-align: center !important;
    padding: 50px 5% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}}

.core-value-title {{
    color: #0D6C68 !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 40px !important;
}}

.core-grid {{
    display: flex !important;
    gap: 20px !important;
    justify-content: center !important;
    align-items: stretch !important;  /* ensures equal height */
}}

.core-value-column {{
    background: rgba(13,108,104,0.05) !important;
    padding: 25px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;  /* equal width for all */
}}

.core-value-column:hover {{
    background: #0D6C68 !important;
}}

.core-value-column:hover .core-value-subtitle,
.core-value-column:hover .core-value-text {{
    color: white !important;
}}

.core-value-subtitle {{
    color: #0D6C68 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    display: flex !important;
    gap: 0px !important;
}}
span:hover {{
    color:white;
}}
.core-value-text {{
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #000 !important;
    text-align: left !important;
    flex-grow: 1 !important;  /* ensures equal height */
}}

@media (max-width: 900px) {{
    .core-grid {{
        flex-direction: column !important;
    }}
}}
</style>

<div class="core-value-container">
    <div class="core-grid">
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Quality</h2>
            <p class="core-value-text">
                We have a strong quality control system supported by advanced inspection equipment and our dedicated testing lab to ensure the quality of Fire Fighting equipment.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Professional Team</h2>
            <p class="core-value-text">
                We have a professional team to develop quality Fire Fighting products that align with the latest market trends and customer needs. Our team has hands-on experience.
            </p>
        </div>
        <div class="core-value-column">
            <h2 class="core-value-subtitle">Service Excellence</h2>
            <p class="core-value-text">
                We at Armor Fire focus on manufacturing quality Fire Fighting equipment. We prioritize long-lasting partnerships by consistently delivering products that safeguard lives & property effectively.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

    .custom-header {
        color: black !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 24px !important;
        text-align: left !important;
        margin-bottom: 0 !important;
        display: inline-block;
        border-bottom: 4px solid white !important;
    }

    .custom-title {
        color: #0D6C68 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 46px !important;
        font-weight: 600 !important;
        text-align: left !important;
        margin-top: 5px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Content ---
with st.container():
    st.markdown('<p class="custom-header">Markets We Serve</p><br>', unsafe_allow_html=True)

# Market icons
with st.container():
    st.markdown('<div class="cert-container">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    
    # Function to display image + styled text
    def market_item(img_url, label):
        st.image(img_url, width=100)
        st.markdown(
            f'<p style="text-align:left; font-size:16px; font-weight:600; font-family:Space Grotesk, sans-serif;">{label}</p>',
            unsafe_allow_html=True
        )

    with c1:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/residential.jpg", "Residential")
    with c2:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/commercial.jpg", "Commercial")
    with c3:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/industrial-units.jpg", "Industrial Units")
    with c4:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/goverment.jpg", "Government")
    with c5:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/hospital-nursing-homes.jpg", "Hospitals & Nursing Homes")
    with c6:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/educational-institutions.jpg", "Educational Institutions")
    with c7:
        market_item("https://www.armorfire.in/public/frontend/assets/images/icons/shopping-malls.jpg", "Shopping Malls")
    
    st.markdown('</div>', unsafe_allow_html=True)




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

