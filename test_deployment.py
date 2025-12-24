#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Deployment - ทดสอบว่า Streamlit รันได้หรือไม่
"""

import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Test Deployment",
    page_icon="✅",
    layout="wide"
)

st.title("✅ ระบบทำงานปกติ")
st.success("Streamlit กำลังทำงาน!")

st.markdown("---")
st.subheader("🔍 ข้อมูลระบบ")

col1, col2 = st.columns(2)

with col1:
    st.write("**Python Version:**", sys.version)
    st.write("**Streamlit Version:**", st.__version__)
    st.write("**Working Directory:**", os.getcwd())

with col2:
    st.write("**ไฟล์ที่มีในโฟลเดอร์:**")
    files = os.listdir(".")
    for f in sorted(files)[:10]:
        st.write(f"- {f}")

st.markdown("---")
st.subheader("📁 ตรวจสอบไฟล์สำคัญ")

important_files = [
    "Home.py",
    "Procfile",
    "requirements.txt",
    "runtime.txt",
    ".streamlit/config.toml"
]

for file in important_files:
    if os.path.exists(file):
        st.success(f"✅ {file} - พบแล้ว")
    else:
        st.error(f"❌ {file} - ไม่พบ")

st.markdown("---")
st.info("💡 ถ้าเห็นหน้านี้ แสดงว่า Streamlit ทำงานได้ปกติ")
