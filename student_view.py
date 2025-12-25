#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student Project Grader using Google Generative AI (Gemini)
"""

import sys
import os
import importlib.util

# Fix for Streamlit subprocess - manually load google.generativeai
def _load_google_generativeai():
    """Load google.generativeai module by finding its path directly."""
    google_genai_paths = [
        'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\lib\\site-packages\\google\\generativeai\\__init__.py',
        os.path.expanduser('~\\AppData\\Local\\Programs\\Python\\Python312\\lib\\site-packages\\google\\generativeai\\__init__.py'),
    ]
    
    for path in google_genai_paths:
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("google.generativeai", path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules['google.generativeai'] = module
                spec.loader.exec_module(module)
                return module
    
    # If file loading fails, add to sys.path and try normal import
    site_packages = 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\lib\\site-packages'
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)
    
    return __import__('google.generativeai', fromlist=[''])

# Try to load google.generativeai
try:
    genai = _load_google_generativeai()
except Exception as e:
    # Fallback: try direct import with sys.path modification
    site_packages = 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\lib\\site-packages'
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)
    import google.generativeai as genai

import streamlit as st
import PyPDF2
from docx import Document
import time
from datetime import datetime
from database import AnalysisDatabase
from report_generator import ReportGenerator
from email_notifier import EmailNotifier
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ========== PWA SETUP ==========
# Inject PWA manifest and service worker scripts
pwa_script = """
<script>
    // PWA Support
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/service-worker.js');
        });
    }
</script>

<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#667eea">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="AI Grader">
"""

st.set_page_config(
    page_title="ระบบตรวจโครงงาน AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add PWA support
st.markdown(pwa_script, unsafe_allow_html=True)

# ========== K-MINIMAL DESIGN SYSTEM ==========
# Import Prompt font from Google Fonts
google_fonts = """
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""
st.markdown(google_fonts, unsafe_allow_html=True)

# ========== LOGIN SYSTEM ==========
# ตั้งค่า Streamlit page config ก่อน
st.set_page_config(page_title="ระบบตรวจโครงงาน AI", page_icon="🎓", layout="wide")

# ตั้งค่า credentials สำหรับล็อกอิน (อาจารย์ และ นักเรียน)
ALL_CREDENTIALS = {
    # อาจารย์
    "teacher": {"password": "teacher123", "role": "teacher", "name": "อาจารย์"},
    "admin": {"password": "admin123", "role": "admin", "name": "ผู้ดูแลระบบ"},
    # นักเรียน
    "student1": {"password": "student123", "role": "student", "name": "นักเรียน 1"},
    "student2": {"password": "student123", "role": "student", "name": "นักเรียน 2"},
    "student3": {"password": "student123", "role": "student", "name": "นักเรียน 3"},
}

# ฟังก์ชันสำหรับ Login
def login_page():
    """แสดงหน้า login"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; color: #D4A5C8; font-family: Prompt, sans-serif;'>🔐 ระบบตรวจโครงงาน AI</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #B8879F; font-family: Prompt, sans-serif;'>Teacher & Student Mode</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Input fields
        username = st.text_input("👤 ชื่อผู้ใช้", placeholder="กรุณาใส่ชื่อผู้ใช้")
        password = st.text_input("🔑 รหัสผ่าน", type="password", placeholder="กรุณาใส่รหัสผ่าน")
        
        col_login, col_info = st.columns([1, 1])
        
        with col_login:
            if st.button("🔓 เข้าสู่ระบบ", use_container_width=True, type="primary"):
                # ตรวจสอบ credentials
                if username in ALL_CREDENTIALS and ALL_CREDENTIALS[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = ALL_CREDENTIALS[username]["role"]
                    st.session_state.display_name = ALL_CREDENTIALS[username]["name"]
                    st.success("✅ เข้าสู่ระบบสำเร็จ!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        
        with col_info:
            st.info("""💡 **สำหรับทดลอง:**
            
**อาจารย์:**
- Username: teacher
- Password: teacher123

