#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แบบประเมินความพึงพอใจในการใช้งานระบบ
Satisfaction Survey Page
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from satisfaction_database import SatisfactionDatabase
import json

# Page config
st.set_page_config(
    page_title="แบบประเมินความพึงพอใจ",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with K-Minimal Design
st.markdown("""
<style>
    * {
        font-family: 'Prompt', sans-serif !important;
    }
    
    body {
        background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%) !important;
    }
    
    h1, h2, h3 {
        color: #D4A5C8 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(212, 165, 200, 0.4) !important;
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5E8F0 100%) !important;
        border: 1px solid #E8B4D4 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    
    .stRadio > label {
        color: #B8879F !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid #E8B4D4 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #D4A5C8 !important;
        box-shadow: 0 0 0 2px rgba(212, 165, 200, 0.2) !important;
    }
    
    hr {
        background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
        height: 3px !important;
        border: none !important;
        border-radius: 2px !important;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 2px solid #17a2b8;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Initialize databases
satisfaction_db = SatisfactionDatabase()

# Load users function
def load_users():
    try:
        with open('users_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('users', [])
    except:
        return []

def get_user(username):
    users = load_users()
    for user in users:
        if user.get('username') == username:
            return user
    return None

# Check login - รองรับทั้ง logged_in และ student_logged_in
is_logged_in = (
    (st.session_state.get('logged_in', False)) or 
    (st.session_state.get('student_logged_in', False))
)

if not is_logged_in:
    st.markdown('<div class="warning-box"><h3>⚠️ กรุณาเข้าสู่ระบบก่อนใช้งาน</h3></div>', unsafe_allow_html=True)
    st.info("👉 กลับไปที่หน้าหลักเพื่อเข้าสู่ระบบ")
    st.stop()

# Get user info - รองรับทั้ง username และ student_username
username = st.session_state.get('username', '') or st.session_state.get('student_username', '')
user_data = get_user(username)

if not user_data:
    st.error("ไม่พบข้อมูลผู้ใช้")
    st.stop()

user_role = user_data.get('role', 'student')
user_name = user_data.get('name', username)

# Header
st.markdown("# 📋 แบบประเมินความพึงพอใจในการใช้งานระบบ")
st.markdown("### ระบบตรวจโครงงาน AI")
st.markdown("---")

# Check if already responded
if satisfaction_db.check_if_user_responded(username):
    st.markdown("""
    <div class="success-box">
        <h3>✅ คุณได้ทำแบบสอบถามไปแล้ว</h3>
        <p>ขอบคุณสำหรับความคิดเห็นของคุณ ข้อมูลจะถูกนำไปใช้ในการพัฒนาระบบต่อไป</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📊 ดูผลสรุปการประเมินได้ที่หน้า **Survey Results**")
    st.stop()

# Display user info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("ชื่อผู้ใช้", username)
with col2:
    role_thai = "ครู" if user_role == "teacher" else "นักเรียน"
    st.metric("บทบาท", role_thai)
with col3:
    st.metric("ชื่อ", user_name)

st.markdown("---")

# Introduction
st.markdown("""
<div class="info-box">
    <h4>📝 วัตถุประสงค์ของแบบสอบถาม</h4>
    <p>แบบสอบถามนี้มีวัตถุประสงค์เพื่อ:</p>
    <ul>
        <li>ประเมินความพึงพอใจในการใช้งานระบบตรวจโครงงาน AI</li>
        <li>รับฟังข้อคิดเห็นและข้อเสนอแนะเพื่อการพัฒนา</li>
        <li>นำข้อมูลไปใช้ในการวิจัยและพัฒนาระบบให้ดีขึ้น</li>
    </ul>
    <p><strong>⏱️ ใช้เวลาประมาณ 5-7 นาที</strong></p>
</div>
""", unsafe_allow_html=True)

st.markdown("### กรุณาให้คะแนนความพึงพอใจในแต่ละด้าน")
st.markdown("**เกณฑ์การให้คะแนน:** 5 = มากที่สุด, 4 = มาก, 3 = ปานกลาง, 2 = น้อย, 1 = น้อยที่สุด")

# Survey questions (แยกตามบทบาท)
if user_role == "teacher":
    # คำถามสำหรับครู
    st.markdown("## 👨‍🏫 ความพึงพอใจของครู")
    
    st.markdown("### 1️⃣ ด้านการใช้งาน (Usability)")
    q1 = st.radio(
        "1.1 ระบบมีความสะดวกในการใช้งาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q1"
    )
    
    q2 = st.radio(
        "1.2 ระบบมีการจัดวางเมนูและฟังก์ชันที่เข้าใจง่าย",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q2"
    )
    
    q3 = st.radio(
        "1.3 ระบบสามารถใช้งานได้รวดเร็ว (Performance)",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q3"
    )
    
    st.markdown("### 2️⃣ ด้านประสิทธิภาพ (Effectiveness)")
    q4 = st.radio(
        "2.1 AI สามารถวิเคราะห์โครงงานได้อย่างถูกต้องแม่นยำ",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q4"
    )
    
    q5 = st.radio(
        "2.2 ข้อเสนอแนะจาก AI มีประโยชน์ต่อการปรับปรุงโครงงาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q5"
    )
    
    q6 = st.radio(
        "2.3 ระบบช่วยลดเวลาในการตรวจโครงงาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q6"
    )
    
    q7 = st.radio(
        "2.4 ระบบช่วยเพิ่มคุณภาพการให้ Feedback แก่นักเรียน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q7"
    )
    
    st.markdown("### 3️⃣ ด้านการนำไปใช้ (Adoption)")
    q8 = st.radio(
        "3.1 ท่านมีความมั่นใจในการนำระบบไปใช้ในการสอนจริง",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q8"
    )
    
    q9 = st.radio(
        "3.2 ท่านจะแนะนำระบบนี้ให้เพื่อนครูคนอื่นใช้",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q9"
    )
    
    st.markdown("### 4️⃣ ด้านความพึงพอใจโดยรวม")
    q10 = st.radio(
        "4.1 ท่านมีความพึงพอใจในการใช้งานระบบโดยรวม",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q10"
    )
    
    # ข้อเสนอแนะ
    st.markdown("### 💬 ข้อเสนอแนะเพิ่มเติม")
    suggestion = st.text_area(
        "กรุณาแสดงความคิดเห็นหรือข้อเสนอแนะในการพัฒนาระบบ",
        placeholder="ระบบควรมีฟีเจอร์อะไรเพิ่มเติม? หรือมีจุดใดที่ควรปรับปรุง?",
        height=150,
        key="suggestion"
    )
    
    # Collect responses
    responses = {
        "usability_easy_to_use": q1,
        "usability_menu_layout": q2,
        "usability_performance": q3,
        "effectiveness_accuracy": q4,
        "effectiveness_feedback_quality": q5,
        "effectiveness_time_saving": q6,
        "effectiveness_feedback_improvement": q7,
        "adoption_confidence": q8,
        "adoption_recommendation": q9,
        "overall_satisfaction": q10,
        "suggestion": suggestion
    }

else:  # student
    # คำถามสำหรับนักเรียน
    st.markdown("## 👨‍🎓 ความพึงพอใจของนักเรียน")
    
    st.markdown("### 1️⃣ ด้านการใช้งาน (Usability)")
    q1 = st.radio(
        "1.1 ระบบมีความสะดวกในการใช้งาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q1"
    )
    
    q2 = st.radio(
        "1.2 ระบบมีการจัดวางเมนูและฟังก์ชันที่เข้าใจง่าย",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q2"
    )
    
    q3 = st.radio(
        "1.3 การอัพโหลดไฟล์และรับผลวิเคราะห์ทำได้ง่าย",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q3"
    )
    
    st.markdown("### 2️⃣ ด้านประโยชน์ที่ได้รับ (Benefits)")
    q4 = st.radio(
        "2.1 ผลวิเคราะห์จาก AI ช่วยให้เข้าใจจุดบกพร่องของโครงงาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q4"
    )
    
    q5 = st.radio(
        "2.2 ข้อเสนอแนะจาก AI มีประโยชน์ในการปรับปรุงโครงงาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q5"
    )
    
    q6 = st.radio(
        "2.3 ระบบช่วยให้เรียนรู้วิธีการเขียนโครงงานที่ดีขึ้น",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q6"
    )
    
    q7 = st.radio(
        "2.4 ระบบช่วยเพิ่มความมั่นใจในการทำโครงงาน",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q7"
    )
    
    st.markdown("### 3️⃣ ด้านความพึงพอใจโดยรวม")
    q8 = st.radio(
        "3.1 ท่านมีความพึงพอใจในการใช้งานระบบโดยรวม",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q8"
    )
    
    q9 = st.radio(
        "3.2 ท่านจะแนะนำให้เพื่อนใช้ระบบนี้",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: f"{x} - {'มากที่สุด' if x==5 else 'มาก' if x==4 else 'ปานกลาง' if x==3 else 'น้อย' if x==2 else 'น้อยที่สุด'}",
        key="q9"
    )
    
    # ข้อเสนอแนะ
    st.markdown("### 💬 ข้อเสนอแนะเพิ่มเติม")
    suggestion = st.text_area(
        "กรุณาแสดงความคิดเห็นหรือข้อเสนอแนะในการพัฒนาระบบ",
        placeholder="อยากให้ระบบมีฟีเจอร์อะไรเพิ่มเติม? หรือมีจุดใดที่ควรปรับปรุง?",
        height=150,
        key="suggestion"
    )
    
    # Collect responses
    responses = {
        "usability_easy_to_use": q1,
        "usability_menu_layout": q2,
        "usability_upload_ease": q3,
        "benefits_understanding": q4,
        "benefits_improvement": q5,
        "benefits_learning": q6,
        "benefits_confidence": q7,
        "overall_satisfaction": q8,
        "overall_recommendation": q9,
        "suggestion": suggestion
    }

# Submit button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📤 ส่งแบบประเมิน", use_container_width=True):
        # Validate
        has_empty = False
        for key, value in responses.items():
            if key != "suggestion" and (value is None or value == 0):
                has_empty = True
                break
        
        if has_empty:
            st.error("⚠️ กรุณาตอบคำถามให้ครบทุกข้อ")
        else:
            # Save to database
            success = satisfaction_db.add_survey_response(
                user_type=user_role,
                username=username,
                name=user_name,
                responses=responses
            )
            
            if success:
                st.markdown("""
                <div class="success-box">
                    <h3>✅ ส่งแบบประเมินสำเร็จ</h3>
                    <p>ขอบคุณสำหรับความคิดเห็นของคุณ ข้อมูลจะถูกนำไปใช้ในการพัฒนาระบบต่อไป</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
                # Calculate average score
                numeric_responses = {k: v for k, v in responses.items() if isinstance(v, (int, float)) and v > 0}
                if numeric_responses:
                    avg_score = sum(numeric_responses.values()) / len(numeric_responses)
                    satisfaction_level = satisfaction_db.get_satisfaction_level(avg_score)
                    
                    st.info(f"📊 คะแนนเฉลี่ยของคุณ: **{avg_score:.2f}/5.00** (ระดับความพึงพอใจ: **{satisfaction_level}**)")
                
                st.success("🔍 ดูผลสรุปการประเมินทั้งหมดได้ที่หน้า **Survey Results**")
                
            else:
                st.error("❌ เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่อีกครั้ง")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #B8879F; padding: 1rem;">
    <p>🔒 ข้อมูลของคุณจะถูกเก็บเป็นความลับและใช้เพื่อการวิจัยเท่านั้น</p>
    <p style="font-size: 0.9rem;">ระบบตรวจโครงงาน AI | พัฒนาโดย ครูอภิรมย์ กึกก้อง</p>
</div>
""", unsafe_allow_html=True)
