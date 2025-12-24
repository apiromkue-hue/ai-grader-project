#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Home Page - ระบบตรวจโครงงานอัจฉริยะด้วย AI
Intelligent Project Grading System with Artificial Intelligence
"""

import streamlit as st

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="ระบบตรวจโครงงานอัจฉริยะด้วย AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== PROMPT FONT & K-MINIMAL DESIGN ==========
google_fonts = """
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""
st.markdown(google_fonts, unsafe_allow_html=True)

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Prompt', sans-serif !important;
}

body {
    background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%);
    min-height: 100vh;
    color: #333;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

h1, h2, h3 {
    color: #B8879F !important;
    font-family: 'Prompt', sans-serif !important;
    font-weight: 600 !important;

.hero-icon {
    font-size: 5rem;
    text-align: center;
    margin-bottom: 1rem;
    animation: bounce 2s infinite;
}

.content-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 3rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(212, 165, 200, 0.3);
    border: 2px solid rgba(232, 180, 212, 0.3);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-item {
    background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #F0D9E8;
    transition: all 0.3s ease;
    text-align: center;
}

.feature-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.3);
    border-color: #E8B4D4;
}

.steps-item {
    background: #F5E8F0;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
    border-radius: 10px;
    border-left: 4px solid #E8B4D4;
    font-size: 1.05rem;
}

.stButton > button {
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
    color: white !important;
    border-radius: 15px !important;
    font-weight: 600 !important;
    padding: 1.2rem 3rem !important;
    font-size: 1.3rem !important;
    transition: all 0.3s ease !important;
    border: none !important;
    font-family: 'Prompt', sans-serif !important;
    box-shadow: 0 6px 20px rgba(232, 180, 212, 0.4) !important;
    width: 100% !important;
    margin: 1rem 0 !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(212, 165, 200, 0.5) !important;
}

.info-box {
    background: #fff3cd;
    border: 2px solid #ffc107;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    color: #856404;
}

hr {
    border: 0;
    height: 2px;
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
    margin: 20px 0;
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-20px);
    }
}

