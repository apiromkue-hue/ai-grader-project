import sys
import subprocess
import time

# --- 🛠️ ส่วนซ่อมแซมตัวเอง (Auto-Fix System) ---
print("กำลังตรวจสอบระบบ... (Checking System...)")

def install_package(package_name):
    try:
        print(f"⏳ กำลังติดตั้ง: {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ ติดตั้ง {package_name} สำเร็จ!")
    except:
        print(f"❌ ติดตั้ง {package_name} ไม่สำเร็จ")

# เช็คและติดตั้ง google-generativeai
try:
    import google.generative_ai as genai
except ImportError:
    print("⚠️ ไม่พบเครื่องมือ AI -> กำลังติดตั้งให้เดี๋ยวนี้ครับ...")
    install_package("google-generativeai")
    import google.generative_ai as genai

# เช็คและติดตั้ง streamlit
try:
    import streamlit as st
except ImportError:
    install_package("streamlit")

# เช็คและติดตั้งตัวอ่านไฟล์
try:
    import PyPDF2
    from docx import Document
except ImportError:
    install_package("PyPDF2")
    install_package("python-docx")

print("-" * 50)
print("✅ ระบบพร้อมใช้งานแล้ว! (System Ready)")
print("-" * 50)

# --- 🚀 ส่วนการทำงานหลัก (Main Code) ---

# 🔑 ใส่ API KEY ของครูตรงนี้
API_KEY = "AIzaSyA8h77ZPpcI0c4ar2GeKQ0kPjGWKu4dk50"  # <--- อย่าลืมแก้ตรงนี้นะครับ

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # ทดสอบถาม AI
    print("\n🤖 AI กำลังคิดคำตอบ...")
    response = model.generate_content("ขอกำลังใจสั้นๆ ให้ครูคอมพิวเตอร์ที่กำลังแก้บั๊กโปรแกรมอยู่หน่อยครับ")
    print(f"💬 AI ตอบกลับมาว่า:\n{response.text}")

except Exception as e:
    print(f"❌ Error: {e}")

    print("👉 (ถ้า Error เรื่อง API Key ให้เช็คบรรทัดที่ 45 นะครับ)")
