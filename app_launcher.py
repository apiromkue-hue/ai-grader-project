#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application Launcher
Choose between Student Interface and Admin Panel
This is the HOME page for Streamlit Multi-Page App
"""

import streamlit as st
import subprocess
import os

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="ระบบตรวจโครงงาน AI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely using CSS injection
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== PROMPT FONT INTEGRATION ==========
google_fonts = """
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""
st.markdown(google_fonts, unsafe_allow_html=True)

# CSS to hide keyboard icons completely - ULTIMATE VERSION
hide_icons_css = """
<style>
/* ซ่อน header toolbar ทั้งหมด */
header[data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
}

/* ซ่อนปุ่ม sidebar collapse อย่างสมบูรณ์ */
[data-testid="collapsedControl"],
button[kind="header"],
[data-testid="baseButton-header"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
    left: -9999px !important;
}

/* ซ่อน sidebar navigation ทั้งหมด - ULTIMATE */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavLink"],
section[data-testid="stSidebar"] nav,
section[data-testid="stSidebar"] > div:first-child,
section[data-testid="stSidebar"] ul,
section[data-testid="stSidebar"] li {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* บังคับซ่อน sidebar ทั้งหมด */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* ซ่อน Material Icons ทั้งหมด */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined {
    display: none !important;
    font-size: 0 !important;
    visibility: hidden !important;
}

</style>

<script>
function removeSidebar() {
    // ลบ sidebar navigation
    const sidebarNav = document.querySelectorAll('[data-testid="stSidebarNav"]');
    sidebarNav.forEach(el => el.remove());
    
    const sidebarNavItems = document.querySelectorAll('[data-testid="stSidebarNavItems"]');
    sidebarNavItems.forEach(el => el.remove());
    
    // ลบทุก navigation link
    const navLinks = document.querySelectorAll('section[data-testid="stSidebar"] a');
    navLinks.forEach(el => el.remove());
    
    // ลบทุก list item ใน sidebar
    const sidebarLists = document.querySelectorAll('section[data-testid="stSidebar"] ul, section[data-testid="stSidebar"] li');
    sidebarLists.forEach(el => el.remove());
    
    // ลบ keyboard icon
    const keyboardIcons = document.querySelectorAll('.material-icons, .material-icons-outlined');
    keyboardIcons.forEach(el => {
        if (el.textContent.includes('keyboard')) {
            el.remove();
        }
    });
    
    // ลบทุก element ที่มีคำว่า keyboard
    document.querySelectorAll('*').forEach(el => {
        if (el.textContent && el.textContent.trim().includes('keyboard_')) {
            el.style.display = 'none';
        }
    });
}

// รันทันที
removeSidebar();

// รันซ้ำทุก 0.5 วินาที
setTimeout(removeSidebar, 500);
setTimeout(removeSidebar, 1000);
setTimeout(removeSidebar, 2000);

// ตรวจสอบการเปลี่ยนแปลง DOM
const observer = new MutationObserver(removeSidebar);
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""

st.markdown(hide_icons_css, unsafe_allow_html=True)

# ========== K-MINIMAL DESIGN SYSTEM ==========
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Prompt', sans-serif !important;
}

body {
    background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%);
    color: #333;
    font-family: 'Prompt', sans-serif;
}

h1 {
    color: #B8879F !important;
    font-weight: 600 !important;
    text-align: center;
    margin-bottom: 30px;
}

h2 {
    color: #D4A5C8 !important;
    font-weight: 600 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 15px 30px !important;
    transition: all 0.3s ease !important;
    border: none !important;
    font-family: 'Prompt', sans-serif !important;
    box-shadow: 0 4px 15px rgba(232, 180, 212, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.4) !important;
}

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

.card-container {
    background: white;
    border: 2px solid #F0D9E8;
    border-radius: 15px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 4px 15px rgba(232, 180, 212, 0.2);
    transition: all 0.3s ease;
}

.card-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.3);
    border-color: #E8B4D4;
}

.feature-list {
    list-style: none;
    padding-left: 0;
}

.feature-list li {
    padding: 10px 0;
    padding-left: 30px;
    position: relative;
    color: #333;
}

.feature-list li:before {
    content: "✅";
    position: absolute;
    left: 0;
    color: #D4A5C8;
    font-weight: bold;
}

hr {
    border: 0;
    height: 2px;
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
    margin: 30px 0;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== MAIN CONTENT ==========
st.markdown("<h1>🎓 ระบบตรวจโครงงาน AI</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #B8879F;'>ระบบตรวจโครงงานด้วย AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 14px;'>ยินดีต้อนรับสู่ระบบตรวจโครงงานด้วยปัญญาประดิษฐ์</p>", unsafe_allow_html=True)

st.markdown("---")

# Choose interface
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='card-container'>
    <h2 style='text-align: center; color: #D4A5C8;'>👨‍🎓 หน้าสำหรับนักเรียนและอาจารย์</h2>
    <p style='text-align: center; color: #666;'>อัปโหลดโครงงานและรับผลการวิเคราะห์จาก AI</p>
    
    <ul class='feature-list'>
    <li>📂 อัปโหลดและวิเคราะห์โครงงาน</li>
    <li>📜 ดูประวัติการวิเคราะห์</li>
    <li>📊 ดูสถิติและรายงาน</li>
    <li>📈 กราฟและแผนภูมิ</li>
    <li>📥 ดาวน์โหลดรายงาน PDF/Word</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 เข้าสู่หน้านักเรียนและอาจารย์", use_container_width=True, type="primary"):
        st.switch_page("pages/1_student_interface.py")

with col2:
    st.markdown("""
    <div class='card-container'>
    <h2 style='text-align: center; color: #D4A5C8;'>⚙️ หน้าสำหรับผู้ดูแลระบบ</h2>
    <p style='text-align: center; color: #666;'>จัดการผู้ใช้และดูสถิติระบบทั้งหมด</p>
    
    <ul class='feature-list'>
    <li>👥 จัดการผู้ใช้ (เพิ่ม/ลบ/แก้ไข)</li>
    <li>📊 ดูสถิติระบบทั้งหมด</li>
    <li>📜 ดูประวัติการใช้งาน</li>
    <li>🔧 ตั้งค่าระบบและความปลอดภัย</li>
    <li>📋 สร้างรายงาน (PDF/Excel)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔐 เข้าสู่หน้าผู้ดูแลระบบ", use_container_width=True, type="primary"):
        st.switch_page("pages/2_admin_panel.py")

