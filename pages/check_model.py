import google.generativeai as genai

# 🔑 ใส่ API Key ของครูตรงนี้
API_KEY = "AIzaSyBjk4Amcrgk5SosIP1dtVBLLrirZld1Elc" 

genai.configure(api_key=API_KEY)

print("กำลังค้นหารายชื่อโมเดลที่ใช้ได้... (กรุณารอสักครู่)")
print("-" * 50)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ พบโมเดล: {m.name}")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")

print("-" * 50)
