#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
หน้าสรุปผลการประเมินความพึงพอใจ
Survey Results and Analytics Page
"""

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from satisfaction_database import SatisfactionDatabase
import json

# Page config
st.set_page_config(
    page_title="ผลการประเมินความพึงพอใจ",
    page_icon="📊",
    layout="wide",
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
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1.5rem;
        color: #B8879F !important;
        border: 2px solid #E8B4D4;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #E8B4D4 0%, #D4A5C8 100%) !important;
        color: white !important;
    }
    
    hr {
        background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%) !important;
        height: 3px !important;
        border: none !important;
        border-radius: 2px !important;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 2px solid #17a2b8;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
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

# Header
st.markdown("# 📊 ผลการประเมินความพึงพอใจในการใช้งานระบบ")
st.markdown("### ระบบตรวจโครงงาน AI - Dashboard วิเคราะห์ผลสำหรับการวิจัย")
st.markdown("---")

# Get metadata
metadata = satisfaction_db.get_metadata()
total_responses = metadata.get("total_responses", 0)
teacher_responses = metadata.get("teacher_responses", 0)
student_responses = metadata.get("student_responses", 0)

# Display summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📋 จำนวนผู้ตอบทั้งหมด", total_responses)
with col2:
    st.metric("👨‍🏫 ครู", teacher_responses)
with col3:
    st.metric("👨‍🎓 นักเรียน", student_responses)
with col4:
    if total_responses > 0:
        response_rate = (total_responses / 100) * 100  # สมมติว่ามีเป้าหมาย 100 คน
        st.metric("📈 อัตราการตอบกลับ", f"{response_rate:.1f}%")
    else:
        st.metric("📈 อัตราการตอบกลับ", "0%")

if total_responses == 0:
    st.markdown("""
    <div class="info-box">
        <h3>📝 ยังไม่มีข้อมูลการประเมิน</h3>
        <p>ยังไม่มีผู้ใช้ตอบแบบสอบถามความพึงพอใจ</p>
        <p>กรุณาเข้าไปทำแบบสอบถามที่หน้า <strong>Satisfaction Survey</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 ภาพรวม", "👨‍🏫 ครู", "👨‍🎓 นักเรียน", "📋 ข้อมูลดิบ"])

