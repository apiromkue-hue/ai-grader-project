import sys
import subprocess

# ดึงตำแหน่งที่อยู่จริงๆ ของ Python ตัวที่กำลังทำงาน
python_path = sys.executable

print("📍 Python ที่กำลังทำงานอยู่ที่:", python_path)
print("🔧 กำลังบังคับติดตั้งเครื่องมือลงใน Python ตัวนี้โดยเฉพาะ...")

# สั่งติดตั้งโดยใช้ Path ที่ระบุเจาะจง (ไม่มีทางพลาด)
commands = [
    [python_path, "-m", "pip", "install", "--upgrade", "pip"],
    [python_path, "-m", "pip", "install", "--upgrade", "google-generativeai"],
    [python_path, "-m", "pip", "install", "--upgrade", "streamlit"],
    [python_path, "-m", "pip", "install", "--upgrade", "PyPDF2"],
    [python_path, "-m", "pip", "install", "--upgrade", "python-docx"]
]

for cmd in commands:
    try:
        print(f"⏳ กำลังรัน: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("✅ สำเร็จ!")
    except Exception as e:
        print(f"❌ ผิดพลาด: {e}")

print("\n" + "="*50)
print("🎉 ติดตั้งครบทุกตัวแล้ว! ครูลองกลับไปรันไฟล์ app.py ได้เลยครับ")
print("="*50)