st.markdown("---")

# System status
st.markdown("### 📊 สถานะระบบ")

col_status1, col_status2, col_status3, col_status4 = st.columns(4)

with col_status1:
    st.metric("🟢 Status", "Online", "OK")

with col_status2:
    st.metric("👥 Users", "4 Active", "100%")

with col_status3:
    st.metric("📊 Analyses", "200+", "+25")

with col_status4:
    st.metric("⏱️ Response", "2.5s", "Fast")

st.markdown("---")

# Quick Start Guide
st.markdown("### 🚀 คู่มือการใช้งานอย่างรวดเร็ว")

st.markdown("""
#### 📚 วิธีการใช้งาน

##### หน้าสำหรับนักเรียนและอาจารย์
1. คลิก "🚀 เข้าสู่หน้านักเรียนและอาจารย์"
2. เข้าสู่ระบบด้วยชื่อผู้ใช้และรหัสผ่าน
3. อัปโหลดไฟล์โครงงาน (PDF หรือ Word)
4. คลิก "🚀 เริ่มวิเคราะห์" เพื่อให้ AI วิเคราะห์
5. ดูผลลัพธ์และดาวน์โหลดรายงาน

##### หน้าสำหรับผู้ดูแลระบบ
1. คลิก "🔐 เข้าสู่หน้าผู้ดูแลระบบ"
2. เข้าสู่ระบบด้วย Admin Credentials
3. จัดการผู้ใช้, ดูสถิติ, ดูประวัติ
4. ตั้งค่าระบบและสร้างรายงาน

##### 🔑 Demo Credentials
- **Student**: username=student1, password=student123
- **Teacher**: username=teacher, password=teacher123
- **Admin**: username=admin, password=admin123
""")

st.markdown("---")

# Features Overview
st.markdown("### ✨ Key Features")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    #### 🤖 AI Analysis
    - Powered by Google Gemini
    - Automatic project analysis
    - Consistency checking
    - Smart recommendations
    """)

with feat_col2:
    st.markdown("""
    #### 📊 Analytics
    - Real-time statistics
    - User activity tracking
    - Performance metrics
    - Historical data
    """)

with feat_col3:
    st.markdown("""
    #### 🔒 Security
    - Role-based access
    - User management
    - Data backup
    - Audit logs
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #B8879F; font-size: 12px; margin-top: 50px;'>
<p>🎓 AI Project Grader System v1.0</p>
<p>K-Minimal Design | Prompt Font | ✨ Modern UI</p>
<p>© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