# ==================== Tab 1: ภาพรวม ====================
with tab1:
    st.markdown("## 📊 สรุปผลภาพรวม")
    
    # Calculate overall statistics
    overall_stats = satisfaction_db.calculate_statistics()
    teacher_stats = satisfaction_db.calculate_statistics("teacher")
    student_stats = satisfaction_db.calculate_statistics("student")
    
    # Display overall satisfaction
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if overall_stats:
            overall_mean = overall_stats.get("overall_mean", 0)
            satisfaction_level = satisfaction_db.get_satisfaction_level(overall_mean)
            st.metric(
                "ความพึงพอใจโดยรวม (ทั้งหมด)",
                f"{overall_mean:.2f}/5.00",
                delta=satisfaction_level
            )
    
    with col2:
        if teacher_stats:
            teacher_mean = teacher_stats.get("overall_mean", 0)
            satisfaction_level = satisfaction_db.get_satisfaction_level(teacher_mean)
            st.metric(
                "ความพึงพอใจครู",
                f"{teacher_mean:.2f}/5.00",
                delta=satisfaction_level
            )
    
    with col3:
        if student_stats:
            student_mean = student_stats.get("overall_mean", 0)
            satisfaction_level = satisfaction_db.get_satisfaction_level(student_mean)
            st.metric(
                "ความพึงพอใจนักเรียน",
                f"{student_mean:.2f}/5.00",
                delta=satisfaction_level
            )
    
    st.markdown("---")
    
    # Comparison bar chart
    if teacher_stats and student_stats:
        st.markdown("### 📊 เปรียบเทียบความพึงพอใจระหว่างครูและนักเรียน")
        
        fig = go.Figure(data=[
            go.Bar(
                name='ครู',
                x=['ความพึงพอใจโดยรวม'],
                y=[teacher_stats.get("overall_mean", 0)],
                marker_color='#E8B4D4',
                text=[f"{teacher_stats.get('overall_mean', 0):.2f}"],
                textposition='auto',
            ),
            go.Bar(
                name='นักเรียน',
                x=['ความพึงพอใจโดยรวม'],
                y=[student_stats.get("overall_mean", 0)],
                marker_color='#D4A5C8',
                text=[f"{student_stats.get('overall_mean', 0):.2f}"],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            barmode='group',
            title='เปรียบเทียบคะแนนความพึงพอใจเฉลี่ย',
            xaxis_title='กลุ่ม',
            yaxis_title='คะแนนเฉลี่ย (1-5)',
            yaxis_range=[0, 5],
            font=dict(family="Prompt", size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution chart
    st.markdown("### 📈 การกระจายของคะแนนความพึงพอใจ")
    
    all_surveys = satisfaction_db.get_all_surveys()
    all_scores = []
    
    for survey in all_surveys:
        responses = survey.get("responses", {})
        for key, value in responses.items():
            if isinstance(value, (int, float)) and value > 0:
                all_scores.append({
                    'user_type': 'ครู' if survey['user_type'] == 'teacher' else 'นักเรียน',
                    'score': value
                })
    
    if all_scores:
        df_scores = pd.DataFrame(all_scores)
        
        fig = px.histogram(
            df_scores,
            x='score',
            color='user_type',
            barmode='group',
            nbins=5,
            title='การกระจายของคะแนน (1-5)',
            labels={'score': 'คะแนน', 'user_type': 'กลุ่ม', 'count': 'จำนวน'},
            color_discrete_map={'ครู': '#E8B4D4', 'นักเรียน': '#D4A5C8'}
        )
        
        fig.update_layout(
            font=dict(family="Prompt", size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== Tab 2: ครู ====================
with tab2:
    st.markdown("## 👨‍🏫 ผลการประเมินความพึงพอใจของครู")
    
    if teacher_responses == 0:
        st.info("ยังไม่มีครูตอบแบบสอบถาม")
    else:
        teacher_stats = satisfaction_db.calculate_statistics("teacher")
        
        if teacher_stats:
            # Overall satisfaction
            teacher_mean = teacher_stats.get("overall_mean", 0)
            satisfaction_level = satisfaction_db.get_satisfaction_level(teacher_mean)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "ความพึงพอใจเฉลี่ย",
                    f"{teacher_mean:.2f}/5.00",
                    delta=satisfaction_level
                )
            with col2:
                st.metric("จำนวนผู้ตอบ", teacher_responses)
            
            st.markdown("---")
            
            # Detailed scores by category
            st.markdown("### 📊 คะแนนแยกตามหมวดหมู่")
            
            categories = teacher_stats.get("categories", {})
            
            # Group by category
            usability_scores = {}
            effectiveness_scores = {}
            adoption_scores = {}
            overall_scores = {}
            
            for key, data in categories.items():
                if key.startswith("usability_"):
                    usability_scores[key] = data
                elif key.startswith("effectiveness_"):
                    effectiveness_scores[key] = data
                elif key.startswith("adoption_"):
                    adoption_scores[key] = data
                elif key.startswith("overall_"):
                    overall_scores[key] = data
            
            # Display categories
            col1, col2 = st.columns(2)
            
            with col1:
                if usability_scores:
                    st.markdown("#### 1️⃣ ด้านการใช้งาน")
                    avg_usability = sum(d["mean"] for d in usability_scores.values()) / len(usability_scores)
                    st.metric("คะแนนเฉลี่ย", f"{avg_usability:.2f}/5.00")
                    
                    for key, data in usability_scores.items():
                        st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
                
                if adoption_scores:
                    st.markdown("#### 3️⃣ ด้านการนำไปใช้")
                    avg_adoption = sum(d["mean"] for d in adoption_scores.values()) / len(adoption_scores)
                    st.metric("คะแนนเฉลี่ย", f"{avg_adoption:.2f}/5.00")
                    
                    for key, data in adoption_scores.items():
                        st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
            
            with col2:
                if effectiveness_scores:
                    st.markdown("#### 2️⃣ ด้านประสิทธิภาพ")
                    avg_effectiveness = sum(d["mean"] for d in effectiveness_scores.values()) / len(effectiveness_scores)
                    st.metric("คะแนนเฉลี่ย", f"{avg_effectiveness:.2f}/5.00")
                    
                    for key, data in effectiveness_scores.items():
                        st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
                
                if overall_scores:
                    st.markdown("#### 4️⃣ ความพึงพอใจโดยรวม")
                    avg_overall = sum(d["mean"] for d in overall_scores.values()) / len(overall_scores)
                    st.metric("คะแนนเฉลี่ย", f"{avg_overall:.2f}/5.00")
                    
                    for key, data in overall_scores.items():
                        st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
            
            # Radar chart
            st.markdown("### 🎯 กราฟเรดาร์แสดงความพึงพอใจแต่ละด้าน (ครู)")
            
            category_means = []
            category_names = []
            
            if usability_scores:
                avg_usability = sum(d["mean"] for d in usability_scores.values()) / len(usability_scores)
                category_means.append(avg_usability)
                category_names.append("การใช้งาน")
            
            if effectiveness_scores:
                avg_effectiveness = sum(d["mean"] for d in effectiveness_scores.values()) / len(effectiveness_scores)
                category_means.append(avg_effectiveness)
                category_names.append("ประสิทธิภาพ")
            
            if adoption_scores:
                avg_adoption = sum(d["mean"] for d in adoption_scores.values()) / len(adoption_scores)
                category_means.append(avg_adoption)
                category_names.append("การนำไปใช้")
            
            if overall_scores:
                avg_overall = sum(d["mean"] for d in overall_scores.values()) / len(overall_scores)
                category_means.append(avg_overall)
                category_names.append("โดยรวม")
            
            if category_means:
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=category_means + [category_means[0]],  # Close the shape
                    theta=category_names + [category_names[0]],
                    fill='toself',
                    fillcolor='rgba(232, 180, 212, 0.5)',
                    line=dict(color='#E8B4D4', width=2),
                    name='ครู'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )
                    ),
                    showlegend=True,
                    font=dict(family="Prompt", size=14),
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Suggestions
            st.markdown("### 💬 ข้อเสนอแนะจากครู")
            teacher_surveys = satisfaction_db.get_surveys_by_type("teacher")
            
            suggestions = []
            for survey in teacher_surveys:
                suggestion = survey.get("responses", {}).get("suggestion", "")
                if suggestion and suggestion.strip():
                    suggestions.append({
                        "name": survey.get("name", "ไม่ระบุ"),
                        "date": survey.get("created_at", ""),
                        "text": suggestion
                    })
            
            if suggestions:
                for i, sug in enumerate(suggestions, 1):
                    with st.expander(f"💡 ข้อเสนอแนะ #{i} - {sug['name']} ({sug['date']})"):
                        st.write(sug['text'])
            else:
                st.info("ไม่มีข้อเสนอแนะเพิ่มเติม")

# ==================== Tab 3: นักเรียน ====================
with tab3:
    st.markdown("## 👨‍🎓 ผลการประเมินความพึงพอใจของนักเรียน")
    
    if student_responses == 0:
        st.info("ยังไม่มีนักเรียนตอบแบบสอบถาม")
    else:
        student_stats = satisfaction_db.calculate_statistics("student")
        
        if student_stats:
            # Overall satisfaction
            student_mean = student_stats.get("overall_mean", 0)
            satisfaction_level = satisfaction_db.get_satisfaction_level(student_mean)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "ความพึงพอใจเฉลี่ย",
                    f"{student_mean:.2f}/5.00",
                    delta=satisfaction_level
                )
            with col2:
                st.metric("จำนวนผู้ตอบ", student_responses)
            
            st.markdown("---")
            
            # Detailed scores by category
            st.markdown("### 📊 คะแนนแยกตามหมวดหมู่")
            
            categories = student_stats.get("categories", {})
            
            # Group by category
            usability_scores = {}
            benefits_scores = {}
            overall_scores = {}
            
            for key, data in categories.items():
                if key.startswith("usability_"):
                    usability_scores[key] = data
                elif key.startswith("benefits_"):
                    benefits_scores[key] = data
                elif key.startswith("overall_"):
                    overall_scores[key] = data
            
            # Display categories
            col1, col2 = st.columns(2)
            
            with col1:
                if usability_scores:
                    st.markdown("#### 1️⃣ ด้านการใช้งาน")
                    avg_usability = sum(d["mean"] for d in usability_scores.values()) / len(usability_scores)
                    st.metric("คะแนนเฉลี่ย", f"{avg_usability:.2f}/5.00")
                    
                    for key, data in usability_scores.items():
                        st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
            
            with col2:
                if benefits_scores:
                    st.markdown("#### 2️⃣ ด้านประโยชน์ที่ได้รับ")
                    avg_benefits = sum(d["mean"] for d in benefits_scores.values()) / len(benefits_scores)
                    st.metric("คะแนนเฉลี่ย", f"{avg_benefits:.2f}/5.00")
                    
                    for key, data in benefits_scores.items():
                        st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
            
            if overall_scores:
                st.markdown("#### 3️⃣ ความพึงพอใจโดยรวม")
                avg_overall = sum(d["mean"] for d in overall_scores.values()) / len(overall_scores)
                st.metric("คะแนนเฉลี่ย", f"{avg_overall:.2f}/5.00")
                
                for key, data in overall_scores.items():
                    st.write(f"• {data['mean']:.2f}/5.00 ({data['count']} คน)")
            
            # Radar chart
            st.markdown("### 🎯 กราฟเรดาร์แสดงความพึงพอใจแต่ละด้าน (นักเรียน)")
            
            category_means = []
            category_names = []
            
            if usability_scores:
                avg_usability = sum(d["mean"] for d in usability_scores.values()) / len(usability_scores)
                category_means.append(avg_usability)
                category_names.append("การใช้งาน")
            
            if benefits_scores:
                avg_benefits = sum(d["mean"] for d in benefits_scores.values()) / len(benefits_scores)
                category_means.append(avg_benefits)
                category_names.append("ประโยชน์")
            
            if overall_scores:
                avg_overall = sum(d["mean"] for d in overall_scores.values()) / len(overall_scores)
                category_means.append(avg_overall)
                category_names.append("โดยรวม")
            
            if category_means:
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=category_means + [category_means[0]],  # Close the shape
                    theta=category_names + [category_names[0]],
                    fill='toself',
                    fillcolor='rgba(212, 165, 200, 0.5)',
                    line=dict(color='#D4A5C8', width=2),
                    name='นักเรียน'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )
                    ),
                    showlegend=True,
                    font=dict(family="Prompt", size=14),
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Suggestions
            st.markdown("### 💬 ข้อเสนอแนะจากนักเรียน")
            student_surveys = satisfaction_db.get_surveys_by_type("student")
            
            suggestions = []
            for survey in student_surveys:
                suggestion = survey.get("responses", {}).get("suggestion", "")
                if suggestion and suggestion.strip():
                    suggestions.append({
                        "name": survey.get("name", "ไม่ระบุ"),
                        "date": survey.get("created_at", ""),
                        "text": suggestion
                    })
            
            if suggestions:
                for i, sug in enumerate(suggestions, 1):
                    with st.expander(f"💡 ข้อเสนอแนะ #{i} - {sug['name']} ({sug['date']})"):
                        st.write(sug['text'])
            else:
                st.info("ไม่มีข้อเสนอแนะเพิ่มเติม")