footer {
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    background: linear-gradient(90deg, #B8879F 0%, #D4A5C8 100%);
    border-radius: 15px;
    color: white;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <svg width="180" height="180" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#E8B4D4;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#D4A5C8;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#B8879F;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#D4A5C8;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="100" cy="100" r="95" fill="url(#gradient1)" opacity="0.2"/>
        <rect x="50" y="40" width="80" height="100" rx="5" fill="url(#gradient1)" stroke="#B8879F" stroke-width="3"/>
        <line x1="60" y1="60" x2="110" y2="60" stroke="white" stroke-width="3" stroke-linecap="round"/>
        <line x1="60" y1="75" x2="120" y2="75" stroke="white" stroke-width="3" stroke-linecap="round"/>
        <line x1="60" y1="90" x2="115" y2="90" stroke="white" stroke-width="3" stroke-linecap="round"/>
        <line x1="60" y1="105" x2="105" y2="105" stroke="white" stroke-width="3" stroke-linecap="round"/>
        <circle cx="145" cy="130" r="35" fill="url(#gradient2)" opacity="0.9"/>
        <circle cx="135" cy="120" r="4" fill="white"/>
        <circle cx="155" cy="125" r="4" fill="white"/>
        <circle cx="145" cy="140" r="4" fill="white"/>
        <line x1="135" y1="120" x2="145" y2="140" stroke="white" stroke-width="2"/>
        <line x1="155" y1="125" x2="145" y2="140" stroke="white" stroke-width="2"/>
        <polyline points="125,115 135,125 155,105" fill="none" stroke="#4CAF50" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center;">ระบบตรวจโครงงานอัจฉริยะด้วย AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #D4A5C8; font-weight: 500;">Intelligent Project Grading System with Artificial Intelligence</p>', unsafe_allow_html=True)

st.markdown("---")

# ========== MAIN CONTENT ==========
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    # About System
    st.markdown("## 📋 เกี่ยวกับระบบ")
    st.markdown("""
    ระบบตรวจโครงงานอัจฉริยะด้วย AI เป็นเครื่องมือที่พัฒนาขึ้นเพื่อช่วยอาจารย์และนักเรียนในการประเมินและปรับปรุง
    คุณภาพของโครงงานวิทยาศาสตร์ โดยใช้เทคโนโลยี **Google Gemini AI** ในการวิเคราะห์เอกสารแบบ 
    **Semantic Analysis 3 ระดับ** ทำให้ได้ผลการประเมินที่ละเอียด ครบถ้วน และมีข้อเสนอแนะที่เป็นประโยชน์
    """)
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ ความสามารถของระบบ")
    
    # Row 1: 3 features
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 220px; transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📝</div>
            <h4 style="color: #B8879F; font-weight: 600; margin-bottom: 0.5rem;">ตรวจรูปแบบ</h4>
            <p style="color: #666; font-size: 0.95rem;">ตรวจสอบโครงสร้าง บรรณานุกรม และการจัดรูปแบบเอกสาร</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 220px; transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔗</div>
            <h4 style="color: #B8879F; font-weight: 600; margin-bottom: 0.5rem;">ตรวจความเชื่อมโยง</h4>
            <p style="color: #666; font-size: 0.95rem;">วิเคราะห์ความสอดคล้องของเนื้อหาและตรรกะการนำเสนอ</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 220px; transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">💡</div>
            <h4 style="color: #B8879F; font-weight: 600; margin-bottom: 0.5rem;">ข้อเสนอแนะ</h4>
            <p style="color: #666; font-size: 0.95rem;">ให้คำแนะนำเชิงเนื้อหาเพื่อปรับปรุงโครงงาน</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: 3 features
    col_f4, col_f5, col_f6 = st.columns(3)
    
    with col_f4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 220px; transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: #B8879F; font-weight: 600; margin-bottom: 0.5rem;">ระบบคะแนน</h4>
            <p style="color: #666; font-size: 0.95rem;">ประเมินคะแนนแบบรายละเอียดพร้อมคำอธิบาย</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f5:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 220px; transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📚</div>
            <h4 style="color: #B8879F; font-weight: 600; margin-bottom: 0.5rem;">ตรวจแบบเลือก</h4>
            <p style="color: #666; font-size: 0.95rem;">เลือกตรวจเฉพาะบทหรือตรวจทั้งโครงงาน</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f6:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 220px; transition: all 0.3s ease;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
            <h4 style="color: #B8879F; font-weight: 600; margin-bottom: 0.5rem;">ติดตามความคืบหน้า</h4>
            <p style="color: #666; font-size: 0.95rem;">ดูประวัติและสถิติการวิเคราะห์ทั้งหมด</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User Guide
    st.markdown("### 📖 คู่มือการใช้งานโดยย่อ")
    
    col_guide1, col_guide2 = st.columns(2)
    
    with col_guide1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 2rem; 
                    height: 100%; min-height: 400px;">
            <div style="text-align: center; margin-bottom: 1rem;">
                <span style="font-size: 3rem;">👨‍🎓</span>
                <h4 style="color: #B8879F; font-weight: 600; margin: 0.5rem 0;">สำหรับนักเรียนและครู</h4>
            </div>
            <div style="color: #666; text-align: left; line-height: 1.8;">
                <p><strong style="color: #B8879F;">1. เข้าสู่ระบบ:</strong> ใช้ username และ password ที่ได้รับจากผู้ดูแลระบบ</p>
                <p><strong style="color: #B8879F;">2. อัปโหลดไฟล์:</strong> เลือกไฟล์โครงงาน (PDF หรือ Word) ที่ต้องการตรวจ</p>
                <p><strong style="color: #B8879F;">3. เลือกบท:</strong> เลือกว่าต้องการตรวจเฉพาะบทใด หรือทั้งหมด 5 บท</p>
                <p><strong style="color: #B8879F;">4. รับผลการวิเคราะห์:</strong> รอ AI วิเคราะห์และแสดงผลคะแนนพร้อมข้อเสนอแนะ</p>
                <p><strong style="color: #B8879F;">5. ดูประวัติ:</strong> ตรวจสอบประวัติและสถิติการวิเคราะห์ทั้งหมด</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_guide2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%); 
                    border: 2px solid #F0D9E8; border-radius: 15px; padding: 2rem; 
                    height: 100%; min-height: 400px;">
            <div style="text-align: center; margin-bottom: 1rem;">
                <span style="font-size: 3rem;">👨‍💼</span>
                <h4 style="color: #B8879F; font-weight: 600; margin: 0.5rem 0;">สำหรับผู้ดูแลระบบ (Admin)</h4>
            </div>
            <div style="color: #666; text-align: left; line-height: 1.8;">
                <p><strong style="color: #B8879F;">1. เข้าสู่ระบบ:</strong> ใช้บัญชี Admin เพื่อเข้าถึงส่วนจัดการ</p>
                <p><strong style="color: #B8879F;">2. จัดการผู้ใช้:</strong> เพิ่ม/ลบ/แก้ไขข้อมูลผู้ใช้ในระบบ</p>
                <p><strong style="color: #B8879F;">3. ดูสถิติระบบ:</strong> ติดตามการใช้งานและประสิทธิภาพของระบบ</p>
                <p><strong style="color: #B8879F;">4. ตั้งค่าระบบ:</strong> กำหนดค่าต่างๆ เช่น API Key, ข้อความแจ้งเตือน</p>
                <p><strong style="color: #B8879F;">5. ดูรายงาน:</strong> สร้างและส่งออกรายงานการใช้งานระบบ</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info Box
    st.markdown("""
    <div class="info-box">
        <p>
            <span style="font-size: 1.5rem;">💡</span>
            <strong>เคล็ดลับ:</strong> ก่อนอัปโหลดโครงงาน ควรตรวจสอบให้แน่ใจว่าไฟล์มีความชัดเจนและอ่านได้ 
            เพื่อให้ AI สามารถวิเคราะห์ได้อย่างมีประสิทธิภาพสูงสุด
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Buttons
    st.markdown("### 🚀 เลือกส่วนที่ต้องการเข้าใช้งาน")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("👨‍🎓 เข้าสู่ระบบ นักเรียน/ครู", key="btn_student"):
            st.switch_page("pages/1_Student_Interface.py")
    
    with col_btn2:
        if st.button("👨‍💼 เข้าสู่ระบบ Admin", key="btn_admin"):
            st.switch_page("pages/2_Admin_Panel.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("---")

# จัดให้อยู่กึ่งกลาง
col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])

with col_footer2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin-top: 2rem; 
                background: linear-gradient(90deg, #B8879F 0%, #D4A5C8 100%); 
                border-radius: 15px; color: white;">
        <h3 style="color: white !important; margin-bottom: 1rem;">👩‍💻 ผู้พัฒนาระบบ</h3>
        <p style="font-size: 1.1rem; margin: 0.5rem 0;"><strong>นางอภิรมย์ กึกก้อง</strong></p>
        <p style="margin: 0.5rem 0;">ตำแหน่ง: <strong>ครู</strong> วิทยฐานะ <strong>ครูชำนาญการพิเศษ</strong></p>
        <div style="margin-top: 1rem; opacity: 0.95; font-size: 0.95rem; line-height: 1.8;">
            <p style="margin: 0.3rem 0;">โรงเรียนเตรียมอุดมศึกษาภาคใต้</p>
            <p style="margin: 0.3rem 0;">สำนักงานเขตพื้นที่การศึกษามัธยมศึกษานครศรีธรรมราช</p>
            <p style="margin: 0.3rem 0;">สำนักงานคณะกรรมการการศึกษาขั้นพื้นฐาน กระทรวงศึกษาธิการ</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