**นักเรียน:**
- Username: student1
- Password: student123""")
        
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #B8879F; font-size: 12px; font-family: Prompt, sans-serif;'>© 2024 AI Project Grader System</p>", unsafe_allow_html=True)

# ========== MAIN APP ==========
# Load API Key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API Key is configured
if not API_KEY or API_KEY == "":
    st.error("❌ API Key ยังไม่ได้ตั้งค่า! โปรดเพิ่ม GOOGLE_API_KEY ใน .env file")
    st.stop()

# Initialize Database
db = AnalysisDatabase(os.getenv("DATABASE_FILE", "history.json"))

# ตั้งค่า AI
model = None
model_name = None
try:
    genai.configure(api_key=API_KEY)
    
    # List available models for debugging
    try:
        available_models = genai.list_models()
        available_names = [m.name.split('/')[-1] for m in available_models if 'generateContent' in m.supported_generation_methods]
    except:
        available_names = []
    
    # Try models in order of preference
    model_candidates = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
    
    for candidate in model_candidates:
        try:
            model = genai.GenerativeModel(candidate)
            model_name = candidate
            break
        except Exception:
            continue
    
    if model is None:
        # Try any available model
        if available_names:
            model = genai.GenerativeModel(available_names[0])
            model_name = available_names[0]
        else:
            raise Exception("ไม่พบ Model ที่ใช้ได้")
            
except Exception as e:
    st.error(f"❌ เชื่อมต่อ AI ไม่ได้: {e}")
    if available_names:
        st.info(f"💡 Models ที่พบ: {', '.join(available_names)}")
    model = None

# ========== CUSTOM CSS STYLING - K-MINIMAL DESIGN ==========
# K-Minimal Color Palette:
# Primary: #E8B4D4 (Pastel Pink)
# Secondary: #D4A5C8 (Darker Pastel Pink)
# Accent: #F0D9E8 (Light Pastel Pink)
# Neutral: #F5F5F5 (Off-white)

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

/* Global font settings */
* {
    font-family: 'Prompt', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Prompt', sans-serif !important;
}

/* Main background gradient - K-Minimal Pastel Pink */
body {
    background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%);
    color: #333;
    font-family: 'Prompt', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F5E8F0 100%);
    border-right: 2px solid #E8B4D4;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 20px;
}

/* Header and title styling */
h1, h2, h3 {
    color: #D4A5C8 !important;
    font-family: 'Prompt', sans-serif !important;
    font-weight: 600 !important;
}

h1 {
    color: #B8879F !important;
    margin-bottom: 20px;
}

/* Button styling - K-Minimal */
.stButton > button {
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    border: none !important;
    font-family: 'Prompt', sans-serif !important;
    box-shadow: 0 4px 15px rgba(232, 180, 212, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* Primary button (type="primary") */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #D4A5C8 0%, #B8879F 100%) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #E8B4D4 0%, #F0D9E8 100%) !important;
    color: #B8879F !important;
    border: 2px solid #D4A5C8 !important;
}

/* Metric styling */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(232, 180, 212, 0.2);
    border: 2px solid #F0D9E8;
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.3);
    border-color: #E8B4D4;
}

/* Expander styling */
[data-testid="stExpander"] {
    background: white;
    border-radius: 12px;
    border: 2px solid #F0D9E8;
    box-shadow: 0 2px 8px rgba(232, 180, 212, 0.1);
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

[data-testid="stExpander"]:hover {
    box-shadow: 0 4px 15px rgba(212, 165, 200, 0.2);
    border-color: #E8B4D4;
}

[data-testid="stExpander"] details > summary {
    color: #D4A5C8 !important;
    font-weight: 600 !important;
}

/* Info/Success/Error/Warning boxes */
[data-testid="stAlert"] {
    border-radius: 12px;
    border: 2px solid;
    padding: 15px;
    font-weight: 500;
    font-family: 'Prompt', sans-serif;
}

.stSuccess {
    background-color: #E6F9E6 !important;
    color: #2D5A2D !important;
    border-color: #B3E6B3 !important;
}

.stInfo {
    background-color: #E8F4F8 !important;
    color: #1A4D5C !important;
    border-color: #B3D9E6 !important;
}

.stWarning {
    background-color: #FFF8E6 !important;
    color: #8B6914 !important;
    border-color: #FFE699 !important;
}

.stError {
    background-color: #FFE8E8 !important;
    color: #8B2D2D !important;
    border-color: #FF9999 !important;
}

/* Data frame styling */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(232, 180, 212, 0.15);
    border: 1px solid #F0D9E8;
}

/* Tab styling - K-Minimal */
button[data-baseweb="tab"] {
    color: #B8879F !important;
    font-weight: 600 !important;
    border-radius: 12px 12px 0 0 !important;
    transition: all 0.3s ease !important;
    font-family: 'Prompt', sans-serif !important;
}

button[data-baseweb="tab"]:hover {
    background-color: rgba(232, 180, 212, 0.15) !important;
    color: #D4A5C8 !important;
}

button[aria-selected="true"][data-baseweb="tab"] {
    color: white !important;
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
    border-bottom: 3px solid #D4A5C8 !important;
}

/* Text input styling */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 2px solid #F0D9E8 !important;
    padding: 10px 15px !important;
    transition: all 0.3s ease !important;
    background-color: white !important;
    font-family: 'Prompt', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: #E8B4D4 !important;
    box-shadow: 0 0 10px rgba(232, 180, 212, 0.4) !important;
}

/* Select box styling */
.stSelectbox > div > div > div {
    border-radius: 10px !important;
    border: 2px solid #F0D9E8 !important;
    background-color: white !important;
}

.stSelectbox > div > div > div:focus {
    border-color: #E8B4D4 !important;
}

/* Divider styling */
hr {
    border: 0;
    height: 2px;
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
    margin: 20px 0;
}

/* Animation for status messages */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stAlert"] {
    animation: slideIn 0.3s ease;
}

/* Container styling */
[data-testid="stForm"] {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(232, 180, 212, 0.1);
    border: 1px solid #F0D9E8;
}

/* Column spacing */
[data-testid="stColumn"] {
    padding: 10px;
}

/* Download button styling */
a {
    color: #D4A5C8 !important;
    text-decoration: none;
    transition: all 0.3s ease;
}

a:hover {
    color: #B8879F !important;
    text-decoration: underline;
}

/* Progress bar styling */
.stProgress > div > div {
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
}

/* Checkbox and radio buttons */
.stCheckbox > label > span {
    font-family: 'Prompt', sans-serif !important;
}

.stRadio > label > span {
    font-family: 'Prompt', sans-serif !important;
}

/* Chart container */
[data-testid="stVegaLiteChart"] {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(232, 180, 212, 0.1);
}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize Email Notifier
email_notifier = EmailNotifier()

# --- 2. ฟังก์ชันช่วยอ่านไฟล์ (Helper Functions) ---
def read_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except:
        return ""

def read_docx(file):
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except:
        return ""

# ========== CHECK LOGIN STATUS ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ========== MAIN APP CONTENT (After Login) ==========

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("ห้องตรวจงาน")
    
    # แสดงข้อมูลผู้ใช้
    user_role_display = f"👨‍🎓 {st.session_state.display_name}" if st.session_state.role == "student" else f"👨‍🏫 {st.session_state.display_name}"
    st.success(f"✅ เข้าสู่ระบบแล้ว: **{user_role_display}**\n\n**ID:** {st.session_state.username}")
    
    st.info("💡 ระบบนี้ใช้ AI (Gemini) ในการอ่านเนื้อหาและวิเคราะห์ความเชื่อมโยง")
    st.divider()
    st.write("สถานะระบบ: 🟢 ออนไลน์")
    
    # Admin Panel Link (only for admin)
    if st.session_state.role == "admin":
        st.divider()
        st.markdown("### ⚙️ Admin Tools")
        if st.button("🔐 Admin Panel", use_container_width=True, type="primary"):
            st.info("💡 เปิด Admin Panel ในแท็บใหม่")
            st.write("```bash\nstreamlit run admin_panel.py\n```")
    
    # ปุ่ม Logout
    st.divider()
    if st.button("🚪 ออกจากระบบ", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.display_name = None
        st.success("ออกจากระบบสำเร็จ")
        st.rerun()

# --- Main Content with Tabs ---
st.title("🎓 ระบบตรวจความสอดคล้องโครงงาน (Logical Consistency)")
st.markdown("---")

# สร้าง tabs
tab1, tab2, tab3, tab4 = st.tabs(["📂 วิเคราะห์โครงงาน", "📜 ประวัติการวิเคราะห์", "📊 สถิติและรายงาน", "📈 กราฟและแผนภูมิ"])

# ========== TAB 1: ANALYSIS ==========
with tab1:
    st.header("📂 อัปโหลดและวิเคราะห์โครงงาน")
    st.markdown("---")
    
    # Upload Zone
    col_up, col_info = st.columns([2, 1])

    with col_up:
        uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์โครงงาน (PDF หรือ Word)", type=['pdf', 'docx'], key="file_uploader_tab1")

    with col_info:
        st.success("📝 **สิ่งที่ AI จะตรวจ:**")
        st.write("1. หา 'วัตถุประสงค์' ในไฟล์")
        st.write("2. หา 'สรุปผล' ในไฟล์")
        st.write("3. วิเคราะห์ว่าสอดคล้องกันหรือไม่")

    # --- ส่วนประมวลผล ---
    if uploaded_file is not None:
        
        # ปุ่มกดเริ่ม
        if st.button("🚀 เริ่มวิเคราะห์ด้วย AI", type="primary", key="analyze_btn_tab1"):
            
            # Check if model is available
            if model is None:
                st.error("❌ ไม่สามารถเชื่อมต่อ AI Model ได้ โปรดตรวจสอบ API Key")
                st.stop()
            
            # 1. อ่านไฟล์
            with st.status("🤖 AI กำลังทำงาน...", expanded=True) as status:
                st.write("📖 กำลังอ่านไฟล์...")
                
                if uploaded_file.name.endswith('.pdf'):
                    content_text = read_pdf(uploaded_file)
                else:
                    content_text = read_docx(uploaded_file)
                
                # เช็คว่าอ่านเจอไหม
                if len(content_text) < 100:
                    status.update(label="❌ อ่านไฟล์ไม่ได้ หรือไฟล์สั้นเกินไป", state="error")
                    st.stop()
                    
                st.write(f"✅ อ่านไฟล์สำเร็จ ({len(content_text)} ตัวอักษร)")
                time.sleep(1)
                
                # 2. ส่งให้ AI วิเคราะห์ (Prompt ขั้นเทพ)
                st.write("🧠 กำลังวิเคราะห์ตรรกะ (Logical Consistency)...")
                
                prompt = f"""
                Role: คุณคือครูที่ปรึกษาโครงงานผู้เชี่ยวชาญ
                Task: วิเคราะห์ "ความสอดคล้อง" ของโครงงานจากข้อความที่แนบมานี้
                
                Text Content:
                {content_text[:30000]}  (ตัดมาบางส่วนเพื่อไม่ให้เกินโควต้า)
                
                คำสั่ง:
                1. ค้นหา "วัตถุประสงค์" และ "สรุปผลการดำเนินงาน/อภิปรายผล" จากข้อความ
                2. เปรียบเทียบว่า สรุปผล ตอบโจทย์ วัตถุประสงค์ ครบทุกข้อไหม?
                3. ตรวจสอบจุดสำคัญ: ถ้าวัตถุประสงค์มีเรื่อง "ความพึงพอใจ" หรือ "ประสิทธิภาพ" ในสรุปผลมี "ตัวเลข/ค่าสถิติ" ไหม?
                
                Output Format (ตอบเป็น Markdown ภาษาไทย):
                ## 📊 ผลการวิเคราะห์ความสอดคล้อง
                
                **1. วัตถุประสงค์ที่พบ:**
                (ลิสต์วัตถุประสงค์ที่ AI จับใจความได้)
                
                **2. การตรวจสอบรายข้อ:**
                - 🎯 **ข้อ 1:** [ผ่าน/ไม่ผ่าน] เพราะ...
                - 🎯 **ข้อ 2:** [ผ่าน/ไม่ผ่าน] เพราะ...
                
                **3. ข้อแนะนำเพิ่มเติม:**
                (แนะนำจุดที่ควรแก้)
                """
                
                try:
                    response = model.generate_content(prompt)
                    status.update(label="✅ วิเคราะห์เสร็จสิ้น!", state="complete", expanded=False)
                    
                    # บันทึกผลลัพธ์ลงฐานข้อมูล
                    db.save_analysis(
                        username=st.session_state.username,
                        file_name=uploaded_file.name,
                        analysis_result=response.text
                    )
                    
                    st.success("✅ บันทึกผลการวิเคราะห์สำเร็จ!")
                    
                    # ส่งอีเมลแจ้งเตือน (ถ้ามีการตั้งค่า)
                    if email_notifier.is_configured:
                        # ตัวอย่าง: ส่งไปยังอีเมลนักเรียน
                        # email_notifier.send_analysis_notification(
                        #     recipient_email=student_email,
                        #     username=st.session_state.username,
                        #     file_name=uploaded_file.name,
                        #     analysis_result=response.text
                        # )
                        st.info("📧 ข้อมูลการวิเคราะห์จะถูกส่งไปยังอีเมลของคุณ (ถ้ามีการตั้งค่า)")
                    
                    # แสดงผลลัพธ์
                    st.divider()
                    st.markdown(response.text)
                    
                except Exception as e:
                    status.update(label="❌ เกิดข้อผิดพลาด", state="error")
                    error_msg = str(e)
                    st.error(f"❌ ข้อผิดพลาด API: {error_msg}")
                    
                    # Provide helpful suggestions
                    if "404" in error_msg or "not found" in error_msg.lower():
                        st.info(f"💡 Model ที่ใช้: {model_name}\n\nลองตรวจสอบ:\n1. API Key ถูกต้องหรือไม่\n2. Model นี้ใช้ได้กับ API Key นี้หรือไม่")
                    elif "quota" in error_msg.lower():
                        st.warning("⚠️ เกิน Quota การใช้งาน API โปรดรอสักครู่แล้วลองใหม่")
                    elif "key" in error_msg.lower():
                        st.error("❌ API Key ไม่ถูกต้อง โปรดตรวจสอบ")


# ========== TAB 2: HISTORY ==========
with tab2:
    st.header("📜 ประวัติการวิเคราะห์")
    st.markdown("---")
    
    # ดึงประวัติของผู้ใช้
    history = db.get_user_history(st.session_state.username)
    
    if not history:
        st.info("📭 ยังไม่มีประวัติการวิเคราะห์")
    else:
        st.success(f"✅ พบประวัติทั้งหมด {len(history)} รายการ")
        
        # Search/Filter
        col_search, col_sort = st.columns([2, 1])
        with col_search:
            search_term = st.text_input("🔍 ค้นหาตามชื่อไฟล์", placeholder="ใส่ชื่อไฟล์ที่ต้องการ...")
        with col_sort:
            sort_by = st.selectbox("เรียงลำดับตาม", ["ล่าสุด", "เก่าสุด"])
        
        # Filter history
        filtered_history = history
        if search_term:
            filtered_history = [h for h in history if search_term.lower() in h['file_name'].lower()]
        
        if sort_by == "เก่าสุด":
            filtered_history = sorted(filtered_history, key=lambda x: x['timestamp'])
        
        st.divider()
        
        # Download Summary Report Button
        if st.button("📥 ดาวน์โหลดรายงานสรุป (Word)", type="primary", key="download_summary"):
            try:
                gen = ReportGenerator()
                doc_buffer = gen.generate_summary_report(st.session_state.username, history)
                st.download_button(
                    label="💾 ดาวน์โหลด (Word Document)",
                    data=doc_buffer.getvalue(),
                    file_name=f"รายงานสรุป_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="summary_download"
                )
                st.success("✅ พร้อมสำหรับดาวน์โหลด!")
            except Exception as e:
                st.error(f"❌ สร้างรายงานไม่สำเร็จ: {e}")
        
        st.divider()
        
        # Display history items
        if not filtered_history:
            st.warning("❌ ไม่พบผลการค้นหา")
        else:
            for idx, entry in enumerate(filtered_history):
                st.markdown(f"#### 📄 {entry['file_name']} (ID: {entry['id']})")
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**📅 วันเวลา:** {entry['timestamp']}")
                        st.write(f"**📊 ขนาด:** {entry['file_size_chars']} ตัวอักษร")
                    
                    with col2:
                        st.write("")  # spacing
                        if st.button("👁️ ดูรายละเอียด", key=f"view_{entry['id']}"):
                            st.session_state[f"expanded_{entry['id']}"] = True
                    
                    with col3:
                        st.write("")  # spacing
                        # Download individual report button
                        try:
                            gen = ReportGenerator()
                            doc_buffer = gen.generate_word_report(
                                username=st.session_state.username,
                                file_name=entry['file_name'],
                                analysis_result=entry['result'],
                                timestamp=entry['timestamp']
                            )
                            st.download_button(
                                label="📥 ดาวน์โหลด",
                                data=doc_buffer.getvalue(),
                                file_name=gen.get_word_filename(entry['file_name'], st.session_state.username),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key=f"download_{entry['id']}"
                            )
                        except Exception as e:
                            st.error(f"❌ {e}")
                    
                    with col4:
                        st.write("")  # spacing
                        # PDF Download button
                        try:
                            gen = ReportGenerator()
                            pdf_buffer = gen.generate_pdf_report(
                                username=st.session_state.username,
                                file_name=entry['file_name'],
                                analysis_result=entry['result'],
                                timestamp=entry['timestamp']
                            )
                            st.download_button(
                                label="📄 PDF",
                                data=pdf_buffer.getvalue(),
                                file_name=gen.get_pdf_filename(entry['file_name'], st.session_state.username),
                                mime="application/pdf",
                                key=f"download_pdf_{entry['id']}"
                            )
                        except Exception as e:
                            st.error(f"❌ {e}")
                    
                    # Delete button
                    col_delete = st.columns([3, 1])[1]
                    with col_delete:
                        if st.button("🗑️ ลบ", key=f"delete_{entry['id']}", help="ลบการวิเคราะห์นี้"):
                            if db.delete_analysis(st.session_state.username, entry['id']):
                                st.success("✅ ลบสำเร็จ!")
                                st.rerun()
                            else:
                                st.error("❌ ลบไม่สำเร็จ")
                    
                    st.markdown("---")
                    st.markdown("**📋 ผลการวิเคราะห์:**")
                    st.markdown(entry['result'])


# ========== TAB 3: STATISTICS ==========
with tab3:
    st.header("📊 สถิติและรายงาน")
    st.markdown("---")
    
    # ดึงสถิติ
    stats = db.get_statistics(st.session_state.username)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📈 ทั้งหมด",
            value=f"{stats['total_analyses']} ครั้ง",
            help="จำนวนการวิเคราะห์ทั้งหมด"
        )
    
    with col2:
        st.metric(
            label="📅 ครั้งล่าสุด",
            value=stats['last_analysis_date'][:10] if stats['last_analysis_date'] != "ยังไม่มีการวิเคราะห์" else "ยังไม่มี",
            help="วันที่ทำการวิเคราะห์ครั้งล่าสุด"
        )
    
    with col3:
        st.metric(
            label="📄 ขนาดเฉลี่ย",
            value=f"{stats['avg_file_size']} ตัวอักษร",
            help="ขนาดไฟล์เฉลี่ย"
        )
    
    st.divider()
    
    # Admin-only statistics
    if st.session_state.role == "admin":
        st.info("👨‍💼 **สถิติระบบสำหรับผู้ดูแลระบบ**")
        
        all_stats = db.get_all_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="👥 จำนวนผู้ใช้ทั้งหมด",
                value=all_stats['total_users']
            )
        with col2:
            st.metric(
                label="📊 จำนวนการวิเคราะห์ทั้งหมด",
                value=all_stats['total_analyses']
            )
        
        st.markdown("---")
        st.subheader("📋 รายงานแบบละเอียด")
        
        if all_stats['users']:
            stats_df = []
            for user, count in all_stats['users'].items():
                stats_df.append({
                    "ชื่อผู้ใช้": user,
                    "จำนวนการวิเคราะห์": count
                })
            
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        else:
            st.info("ยังไม่มีข้อมูล")
        
        # Delete all history option
        st.divider()
        st.warning("⚠️ **ตัวเลือกอันตราย**")
        if st.checkbox("ฉันต้องการลบประวัติทั้งหมดของผู้ใช้"):
            selected_user = st.selectbox("เลือกผู้ใช้", list(all_stats['users'].keys()) if all_stats['users'] else [])
            if st.button("🔥 ลบประวัติทั้งหมด", type="secondary"):
                if db.delete_all_user_history(selected_user):
                    st.success(f"✅ ลบประวัติของ {selected_user} สำเร็จ!")
                    st.rerun()
                else:
                    st.error("❌ ลบไม่สำเร็จ")


# ========== TAB 4: CHARTS & GRAPHS ==========
with tab4:
    st.header("📈 กราฟและแผนภูมิ")
    st.markdown("---")
    
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    import plotly.express as px
    from collections import Counter
    
    # ดึงข้อมูลประวัติ
    history = db.get_user_history(st.session_state.username)
    
    if not history:
        st.info("📭 ยังไม่มีข้อมูลสำหรับสร้างกราฟ")
    else:
        # Chart 1: Analyses Over Time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 จำนวนการวิเคราะห์ตามเวลา")
            
            # Extract dates
            dates = [entry['timestamp'][:10] for entry in history]
            date_counts = Counter(dates)
            sorted_dates = sorted(date_counts.keys())
            counts = [date_counts[d] for d in sorted_dates]
            
            # Create line chart
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=sorted_dates,
                y=counts,
                mode='lines+markers',
                name='จำนวนการวิเคราะห์',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10, color='#764ba2')
            ))
            
            fig_time.update_layout(
                xaxis_title="วันที่",
                yaxis_title="จำนวนการวิเคราะห์",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            st.subheader("📊 ประเภทไฟล์ที่วิเคราะห์")
            
            # Count file types
            file_extensions = [entry['file_name'].split('.')[-1] for entry in history]
            ext_counts = Counter(file_extensions)
            
            # Create pie chart
            fig_types = go.Figure(data=[go.Pie(
                labels=[f".{ext}" for ext in ext_counts.keys()],
                values=list(ext_counts.values()),
                marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
            )])
            
            fig_types.update_layout(
                title="ประเภทไฟล์",
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_types, use_container_width=True)
        
        # Chart 3: File Size Distribution
        st.subheader("📈 การกระจายตัวของขนาดไฟล์")
        
        file_sizes = [entry['file_size_chars'] for entry in history]
        
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=file_sizes,
            nbinsx=15,
            name='จำนวนไฟล์',
            marker=dict(color='#667eea', opacity=0.7),
            hovertemplate='ขนาด: %{x} ตัวอักษร<br>จำนวน: %{y}<extra></extra>'
        ))
        
        fig_dist.update_layout(
            xaxis_title="ขนาดไฟล์ (ตัวอักษร)",
            yaxis_title="จำนวนไฟล์",
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Statistics Summary
        st.divider()
        st.subheader("📊 สรุปสถิติ")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("รวมการวิเคราะห์", len(history))
        
        with col2:
            st.metric("วันที่วิเคราะห์", len(set(dates)))
        
        with col3:
            avg_size = sum(file_sizes) // len(file_sizes)
            st.metric("ขนาดเฉลี่ย", f"{avg_size:,} ตัวอักษร")
        
        with col4:
            max_size = max(file_sizes)
            st.metric("ขนาดมากสุด", f"{max_size:,} ตัวอักษร")
        
        # Top 5 files
        st.subheader("🔝 ไฟล์ที่มีขนาดใหญ่สุด")
        top_files = sorted(history, key=lambda x: x['file_size_chars'], reverse=True)[:5]
        
        top_data = []
        for idx, entry in enumerate(top_files, 1):
            top_data.append({
                "ลำดับ": idx,
                "ชื่อไฟล์": entry['file_name'],
                "ขนาด": f"{entry['file_size_chars']:,} ตัวอักษร",
                "วันเวลา": entry['timestamp'][:10]
            })
        
        st.dataframe(top_data, use_container_width=True, hide_index=True)
        
        if history:
            st.subheader("📁 ไฟล์ที่วิเคราะห์ล่าสุด")
            
            recent_files = []
            for entry in history[:5]:
                recent_files.append({
                    "ชื่อไฟล์": entry['file_name'],
                    "วันเวลา": entry['timestamp'][:10],
                    "ขนาด": f"{entry['file_size_chars']} ตัวอักษร"
                })
            
            if recent_files:
                st.dataframe(recent_files, use_container_width=True, hide_index=True)
        else:
            st.info("📭 ยังไม่มีประวัติการวิเคราะห์")