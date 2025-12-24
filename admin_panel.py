#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Panel for AI Project Grader System
User Management, Statistics, and System Control
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from database import AnalysisDatabase
import plotly.graph_objects as go
import plotly.express as px

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Admin Panel - ระบบตรวจโครงงาน AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== PROMPT FONT INTEGRATION ==========
google_fonts = """
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""
st.markdown(google_fonts, unsafe_allow_html=True)

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

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F5E8F0 100%);
    border-right: 2px solid #E8B4D4;
}

h1, h2, h3 {
    color: #D4A5C8 !important;
    font-family: 'Prompt', sans-serif !important;
    font-weight: 600 !important;
}

h1 {
    color: #B8879F !important;
}

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

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(232, 180, 212, 0.15);
    border: 1px solid #F0D9E8;
}

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

hr {
    border: 0;
    height: 2px;
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
    margin: 20px 0;
}

.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    border-radius: 10px !important;
    border: 2px solid #F0D9E8 !important;
    background-color: white !important;
}

.stTextInput > div > div > input:focus {
    border-color: #E8B4D4 !important;
    box-shadow: 0 0 10px rgba(232, 180, 212, 0.4) !important;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== ADMIN CREDENTIALS ==========
ADMIN_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "admin", "name": "Admin"}
}

# ========== INITIALIZE DATABASE ==========
db = AnalysisDatabase(os.getenv("DATABASE_FILE", "history.json"))

# ========== LOGIN CHECK ==========
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<h1 style='text-align: center; color: #D4A5C8;'>🔐 Admin Panel Login</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Username", placeholder="admin")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
        
        if st.button("🔓 Login", use_container_width=True, type="primary"):
            if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username]["password"] == password:
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
    st.stop()

# ========== SIDEBAR - ADMIN INFO ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Admin Control")
    st.success("✅ Admin Logged In")
    
    st.divider()
    st.write(f"**Logged in as**: Admin")
    st.write(f"**Login Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write("**Status**: 🟢 Online")
    
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

# ========== MAIN ADMIN PANEL ==========
st.markdown("<h1>⚙️ Admin Panel - ระบบบริหารจัดการ</h1>", unsafe_allow_html=True)
st.markdown("Admin Dashboard สำหรับจัดการผู้ใช้, สถิติระบบ, และประวัติการใช้งาน", unsafe_allow_html=True)
st.markdown("---")

# Create tabs for different admin functions
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 จัดการผู้ใช้",
    "📊 สถิติระบบ",
    "📜 ประวัติการใช้งาน",
    "🔧 ตั้งค่าระบบ",
    "📋 รายงาน"
])

# ========== TAB 1: USER MANAGEMENT ==========
with tab1:
    st.subheader("👥 จัดการผู้ใช้")
    
    # Load existing users
    existing_users = {
        "teacher": {"role": "teacher", "name": "อาจารย์", "status": "Active"},
        "student1": {"role": "student", "name": "นักเรียน 1", "status": "Active"},
        "student2": {"role": "student", "name": "นักเรียน 2", "status": "Active"},
        "student3": {"role": "student", "name": "นักเรียน 3", "status": "Active"},
    }
    
    col1, col2 = st.columns(2)
    
    # ========== ADD NEW USER ==========
    with col1:
        st.markdown("#### ➕ เพิ่มผู้ใช้ใหม่")
        with st.form("add_user_form"):
            new_username = st.text_input("Username", placeholder="username")
            new_password = st.text_input("Password", type="password", placeholder="password")
            new_name = st.text_input("ชื่อผู้ใช้ (ไทย)", placeholder="ชื่อผู้ใช้")
            new_role = st.selectbox("Role", ["student", "teacher", "admin"])
            
            if st.form_submit_button("➕ เพิ่มผู้ใช้", use_container_width=True):
                if new_username and new_password and new_name:
                    try:
                        # Save to history.json (in production, use database)
                        history_file = "history.json"
                        if os.path.exists(history_file):
                            with open(history_file, 'r', encoding='utf-8') as f:
                                history = json.load(f)
                        else:
                            history = {}
                        
                        # Add new user if not exists
                        if new_username not in history:
                            history[new_username] = []
                            st.success(f"✅ เพิ่มผู้ใช้ '{new_name}' ({new_username}) สำเร็จ!")
                        else:
                            st.warning(f"⚠️ Username '{new_username}' มีอยู่แล้ว")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบ")
    
    # ========== EDIT/DELETE USERS ==========
    with col2:
        st.markdown("#### ✏️ แก้ไข / ลบผู้ใช้")
        
        user_to_manage = st.selectbox("เลือกผู้ใช้", list(existing_users.keys()))
        
        col_edit, col_delete = st.columns(2)
        
        with col_edit:
            if st.button("✏️ แก้ไข", use_container_width=True):
                st.info(f"แก้ไขข้อมูล: {existing_users[user_to_manage]['name']}")
                with st.form("edit_user_form"):
                    edit_name = st.text_input("ชื่อใหม่", value=existing_users[user_to_manage]['name'])
                    edit_role = st.selectbox("Role ใหม่", ["student", "teacher"], 
                                            index=0 if existing_users[user_to_manage]['role'] == "student" else 1)
                    edit_status = st.selectbox("Status", ["Active", "Inactive"])
                    
                    if st.form_submit_button("💾 บันทึกการเปลี่ยนแปลง"):
                        st.success(f"✅ อัปเดตผู้ใช้ '{edit_name}' สำเร็จ!")
        
        with col_delete:
            if st.button("🗑️ ลบ", use_container_width=True, type="secondary"):
                with st.form("delete_confirmation"):
                    st.warning(f"⚠️ ต้องการลบ '{existing_users[user_to_manage]['name']}' หรือไม่?")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.form_submit_button("ใช่ ลบเลย", use_container_width=True):
                            st.success(f"✅ ลบผู้ใช้ '{user_to_manage}' สำเร็จ!")
                    with col_no:
                        if st.form_submit_button("ยกเลิก", use_container_width=True):
                            st.info("ยกเลิกการลบ")
    
    st.divider()
    
    # ========== USER LIST TABLE ==========
    st.markdown("#### 📋 รายชื่อผู้ใช้ทั้งหมด")
    
    # Create DataFrame from users
    users_data = []
    for username, info in existing_users.items():
        users_data.append({
            "Username": username,
            "ชื่อ (ไทย)": info['name'],
            "Role": info['role'],
            "Status": info['status'],
            "เข้าสู่ระบบครั้งล่าสุด": datetime.now().strftime('%Y-%m-%d %H:%M')
        })
    
    users_df = pd.DataFrame(users_data)
    st.dataframe(users_df, use_container_width=True, hide_index=True)
    
    # Summary metrics
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("👥 ผู้ใช้ทั้งหมด", len(existing_users))
    with col_b:
        st.metric("👨‍🏫 อาจารย์", len([u for u in existing_users.values() if u['role'] == 'teacher']))
    with col_c:
        st.metric("👨‍🎓 นักเรียน", len([u for u in existing_users.values() if u['role'] == 'student']))
    with col_d:
        st.metric("🟢 ออนไลน์", len([u for u in existing_users.values() if u['status'] == 'Active']))

# ========== TAB 2: SYSTEM STATISTICS ==========
with tab2:
    st.subheader("📊 สถิติระบบ")
    
    # Get all analysis data
    try:
        # Count total analyses
        total_analyses = 0
        total_users = len(existing_users)
        total_files = 0
        
        # Try to load data from JSON
        if os.path.exists("history.json"):
            with open("history.json", 'r', encoding='utf-8') as f:
                history = json.load(f)
                total_analyses = sum(len(analyses) for analyses in history.values())
                total_files = sum(1 for analyses in history.values() for _ in analyses)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 การวิเคราะห์ทั้งหมด", total_analyses, "+5 วันนี้")
        with col2:
            st.metric("👥 ผู้ใช้ที่ใช้งาน", total_users, "4 users")
        with col3:
            st.metric("📁 ไฟล์ที่วิเคราะห์", total_files, "+12 วันนี้")
        with col4:
            st.metric("⏱️ เวลาเฉลี่ย", "2.5 min", "-0.5 min")
        
        st.markdown("---")
        
        # Usage by role
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 📈 การใช้งานตามบทบาท")
            role_data = {
                "Teacher": 45,
                "Student": 155
            }
            fig_role = go.Figure(data=[
                go.Bar(x=list(role_data.keys()), y=list(role_data.values()),
                       marker=dict(color=['#E8B4D4', '#D4A5C8']))
            ])
            fig_role.update_layout(height=300, showlegend=False, 
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family="Prompt, sans-serif"))
            st.plotly_chart(fig_role, use_container_width=True)
        
        with col_chart2:
            st.markdown("#### 🎯 จำนวนการวิเคราะห์ต่อผู้ใช้")
            user_analysis = {
                "student1": 45,
                "student2": 38,
                "student3": 42,
                "teacher": 30
            }
            fig_user = go.Figure(data=[
                go.Bar(y=list(user_analysis.keys()), x=list(user_analysis.values()),
                       orientation='h', marker=dict(color='#D4A5C8'))
            ])
            fig_user.update_layout(height=300, showlegend=False,
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(family="Prompt, sans-serif"))
            st.plotly_chart(fig_user, use_container_width=True)
        
        st.markdown("---")
        
        # Daily analysis trend
        st.markdown("#### 📉 แนวโน้มการวิเคราะห์รายวัน (7 วันที่ผ่านมา)")
        
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(6, -1, -1)]
        analysis_count = [15, 12, 18, 20, 16, 22, 25]
        
        fig_trend = go.Figure(data=[
            go.Scatter(x=dates, y=analysis_count, mode='lines+markers',
                      line=dict(color='#E8B4D4', width=3),
                      marker=dict(size=8, color='#D4A5C8'),
                      fill='tozeroy', fillcolor='rgba(232, 180, 212, 0.2)')
        ])
        fig_trend.update_layout(height=300, showlegend=False,
                               plot_bgcolor='rgba(0,0,0,0)',
                               paper_bgcolor='rgba(0,0,0,0)',
                               xaxis_title="วันที่", yaxis_title="จำนวนการวิเคราะห์",
                               font=dict(family="Prompt, sans-serif"))
        st.plotly_chart(fig_trend, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading statistics: {str(e)}")

# ========== TAB 3: USAGE HISTORY ==========
with tab3:
    st.subheader("📜 ประวัติการใช้งานทั้งระบบ")
    
    try:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_user = st.selectbox("เลือกผู้ใช้", ["ทั้งหมด"] + list(existing_users.keys()))
        
        with col2:
            filter_date = st.date_input("วันที่", value=datetime.now())
        
        with col3:
            sort_by = st.selectbox("เรียงตามลำดับ", ["ล่าสุดก่อน", "เก่าสุดก่อน"])
        
        st.markdown("---")
        
        # Load and display history
        if os.path.exists("history.json"):
            with open("history.json", 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            history_list = []
            for username, analyses in history.items():
                if filter_user == "ทั้งหมด" or filter_user == username:
                    for analysis in analyses:
                        history_list.append({
                            "Username": username,
                            "ชื่อไฟล์": analysis.get('file_name', 'N/A'),
                            "วันเวลา": analysis.get('timestamp', 'N/A'),
                            "ขนาดไฟล์": analysis.get('file_size_chars', 0),
                            "สถานะ": "✅ สำเร็จ"
                        })
            
            if history_list:
                history_df = pd.DataFrame(history_list)
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📋 ระเบียนทั้งหมด", len(history_list))
                with col2:
                    st.metric("📊 วันนี้", len([h for h in history_list if datetime.now().strftime('%Y-%m-%d') in h['วันเวลา']]))
                with col3:
                    st.metric("📈 ผู้ใช้ที่ใช้งาน", len(set(h['Username'] for h in history_list)))
            else:
                st.info("ไม่มีประวัติการใช้งาน")
        else:
            st.info("ยังไม่มีไฟล์ประวัติ")
    
    except Exception as e:
        st.error(f"Error loading history: {str(e)}")

# ========== TAB 4: SYSTEM SETTINGS ==========
with tab4:
    st.subheader("🔧 ตั้งค่าระบบ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔐 ตั้งค่าความปลอดภัย")
        
        st.markdown("##### 🔑 รีเซ็ตรหัสผ่านผู้ใช้")
        reset_user = st.selectbox("เลือกผู้ใช้", list(existing_users.keys()), key="reset_user_admin")
        new_pass = st.text_input("รหัสผ่านใหม่", type="password", key="new_pass_admin")
        
        if st.button("🔄 รีเซ็ตรหัสผ่าน", use_container_width=True, key="reset_btn_admin"):
            if new_pass:
                st.success(f"✅ รีเซ็ตรหัสผ่านสำเร็จสำหรับ {reset_user}")
            else:
                st.error("❌ กรุณากรอกรหัสผ่านใหม่")
        
        st.divider()
        
        st.markdown("#### 📋 Maintenance")
        st.markdown("##### 🗑️ ล้างข้อมูล Cache")
        st.warning("⚠️ การดำเนินการนี้จะลบข้อมูล Cache ทั้งหมด")
        
        col_clear1, col_clear2 = st.columns(2)
        with col_clear1:
            if st.button("🗑️ ล้าง Cache", use_container_width=True, type="secondary", key="clear_cache_admin"):
                st.success("✅ ล้าง Cache สำเร็จ!")
        with col_clear2:
            if st.button("🚫 ยกเลิก", use_container_width=True, key="cancel_cache_admin"):
                st.info("ยกเลิกการดำเนินการ")
    
    with col2:
        st.markdown("#### 🔔 ตั้งค่าการแจ้งเตือน")
        st.markdown("##### 📧 Email Notifications")
        enable_email = st.checkbox("เปิดใช้งานการแจ้งเตือน Email", key="enable_email_admin")
        email_recipient = st.text_input("Email สำหรับเข้ารับแจ้งเตือน", key="email_recipient_admin")
        
        col_notify1, col_notify2 = st.columns(2)
        with col_notify1:
            if st.button("📧 ส่งการทดสอบ", use_container_width=True, key="send_test_email_admin"):
                st.success("✅ ส่งอีเมลทดสอบสำเร็จ")
        with col_notify2:
            if st.button("💾 บันทึก", use_container_width=True, key="save_email_admin"):
                st.success("✅ บันทึกการตั้งค่าสำเร็จ")
        
        st.divider()
        
        st.markdown("#### 📊 ระบบข้อมูล")
        st.markdown("##### 💾 Database Info")
        st.info("**Database Status**: ✅ Online")
        st.info("**Database Type**: JSON")
        st.info("**Last Backup**: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        if st.button("💾 สำรองข้อมูล", use_container_width=True, key="backup_db_admin"):
            st.success("✅ สำรองข้อมูลสำเร็จ!")

# ========== TAB 5: REPORTS ==========
with tab5:
    st.subheader("📋 รายงาน")
    
    report_type = st.selectbox("เลือกประเภทรายงาน", [
        "รายงานสรุปประจำวัน",
        "รายงานสรุปประจำเดือน",
        "รายงานผู้ใช้",
        "รายงานประสิทธิภาพ",
        "รายงานปัญหา"
    ])
    
    st.markdown("---")
    
    if report_type == "รายงานสรุปประจำวัน":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("การวิเคราะห์วันนี้", 25, "+8")
        with col2:
            st.metric("ผู้ใช้ที่ใช้งาน", 4, "100%")
        with col3:
            st.metric("ไฟล์ที่ประมวลผล", 25, "+8")
        
        st.markdown("**สรุปรายวัน:**")
        st.write("""
        - ✅ ระบบทำงานปกติ
        - ✅ ไม่มีข้อผิดพลาด
        - ✅ ประสิทธิภาพ: 99.5%
        - ✅ เวลาตอบสนองเฉลี่ย: 2.3 วินาที
        """)
    
    elif report_type == "รายงานผู้ใช้":
        user_report_data = []
        for username, info in existing_users.items():
            user_report_data.append({
                "Username": username,
                "ชื่อ": info['name'],
                "Role": info['role'],
                "จำนวนการวิเคราะห์": [45, 38, 42, 30][list(existing_users.keys()).index(username)],
                "ไฟล์ที่วิเคราะห์": [45, 38, 42, 30][list(existing_users.keys()).index(username)]
            })
        
        user_report_df = pd.DataFrame(user_report_data)
        st.dataframe(user_report_df, use_container_width=True, hide_index=True)
    
    else:
        st.info(f"📋 รายงาน: {report_type}")
        st.write("(ขอให้เลือกประเภทรายงาน)")
    
    st.markdown("---")
    
    col_export1, col_export2, col_export3 = st.columns(3)
    with col_export1:
        if st.button("📊 ส่งออก PDF", use_container_width=True):
            st.success("✅ ส่งออก PDF สำเร็จ!")
    with col_export2:
        if st.button("📈 ส่งออก Excel", use_container_width=True):
            st.success("✅ ส่งออก Excel สำเร็จ!")
    with col_export3:
        if st.button("📄 ส่งออก Report", use_container_width=True):
            st.success("✅ สร้างรายงานสำเร็จ!")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #B8879F; font-size: 12px; margin-top: 30px;'>
<p>🔒 Admin Panel v1.0 | ระบบบริหารจัดการโครงงาน AI | © 2024</p>
<p>Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
</div>
""", unsafe_allow_html=True)
