#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Panel Page
Part of Streamlit Multi-Page App
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import time

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Admin Panel - ระบบตรวจโครงงาน AI",
    page_icon="⚙️",
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
    font-family: 'Prompt', sans-serif !important;
}

body {
    background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%);
    color: #333;
    font-family: 'Prompt', sans-serif;
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
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.3);
    border-color: #E8B4D4;
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

hr {
    border: 0;
    height: 2px;
    background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
    margin: 20px 0;
}

/* ปรับ padding ด้านบนให้พอดี */
.main .block-container {
    padding-top: 1rem !important;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== SIDEBAR REMOVED ==========

# ========== INITIALIZATION ==========
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'admin_username' not in st.session_state:
    st.session_state.admin_username = None

# ========== LOGIN PAGE ==========
if not st.session_state.admin_logged_in:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("# ⚙️ หน้าสำหรับผู้ดูแลระบบ")
        st.markdown("### จัดการผู้ใช้และดูสถิติระบบทั้งหมด")
        
        with st.form("admin_login_form"):
            st.markdown("#### Admin Login")
            username = st.text_input("👤 Username")
            password = st.text_input("🔐 Password", type="password")
            
            submitted = st.form_submit_button("🔓 เข้าสู่ระบบ Admin", use_container_width=True)
            
            if submitted:
                if username and password:
                    # ตรวจสอบจาก database
                    users_file = "users_database.json"
                    if os.path.exists(users_file):
                        with open(users_file, 'r', encoding='utf-8') as f:
                            users_data = json.load(f)
                        
                        # หา user ที่ตรงกัน
                        user_found = False
                        for user in users_data.get("users", []):
                            if user["username"] == username and user["password"] == password:
                                # ตรวจสอบว่าเป็น admin หรือ teacher เท่านั้น
                                if user["role"] in ["admin", "teacher"]:
                                    st.session_state.admin_logged_in = True
                                    st.session_state.admin_username = username
                                    st.session_state.admin_role = user["role"]
                                    st.success(f"✅ เข้าสู่ระบบสำเร็จ! ยินดีต้อนรับ {user['name']}")
                                    time.sleep(1)
                                    st.rerun()
                                    user_found = True
                                    break
                                else:
                                    st.error("❌ คุณไม่มีสิทธิ์เข้าถึง Admin Panel (เฉพาะ Admin/Teacher)")
                                    user_found = True
                                    break
                        
                        if not user_found:
                            st.error("❌ Username หรือ Password ไม่ถูกต้อง")
                    else:
                        st.error("❌ ไม่พบฐานข้อมูลผู้ใช้")
                else:
                    st.warning("⚠️ กรุณากรอก Username และ Password")

# ========== MAIN ADMIN INTERFACE ==========
else:
    
    st.markdown("# ⚙️ ระบบจัดการผู้ดูแล")
    st.markdown(f"ยินดีต้อนรับ **{st.session_state.admin_username}**! 👋")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "👥 จัดการผู้ใช้",
        "📊 สถิติระบบ",
        "📜 ประวัติการใช้งาน",
        "🔧 ตั้งค่าระบบ",
        "📋 รายงาน",
        "📝 ผลการประเมินความพึงพอใจ",
        "🚪 ออกจากระบบ"
    ])
    
    # ========== TAB 1: USER MANAGEMENT ==========
    with tab1:
        st.markdown("## 👥 จัดการผู้ใช้")
        
        # ฟังก์ชันจัดการฐานข้อมูลผู้ใช้
        def load_users():
            """โหลดข้อมูลผู้ใช้จากไฟล์"""
            import json
            users_file = "users_database.json"
            try:
                if os.path.exists(users_file):
                    with open(users_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    return {"users": []}
            except:
                return {"users": []}
        
        def save_users(users_data):
            """บันทึกข้อมูลผู้ใช้ลงไฟล์"""
            import json
            users_file = "users_database.json"
            with open(users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
        
        def add_user(username, password, name, role):
            """เพิ่มผู้ใช้ใหม่"""
            users_data = load_users()
            
            # ตรวจสอบว่า username ซ้ำหรือไม่
            for user in users_data["users"]:
                if user["username"] == username:
                    return False, "ชื่อผู้ใช้นี้มีอยู่แล้ว"
            
            # สร้าง ID ใหม่
            user_id = f"user_{len(users_data['users']) + 1:03d}"
            
            new_user = {
                "id": user_id,
                "username": username,
                "password": password,
                "name": name,
                "role": role,
                "status": "active",
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "last_login": None
            }
            
            users_data["users"].append(new_user)
            save_users(users_data)
            return True, "เพิ่มผู้ใช้สำเร็จ"
        
        def update_user(user_id, username, password, name, role, status):
            """แก้ไขข้อมูลผู้ใช้"""
            users_data = load_users()
            
            for user in users_data["users"]:
                if user["id"] == user_id:
                    user["username"] = username
                    if password:  # เปลี่ยนรหัสผ่านเฉพาะเมื่อใส่ค่าใหม่
                        user["password"] = password
                    user["name"] = name
                    user["role"] = role
                    user["status"] = status
                    save_users(users_data)
                    return True, "แก้ไขข้อมูลสำเร็จ"
            
            return False, "ไม่พบผู้ใช้"
        
        def delete_user(user_id):
            """ลบผู้ใช้"""
            users_data = load_users()
            users_data["users"] = [u for u in users_data["users"] if u["id"] != user_id]
            save_users(users_data)
            return True, "ลบผู้ใช้สำเร็จ"
        
        # โหลดข้อมูลผู้ใช้
        users_db = load_users()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ➕ เพิ่มผู้ใช้ใหม่")
            with st.form("add_user_form"):
                new_username = st.text_input("ชื่อผู้ใช้ *", placeholder="student2")
                new_password = st.text_input("รหัสผ่าน *", type="password", placeholder="อย่างน้อย 6 ตัวอักษร")
                new_name = st.text_input("ชื่อ-นามสกุล *", placeholder="นักเรียน 2")
                new_role = st.selectbox("บทบาท *", ["student", "teacher", "admin"])
                
                submitted = st.form_submit_button("✅ เพิ่มผู้ใช้", use_container_width=True)
                
                if submitted:
                    if not new_username or not new_password or not new_name:
                        st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
                    elif len(new_password) < 6:
                        st.error("❌ รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
                    else:
                        success, message = add_user(new_username, new_password, new_name, new_role)
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        with col2:
            st.markdown("### 📋 รายชื่อผู้ใช้")
            st.info(f"📊 จำนวนผู้ใช้ทั้งหมด: **{len(users_db['users'])}** คน")
            
            # แสดงตารางผู้ใช้
            if users_db["users"]:
                users_data = {
                    "ชื่อผู้ใช้": [u["username"] for u in users_db["users"]],
                    "ชื่อ": [u["name"] for u in users_db["users"]],
                    "บทบาท": [u["role"] for u in users_db["users"]],
                    "สถานะ": ["✅ ใช้งาน" if u["status"] == "active" else "⛔ ปิดใช้งาน" for u in users_db["users"]]
            }
                st.dataframe(pd.DataFrame(users_data), use_container_width=True)
            else:
                st.info("ยังไม่มีผู้ใช้ในระบบ")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✏️ แก้ไขผู้ใช้")
            
            if users_db["users"]:
                user_options = {f"{u['username']} ({u['name']})": u for u in users_db["users"]}
                selected_user_key = st.selectbox("เลือกผู้ใช้ที่จะแก้ไข", list(user_options.keys()), key="edit_select")
                
                if selected_user_key:
                    selected_user = user_options[selected_user_key]
                    
                    with st.form("edit_user_form"):
                        edit_username = st.text_input("ชื่อผู้ใช้", value=selected_user["username"])
                        edit_password = st.text_input("รหัสผ่านใหม่", type="password", placeholder="เว้นว่างถ้าไม่เปลี่ยน")
                        edit_name = st.text_input("ชื่อ-นามสกุล", value=selected_user["name"])
                        edit_role = st.selectbox("บทบาท", ["student", "teacher", "admin"], 
                                                index=["student", "teacher", "admin"].index(selected_user["role"]))
                        edit_status = st.selectbox("สถานะ", ["active", "inactive"],
                                                  index=0 if selected_user["status"] == "active" else 1)
                        
                        if st.form_submit_button("💾 บันทึกการเปลี่ยนแปลง", use_container_width=True):
                            success, message = update_user(
                                selected_user["id"],
                                edit_username,
                                edit_password if edit_password else None,
                                edit_name,
                                edit_role,
                                edit_status
                            )
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
            else:
                st.info("ยังไม่มีผู้ใช้ในระบบ")
        
        with col2:
            st.markdown("### 🗑️ ลบผู้ใช้")
            
            if users_db["users"]:
                delete_options = {f"{u['username']} ({u['name']})": u for u in users_db["users"]}
                selected_delete_key = st.selectbox("เลือกผู้ใช้ที่จะลบ", list(delete_options.keys()), key="delete_select")
                
                if selected_delete_key:
                    selected_delete_user = delete_options[selected_delete_key]
                    
                    st.warning(f"⚠️ คุณกำลังจะลบ: **{selected_delete_user['username']}** ({selected_delete_user['name']})")
                    
                    col_del1, col_del2 = st.columns(2)
                    with col_del1:
                        if st.button(f"❌ ยืนยันลบ", type="secondary", use_container_width=True, key="confirm_delete"):
                            success, message = delete_user(selected_delete_user["id"])
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                    with col_del2:
                        if st.button("🚫 ยกเลิก", use_container_width=True, key="cancel_delete"):
                            st.info("ยกเลิกการลบ")
            else:
                st.info("ยังไม่มีผู้ใช้ในระบบ")
    
    # ========== TAB 2: STATISTICS ==========
    with tab2:
        st.markdown("## 📊 สถิติระบบ")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 การวิเคราะห์ทั้งหมด", "156", "+12")
        with col2:
            st.metric("👥 ผู้ใช้ที่ใช้งาน", "8", "+2")
        with col3:
            st.metric("📂 ไฟล์ที่วิเคราะห์", "45", "+5")
        with col4:
            st.metric("⏱️ เวลาตอบสนองเฉลี่ย", "2.3s", "-0.3s")
        
        st.markdown("---")
        
        st.markdown("### 📈 การใช้งานตามบทบาท")
        st.bar_chart(data={
            "นักเรียน": 120,
            "อาจารย์": 25,
            "ผู้ดูแล": 11
        })
    
    # ========== TAB 3: HISTORY ==========
    with tab3:
        st.markdown("## 📜 ประวัติการใช้งาน")
        
        # อ่านข้อมูลจาก history.json
        try:
            history_file = "history.json"
            all_analyses = []
            
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                if "analyses" in history_data:
                    all_analyses = history_data["analyses"]
            
            # ดึงรายชื่อ user ทั้งหมด
            all_users = list(set([entry.get("username", "-") for entry in all_analyses]))
            all_users.insert(0, "ทั้งหมด")
            
            col1, col2 = st.columns(2)
            with col1:
                filter_user = st.selectbox("กรองตามผู้ใช้", all_users)
            with col2:
                filter_date = st.date_input("กรองตามวันที่", datetime.now())
            
            # กรองข้อมูล
            filtered_analyses = all_analyses
            
            if filter_user != "ทั้งหมด":
                filtered_analyses = [a for a in filtered_analyses if a.get("username") == filter_user]
            
            if filter_date:
                filter_date_str = filter_date.strftime('%Y-%m-%d')
                filtered_analyses = [
                    a for a in filtered_analyses 
                    if a.get("timestamp", "").startswith(filter_date_str)
                ]
            
            # แสดงข้อมูลเป็นตาราง
            if filtered_analyses:
                display_data = {
                    "ชื่อผู้ใช้": [a.get("username", "-") for a in filtered_analyses],
                    "ไฟล์": [a.get("file_name", "-") for a in filtered_analyses],
                    "บทที่ตรวจ": [a.get("chapter_checked", "ทั้งหมด") for a in filtered_analyses],
                    "วันที่": [a.get("timestamp", "-") for a in filtered_analyses],
                    "จำนวนคำ": [f"{a.get('word_count', 0):,}" for a in filtered_analyses],
                    "คะแนน": [f"{a.get('score', '-')}/100" if a.get('score') is not None else "-" for a in filtered_analyses],
                    "สถานะ": ["✅ สำเร็จ" for _ in filtered_analyses]
                }
                
                st.dataframe(pd.DataFrame(display_data), use_container_width=True)
                
                # แสดงรายละเอียดเพิ่มเติม
                st.markdown("---")
                st.markdown("### 📊 รายละเอียดการวิเคราะห์")
                
                for i, entry in enumerate(filtered_analyses[:10], 1):  # แสดง 10 รายการล่าสุด
                    with st.expander(f"📄 {entry.get('username', '-')} - {entry.get('file_name', '-')} ({entry.get('timestamp', '-')})"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"**ผู้ใช้:** {entry.get('username', '-')}")
                            st.markdown(f"**ไฟล์:** {entry.get('file_name', '-')}")
                            st.markdown(f"**บทที่ตรวจ:** {entry.get('chapter_checked', 'ทั้งหมด')}")
                        with col_b:
                            st.markdown(f"**จำนวนคำ:** {entry.get('word_count', 0):,} คำ")
                            st.markdown(f"**จำนวนหน้า:** {entry.get('num_pages', 0)} หน้า")
                            st.markdown(f"**ขนาดไฟล์:** {entry.get('file_size', 0) / 1024:.2f} KB")
                        
                        # แสดงความคืบหน้า
                        if 'chapter_progress' in entry:
                            progress = entry['chapter_progress']
                            completed = sum(1 for v in progress.values() if v)
                            total = 5
                            st.progress(completed / total)
                            st.markdown(f"**ความคืบหน้า:** {completed}/{total} บท ({completed/total*100:.0f}%)")
                        
                        # แสดงผลการวิเคราะห์
                        if st.button(f"📖 ดูผลการวิเคราะห์", key=f"admin_view_{i}"):
                            st.markdown(entry.get('analysis_result', 'ไม่มีข้อมูล'))
            else:
                st.info("ℹ️ ไม่พบข้อมูลตามเงื่อนไขที่เลือก")
            
            # สถิติ
            col1, col2, col3 = st.columns(3)
            
            # นับระเบียนทั้งหมด
            total_records = len(all_analyses)
            
            # นับระเบียนวันนี้
            today_str = datetime.now().strftime('%Y-%m-%d')
            today_records = len([a for a in all_analyses if a.get("timestamp", "").startswith(today_str)])
            
            # นับผู้ใช้ที่ใช้งาน (unique users)
            active_users = len(set([a.get("username", "-") for a in all_analyses]))
            
            with col1:
                st.metric("📋 ระเบียนทั้งหมด", f"{total_records}")
            with col2:
                st.metric("📅 ระเบียนวันนี้", f"{today_records}")
            with col3:
                st.metric("👤 ผู้ใช้ที่ใช้งาน", f"{active_users}")
                
        except Exception as e:
            st.error(f"❌ ไม่สามารถโหลดประวัติได้: {str(e)}")
            st.info("ℹ️ กรุณาตรวจสอบไฟล์ history.json")
    
    # ========== TAB 4: SETTINGS ==========
    with tab4:
        st.markdown("## 🔧 ตั้งค่าระบบ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔐 ความปลอดภัย")
            
            st.markdown("#### 🔑 รีเซ็ตรหัสผ่านผู้ใช้")
            
            # โหลดข้อมูลผู้ใช้จริงจากฐานข้อมูล
            users_data = load_users()
            user_list = [u['username'] for u in users_data.get('users', [])]
            
            if user_list:
                reset_user = st.selectbox("เลือกผู้ใช้", user_list, key="reset_user_select")
                new_pass = st.text_input("รหัสผ่านใหม่", type="password", key="new_pass_input")
                confirm_pass = st.text_input("ยืนยันรหัสผ่านใหม่", type="password", key="confirm_pass_input")
                
                if st.button("✅ รีเซ็ตรหัสผ่าน", use_container_width=True, key="reset_pass_btn"):
                    if not new_pass:
                        st.error("❌ กรุณากรอกรหัสผ่านใหม่")
                    elif len(new_pass) < 6:
                        st.error("❌ รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
                    elif new_pass != confirm_pass:
                        st.error("❌ รหัสผ่านไม่ตรงกัน")
                    else:
                        # รีเซ็ตรหัสผ่านจริง
                        for user in users_data['users']:
                            if user['username'] == reset_user:
                                user['password'] = new_pass
                                save_users(users_data)
                                st.success(f"✅ รีเซ็ตรหัสผ่านสำหรับ '{reset_user}' สำเร็จ!")
                                break
            else:
                st.info("ไม่พบผู้ใช้ในระบบ")
            
            st.markdown("---")
            st.markdown("#### 🗑️ ล้างแคช")
            if st.button("🧹 ล้างแคชระบบ", use_container_width=True, type="secondary", key="clear_cache_btn"):
                try:
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    st.success("✅ ล้างแคชสำเร็จ!")
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")
        
        with col2:
            st.markdown("### 📧 การแจ้งเตือน")
            
            st.markdown("#### 📬 ตั้งค่าอีเมล")
            
            # โหลดการตั้งค่าอีเมล
            settings_file = "system_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            else:
                settings = {
                    "email_enabled": False,
                    "email_address": ""
                }
            
            email_enabled = st.checkbox("เปิดใช้การแจ้งเตือนผ่านอีเมล", 
                                       value=settings.get("email_enabled", False), 
                                       key="email_enabled_check")
            
            if email_enabled:
                email = st.text_input("อีเมลสำหรับแจ้งเตือน", 
                                     value=settings.get("email_address", ""),
                                     key="email_input")
                
                col_email1, col_email2 = st.columns(2)
                with col_email1:
                    if st.button("💾 บันทึกการตั้งค่า", use_container_width=True, key="save_email_btn"):
                        if email:
                            settings["email_enabled"] = True
                            settings["email_address"] = email
                            with open(settings_file, 'w', encoding='utf-8') as f:
                                json.dump(settings, f, ensure_ascii=False, indent=2)
                            st.success("✅ บันทึกการตั้งค่าสำเร็จ!")
                        else:
                            st.error("❌ กรุณากรอกอีเมล")
                
                with col_email2:
                    if st.button("✉️ ทดสอบ", use_container_width=True, key="send_email_btn"):
                        if email:
                            st.info(f"📧 ทดสอบส่งอีเมลไปที่: {email}")
                            st.warning("⚠️ ฟีเจอร์การส่งอีเมลจริงต้องตั้งค่า SMTP Server ก่อน")
                        else:
                            st.error("❌ กรุณากรอกอีเมล")
            else:
                # บันทึกการปิดใช้งาน
                if settings.get("email_enabled", False):
                    settings["email_enabled"] = False
                    with open(settings_file, 'w', encoding='utf-8') as f:
                        json.dump(settings, f, ensure_ascii=False, indent=2)
            
            st.markdown("---")
            st.markdown("#### 💾 ฐานข้อมูล")
            if st.button("💾 สำรองฐานข้อมูล", use_container_width=True, key="backup_db_btn"):
                try:
                    from datetime import datetime
                    import shutil
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_folder = "backups"
                    
                    if not os.path.exists(backup_folder):
                        os.makedirs(backup_folder)
                    
                    # สำรองไฟล์ที่สำคัญ
                    files_to_backup = [
                        "users_database.json",
                        "satisfaction_data.json",
                        "history.json"
                    ]
                    
                    backed_up = []
                    for file in files_to_backup:
                        if os.path.exists(file):
                            backup_name = f"{backup_folder}/{file.replace('.json', '')}_{timestamp}.json"
                            shutil.copy2(file, backup_name)
                            backed_up.append(file)
                    
                    if backed_up:
                        st.success(f"✅ สำรองฐานข้อมูลสำเร็จ! ({len(backed_up)} ไฟล์)")
                        st.info(f"📁 ตำแหน่ง: {backup_folder}/")
                    else:
                        st.warning("⚠️ ไม่พบไฟล์ฐานข้อมูลที่ต้องสำรอง")
                        
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")
    
    # ========== TAB 5: REPORTS ==========
    with tab5:
        st.markdown("## 📋 รายงาน")
        
        report_type = st.selectbox("ประเภทรายงาน", [
            "รายงานประจำวัน",
            "รายงานประจำเดือน",
            "รายงานผู้ใช้",
            "รายงานประสิทธิภาพ",
            "รายงานปัญหา"
        ])
        
        st.markdown(f"### {report_type}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 ส่งออก PDF", use_container_width=True):
                st.success(f"✅ ส่งออก {report_type} เป็น PDF สำเร็จ!")
        with col2:
            if st.button("📊 ส่งออก Excel", use_container_width=True):
                st.success(f"✅ ส่งออก {report_type} เป็น Excel สำเร็จ!")
        with col3:
            if st.button("📋 ดูรายงาน", use_container_width=True):
                st.info(f"📄 {report_type} - แสดงข้อมูลตัวอย่าง")
        
        st.markdown("---")
        st.dataframe({
            "วันที่": ["2025-12-15", "2025-12-14", "2025-12-13"],
            "การวิเคราะห์": [15, 18, 12],
            "ผู้ใช้": [5, 6, 4],
            "ข้อผิดพลาด": [0, 1, 0]
        }, use_container_width=True)
    
    # ========== TAB 6: SURVEY RESULTS ==========
    with tab6:
        st.markdown("## 📝 ผลการประเมินความพึงพอใจระบบ")
        st.markdown("### สรุปผลการสำรวจจากครูและนักเรียน")
        
        # โหลดข้อมูลจาก satisfaction database
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            from satisfaction_database import SatisfactionDatabase
            
            db = SatisfactionDatabase()
            all_surveys = db.get_all_surveys()
            
            # ตรวจสอบว่า all_surveys เป็น list และไม่ว่าง
            if not all_surveys or not isinstance(all_surveys, list):
                st.info("📭 ยังไม่มีข้อมูลการประเมินความพึงพอใจ")
                st.info("💡 รอให้ครูหรือนักเรียนทำแบบประเมินความพึงพอใจก่อน")
            else:
                # สถิติภาพรวม
                teacher_surveys = db.get_surveys_by_type("teacher")
                student_surveys = db.get_surveys_by_type("student")
                
                # ตรวจสอบว่าเป็น list
                if not isinstance(teacher_surveys, list):
                    teacher_surveys = []
                if not isinstance(student_surveys, list):
                    student_surveys = []
                
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.metric("📊 การประเมินทั้งหมด", len(all_surveys))
                
                with col_stat2:
                    st.metric("👨‍🏫 ครู", len(teacher_surveys))
                
                with col_stat3:
                    st.metric("👨‍🎓 นักเรียน", len(student_surveys))
                
                with col_stat4:
                    # คำนวณคะแนนเฉลี่ยอย่างปลอดภัย
                    try:
                        avg_scores = []
                        for s in all_surveys:
                            if isinstance(s, dict) and 'average_score' in s:
                                score = s.get('average_score', 0)
                                if isinstance(score, (int, float)):
                                    avg_scores.append(score)
                        
                        avg_satisfaction = sum(avg_scores) / len(avg_scores) if avg_scores else 0
                        st.metric("⭐ คะแนนเฉลี่ย", f"{avg_satisfaction:.2f}/5.0")
                    except:
                        st.metric("⭐ คะแนนเฉลี่ย", "N/A")
                
                st.markdown("---")
                
                # Tabs สำหรับแยกดูแต่ละกลุ่ม
                tab_overview, tab_teacher, tab_student, tab_export = st.tabs([
                    "📊 ภาพรวม",
                    "👨‍🏫 ครู",
                    "👨‍🎓 นักเรียน",
                    "📥 ส่งออกข้อมูล"
                ])
                
                with tab_overview:
                    st.markdown("### 📊 เปรียบเทียบความพึงพอใจ")
                    
                    # สถิติแบบละเอียด
                    teacher_stats = db.calculate_statistics("teacher")
                    student_stats = db.calculate_statistics("student")
                    
                    if teacher_stats and student_stats:
                        # กราฟแท่งเปรียบเทียบ
                        import plotly.graph_objects as go
                        
                        categories = []
                        teacher_scores = []
                        student_scores = []
                        
                        # รวมหมวดหมู่จาก teacher และ student
                        all_categories = set(list(teacher_stats.keys()) + list(student_stats.keys()))
                        
                        for cat in sorted(all_categories):
                            if cat != 'overall':
                                categories.append(cat)
                                
                                # ตรวจสอบว่า value เป็น dict จริงก่อนเรียก .get()
                                teacher_val = teacher_stats.get(cat, {})
                                if isinstance(teacher_val, dict):
                                    teacher_scores.append(teacher_val.get('mean', 0))
                                else:
                                    teacher_scores.append(0)
                                
                                student_val = student_stats.get(cat, {})
                                if isinstance(student_val, dict):
                                    student_scores.append(student_val.get('mean', 0))
                                else:
                                    student_scores.append(0)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            name='ครู',
                            x=categories,
                            y=teacher_scores,
                            marker_color='#E8B4D4',
                            text=[f"{s:.2f}" for s in teacher_scores],
                            textposition='auto'
                        ))
                        fig.add_trace(go.Bar(
                            name='นักเรียน',
                            x=categories,
                            y=student_scores,
                            marker_color='#D4A5C8',
                            text=[f"{s:.2f}" for s in student_scores],
                            textposition='auto'
                        ))
                        
                        fig.update_layout(
                            title="คะแนนเฉลี่ยแต่ละหมวดหมู่",
                            xaxis_title="หมวดหมู่",
                            yaxis_title="คะแนนเฉลี่ย (1-5)",
                            barmode='group',
                            height=400,
                            yaxis=dict(range=[0, 5])
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # แสดงตารางเปรียบเทียบ
                        st.markdown("#### 📋 สรุปคะแนนเฉลี่ยรายหมวด")
                        
                        comparison_data = {
                            "หมวดหมู่": categories,
                            "ครู (คะแนนเฉลี่ย)": [f"{s:.2f}" for s in teacher_scores],
                            "นักเรียน (คะแนนเฉลี่ย)": [f"{s:.2f}" for s in student_scores]
                        }
                        
                        st.dataframe(comparison_data, use_container_width=True)
                    
                    # Histogram แสดงการกระจายของคะแนน
                    st.markdown("---")
                    st.markdown("### 📈 การกระจายของคะแนนความพึงพอใจ")
                    
                    all_scores_teacher = []
                    all_scores_student = []
                    
                    # ดึงคะแนนจากครูอย่างปลอดภัย
                    for survey in teacher_surveys:
                        if isinstance(survey, dict):
                            responses = survey.get('responses', {})
                            if isinstance(responses, dict):
                                for k, v in responses.items():
                                    if k.startswith('q') and isinstance(v, (int, float)):
                                        all_scores_teacher.append(v)
                    
                    # ดึงคะแนนจากนักเรียนอย่างปลอดภัย
                    for survey in student_surveys:
                        if isinstance(survey, dict):
                            responses = survey.get('responses', {})
                            if isinstance(responses, dict):
                                for k, v in responses.items():
                                    if k.startswith('q') and isinstance(v, (int, float)):
                                        all_scores_student.append(v)
                    
                    if all_scores_teacher or all_scores_student:
                        try:
                            import pandas as pd
                            import plotly.express as px
                            
                            # สร้าง DataFrame
                            data = []
                            for score in all_scores_teacher:
                                data.append({"คะแนน": score, "กลุ่ม": "ครู"})
                            for score in all_scores_student:
                                data.append({"คะแนน": score, "กลุ่ม": "นักเรียน"})
                            
                            df = pd.DataFrame(data)
                            
                            fig = px.histogram(
                                df, 
                                x="คะแนน", 
                                color="กลุ่ม",
                                barmode="overlay",
                                nbins=5,
                                color_discrete_map={"ครู": "#E8B4D4", "นักเรียน": "#D4A5C8"}
                            )
                            
                            fig.update_layout(
                                title="การกระจายของคะแนน (1-5)",
                                xaxis_title="คะแนน",
                                yaxis_title="จำนวน",
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.warning(f"⚠️ ไม่สามารถสร้างกราฟได้: {str(e)}")
                    else:
                        st.info("📭 ไม่มีข้อมูลคะแนนเพียงพอในการสร้างกราฟ")
                
                with tab_teacher:
                    st.markdown("### 👨‍🏫 ผลการประเมินจากครู")
                    
                    if not teacher_surveys:
                        st.info("📭 ยังไม่มีการประเมินจากครู")
                    else:
                        # แสดงสถิติครู
                        teacher_stats = db.calculate_statistics("teacher")
                        
                        if teacher_stats and isinstance(teacher_stats, dict):
                            st.markdown("#### 📊 คะแนนเฉลี่ยแต่ละหมวดหมู่")
                            
                            for category, stats in teacher_stats.items():
                                if category != 'overall' and isinstance(stats, dict):
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        mean_val = stats.get('mean', 0)
                                        st.metric(f"📌 {category}", f"{mean_val:.2f}/5.0")
                                    with col2:
                                        max_val = stats.get('max', 0)
                                        st.metric("สูงสุด", f"{max_val:.2f}")
                                    with col3:
                                        min_val = stats.get('min', 0)
                                        st.metric("ต่ำสุด", f"{min_val:.2f}")
                        
                        st.markdown("---")
                        
                        # แสดงข้อเสนอแนะ
                        st.markdown("#### 💭 ข้อเสนอแนะจากครู")
                        
                        suggestions = []
                        for survey in teacher_surveys:
                            if isinstance(survey, dict):
                                responses = survey.get('responses', {})
                                if isinstance(responses, dict):
                                    suggestion = responses.get('suggestions', '')
                                    if suggestion and suggestion.strip():
                                        username = survey.get('username', 'ไม่ระบุชื่อ')
                                        timestamp = survey.get('timestamp', '')
                                        suggestions.append({
                                            "ผู้ใช้": username,
                                            "วันที่": timestamp,
                                            "ข้อเสนอแนะ": suggestion
                                        })
                        
                        if suggestions:
                            for i, sug in enumerate(suggestions, 1):
                                with st.expander(f"💬 ข้อเสนอแนะที่ {i} - {sug['ผู้ใช้']} ({sug['วันที่']})"):
                                    st.write(sug['ข้อเสนอแนะ'])
                        else:
                            st.info("ไม่มีข้อเสนอแนะเพิ่มเติม")
                
                with tab_student:
                    st.markdown("### 👨‍🎓 ผลการประเมินจากนักเรียน")
                    
                    if not student_surveys:
                        st.info("📭 ยังไม่มีการประเมินจากนักเรียน")
                    else:
                        # แสดงสถิตินักเรียน
                        student_stats = db.calculate_statistics("student")
                        
                        if student_stats and isinstance(student_stats, dict):
                            st.markdown("#### 📊 คะแนนเฉลี่ยแต่ละหมวดหมู่")
                            
                            for category, stats in student_stats.items():
                                if category != 'overall' and isinstance(stats, dict):
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        mean_val = stats.get('mean', 0)
                                        st.metric(f"📌 {category}", f"{mean_val:.2f}/5.0")
                                    with col2:
                                        max_val = stats.get('max', 0)
                                        st.metric("สูงสุด", f"{max_val:.2f}")
                                    with col3:
                                        min_val = stats.get('min', 0)
                                        st.metric("ต่ำสุด", f"{min_val:.2f}")
                        
                        st.markdown("---")
                        
                        # แสดงข้อเสนอแนะ
                        st.markdown("#### 💭 ข้อเสนอแนะจากนักเรียน")
                        
                        suggestions = []
                        for survey in student_surveys:
                            if isinstance(survey, dict):
                                responses = survey.get('responses', {})
                                if isinstance(responses, dict):
                                    suggestion = responses.get('suggestions', '')
                                    if suggestion and suggestion.strip():
                                        username = survey.get('username', 'ไม่ระบุชื่อ')
                                        timestamp = survey.get('timestamp', '')
                                        suggestions.append({
                                            "ผู้ใช้": username,
                                            "วันที่": timestamp,
                                            "ข้อเสนอแนะ": suggestion
                                        })
                        
                        if suggestions:
                            for i, sug in enumerate(suggestions, 1):
                                with st.expander(f"💬 ข้อเสนอแนะที่ {i} - {sug['ผู้ใช้']} ({sug['วันที่']})"):
                                    st.write(sug['ข้อเสนอแนะ'])
                        else:
                            st.info("ไม่มีข้อเสนอแนะเพิ่มเติม")
                
                with tab_export:
                    st.markdown("### 📥 ส่งออกข้อมูลเพื่อการวิจัย")
                    
                    st.info("💡 ข้อมูลที่ส่งออกสามารถนำไปวิเคราะห์ด้วย Excel, SPSS, หรือเครื่องมือสถิติอื่นๆ ได้")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Export JSON
                        try:
                            export_data = db.export_for_research()
                            
                            import json
                            json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
                            
                            st.download_button(
                                label="📄 ดาวน์โหลด JSON (ข้อมูลเต็ม)",
                                data=json_str,
                                file_name=f"survey_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"❌ ไม่สามารถส่งออก JSON: {str(e)}")
                    
                    with col2:
                        # Export CSV
                        try:
                            import pandas as pd
                            
                            csv_data = []
                            for survey in all_surveys:
                                if isinstance(survey, dict):
                                    row = {
                                        "ผู้ใช้": survey.get('username', ''),
                                        "ประเภท": survey.get('user_type', ''),
                                        "วันที่": survey.get('timestamp', ''),
                                        "คะแนนเฉลี่ย": survey.get('average_score', 0)
                                    }
                                    
                                    # เพิ่มคำตอบแต่ละข้อ
                                    responses = survey.get('responses', {})
                                    if isinstance(responses, dict):
                                        for key, value in responses.items():
                                            if key.startswith('q'):
                                                row[f"คำตอบ_{key}"] = value
                                        
                                        row["ข้อเสนอแนะ"] = responses.get('suggestions', '')
                                    
                                    csv_data.append(row)
                            
                            if csv_data:
                                df = pd.DataFrame(csv_data)
                                csv_str = df.to_csv(index=False, encoding='utf-8-sig')
                                
                                st.download_button(
                                    label="📊 ดาวน์โหลด CSV (สำหรับ Excel/SPSS)",
                                    data=csv_str,
                                    file_name=f"survey_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            else:
                                st.warning("⚠️ ไม่มีข้อมูลสำหรับส่งออก")
                        except Exception as e:
                            st.error(f"❌ ไม่สามารถส่งออก CSV: {str(e)}")
                    
                    st.markdown("---")
                    st.markdown("#### 📋 ข้อมูลสรุปโดยละเอียด")
                    
                    try:
                        # แสดงข้อมูลเชิงสถิติแบบละเอียด
                        col_summary1, col_summary2 = st.columns(2)
                        
                        with col_summary1:
                            st.markdown("##### 📊 สถิติการตอบแบบสอบถาม")
                            summary_stats = {
                                "การตอบแบบสอบถามทั้งหมด": len(all_surveys),
                                "ครูที่ตอบแบบสอบถาม": len(teacher_surveys),
                                "นักเรียนที่ตอบแบบสอบถาม": len(student_surveys),
                                "วันที่สร้างข้อมูล": db._load_data().get('metadata', {}).get('created_at', 'N/A'),
                                "อัพเดทล่าสุด": db._load_data().get('metadata', {}).get('last_updated', 'N/A')
                            }
                            
                            for key, value in summary_stats.items():
                                st.metric(key, value)
                        
                        with col_summary2:
                            st.markdown("##### ⭐ คะแนนเฉลี่ยตามหมวดหมู่")
                            
                            # คำนวณคะแนนเฉลี่ยรวมทั้งครูและนักเรียน
                            teacher_stats = db.calculate_statistics("teacher")
                            student_stats = db.calculate_statistics("student")
                            
                            # แสดงคะแนนเฉลี่ยรวม
                            if teacher_stats and student_stats:
                                all_categories = set(list(teacher_stats.keys()) + list(student_stats.keys()))
                                
                                for cat in sorted(all_categories):
                                    if cat != 'overall_mean' and cat != 'overall':
                                        teacher_val = teacher_stats.get(cat, {})
                                        student_val = student_stats.get(cat, {})
                                        
                                        teacher_mean = teacher_val.get('mean', 0) if isinstance(teacher_val, dict) else 0
                                        student_mean = student_val.get('mean', 0) if isinstance(student_val, dict) else 0
                                        
                                        # คำนวณค่าเฉลี่ยรวม
                                        if teacher_mean > 0 and student_mean > 0:
                                            combined_mean = (teacher_mean + student_mean) / 2
                                        elif teacher_mean > 0:
                                            combined_mean = teacher_mean
                                        elif student_mean > 0:
                                            combined_mean = student_mean
                                        else:
                                            combined_mean = 0
                                        
                                        st.metric(
                                            f"{cat}", 
                                            f"{combined_mean:.2f}/5.0",
                                            help=f"ครู: {teacher_mean:.2f}, นักเรียน: {student_mean:.2f}"
                                        )
                        
                        st.markdown("---")
                        
                        # แสดง metadata แบบ JSON
                        st.markdown("##### 🔍 ข้อมูล Metadata (JSON)")
                        with st.expander("แสดงข้อมูล Metadata แบบละเอียด"):
                            metadata = db._load_data().get('metadata', {})
                            st.json(metadata)
                        
                        # แสดงคำแนะนำ
                        st.info("""
                        💡 **คำแนะนำ:** 
                        - ดาวน์โหลด JSON เพื่อดูข้อมูลแบบละเอียดทั้งหมด
                        - ดาวน์โหลด CSV เพื่อวิเคราะห์ด้วย Excel หรือ SPSS
                        - ข้อมูลเหล่านี้สามารถนำไปใช้ในการวิจัยหรือพัฒนาระบบต่อได้
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ ไม่สามารถแสดงข้อมูลสรุป: {str(e)}")
        
        except ImportError:
            st.error("❌ ไม่พบไฟล์ satisfaction_database.py")
            st.info("💡 ตรวจสอบว่ามีไฟล์ satisfaction_database.py ในโฟลเดอร์โปรเจคหรือไม่")
        except FileNotFoundError:
            st.error("❌ ไม่พบไฟล์ satisfaction_data.json")
            st.info("💡 ไฟล์นี้จะถูกสร้างขึ้นอัตโนมัติเมื่อมีผู้ทำแบบประเมินความพึงพอใจครั้งแรก")
    
    # ========== TAB 7: LOGOUT ==========
    with tab7:
        st.markdown("## 🚪 ออกจากระบบ")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""<div style="
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                border: 2px solid #ffc107;
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin: 2rem 0;
            ">
                <h3 style="color: #856404; margin: 0;">⚠️ คุณต้องการออกจากระบบหรือไม่?</h3>
            </div>""", unsafe_allow_html=True)
            
            st.markdown("""<div style="text-align: center; margin: 1rem 0;">
                <p style="font-size: 1.1rem; color: #666;">
                    หากคุณออกจากระบบ Admin คุณจะต้องเข้าสู่ระบบอีกครั้ง<br>
                    เพื่อเข้าถึงฟังก์ชันการจัดการระบบ
                </p>
            </div>""", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🚪 ยืนยันออกจากระบบ", type="primary", use_container_width=True, key="logout_admin"):
                    # ล้างข้อมูล session
                    st.session_state.admin_logged_in = False
                    st.session_state.admin_username = None
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    
                    st.success("✅ ออกจากระบบสำเร็จ!")
                    time.sleep(1)
                    
                    # กลับไปหน้าหลัก
                    st.markdown("""
                    <meta http-equiv="refresh" content="0; url=/" />
                    <script>
                        window.parent.location.href = '/';
                    </script>
                    """, unsafe_allow_html=True)
                    st.stop()
            
            with col_b:
                st.markdown("""
                <a href="/" target="_self">
                    <button style="
                        width: 100%;
                        padding: 0.5rem 1rem;
                        background: #6c757d;
                        color: white;
                        border: none;
                        border-radius: 12px;
                        font-family: 'Prompt', sans-serif;
                        font-size: 16px;
                        font-weight: 600;
                        cursor: pointer;
                        box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
                    ">
                        ❌ ยกเลิก
                    </button>
                </a>
                """, unsafe_allow_html=True)

# ========== FOOTER BUTTONS (ปุ่มด้านล่างสุด) ==========