# ==================== Tab 4: ข้อมูลดิบ ====================
with tab4:
    st.markdown("## 📋 ข้อมูลดิบสำหรับการวิจัย")
    
    # Export button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📥 ส่งออกข้อมูล JSON"):
            export_data = satisfaction_db.export_for_research()
            
            # Convert to JSON string
            import json
            json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
            
            st.download_button(
                label="💾 ดาวน์โหลด JSON",
                data=json_str,
                file_name=f"satisfaction_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 ส่งออกข้อมูล CSV"):
            all_surveys = satisfaction_db.get_all_surveys()
            
            # Flatten data for CSV
            csv_data = []
            for survey in all_surveys:
                row = {
                    "ID": survey.get("id", ""),
                    "วันที่": survey.get("created_at", ""),
                    "ประเภท": "ครู" if survey.get("user_type") == "teacher" else "นักเรียน",
                    "ชื่อผู้ใช้": survey.get("username", ""),
                    "ชื่อ": survey.get("name", "")
                }
                
                # Add responses
                responses = survey.get("responses", {})
                for key, value in responses.items():
                    row[key] = value
                
                csv_data.append(row)
            
            if csv_data:
                df_csv = pd.DataFrame(csv_data)
                csv_string = df_csv.to_csv(index=False, encoding='utf-8-sig')
                
                st.download_button(
                    label="💾 ดาวน์โหลด CSV",
                    data=csv_string,
                    file_name=f"satisfaction_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    st.markdown("---")
    
    # Display raw data table
    st.markdown("### 📊 ตารางข้อมูลทั้งหมด")
    
    all_surveys = satisfaction_db.get_all_surveys()
    
    if all_surveys:
        # Create DataFrame
        table_data = []
        for survey in all_surveys:
            responses = survey.get("responses", {})
            
            # Calculate average score
            numeric_responses = {k: v for k, v in responses.items() if isinstance(v, (int, float)) and v > 0}
            avg_score = sum(numeric_responses.values()) / len(numeric_responses) if numeric_responses else 0
            
            table_data.append({
                "วันที่": survey.get("created_at", ""),
                "ประเภท": "ครู" if survey.get("user_type") == "teacher" else "นักเรียน",
                "ชื่อ": survey.get("name", ""),
                "คะแนนเฉลี่ย": f"{avg_score:.2f}",
                "ระดับ": satisfaction_db.get_satisfaction_level(avg_score)
            })
        
        df_table = pd.DataFrame(table_data)
        st.dataframe(df_table, use_container_width=True)
        
        st.markdown("---")
        
        # Display detailed responses
        st.markdown("### 🔍 ข้อมูลรายละเอียด")
        
        for i, survey in enumerate(all_surveys, 1):
            user_type = "ครู" if survey.get("user_type") == "teacher" else "นักเรียน"
            with st.expander(f"#{i} - {user_type}: {survey.get('name', '')} ({survey.get('created_at', '')})"):
                responses = survey.get("responses", {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**คะแนนที่ให้:**")
                    for key, value in responses.items():
                        if isinstance(value, (int, float)) and value > 0:
                            st.write(f"• {key}: {value}/5")
                
                with col2:
                    suggestion = responses.get("suggestion", "")
                    if suggestion and suggestion.strip():
                        st.write("**ข้อเสนอแนะ:**")
                        st.info(suggestion)
                    else:
                        st.write("**ข้อเสนอแนะ:**")
                        st.write("ไม่มี")
    else:
        st.info("ยังไม่มีข้อมูล")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #B8879F; padding: 1rem;">
    <p>📊 Dashboard นี้ออกแบบมาเพื่อการวิจัยและพัฒนาระบบ</p>
    <p style="font-size: 0.9rem;">ระบบตรวจโครงงาน AI | พัฒนาโดย ครูอภิรมย์ กึกก้อง</p>
</div>
""", unsafe_allow_html=True)
