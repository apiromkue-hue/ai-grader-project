# 🔄 คำสั่งอัปเดต Server ให้แสดงหน้า Home.py

## ⚠️ ปัญหาที่พบ
Server ยังรัน `student_view.py` แทนที่จะรัน `Home.py` (หน้าหลักใหม่)

---

## ✅ วิธีแก้ไข (ต้องรันบน Server)

### วิธีที่ 1: หยุด Streamlit เดิมและรันใหม่

```bash
# 1. เข้า SSH ไปที่ server
ssh user@project-ai.triamudomsouth.ac.th

# 2. หาและหยุด process เดิม
ps aux | grep streamlit
kill <PID_ของ_streamlit>

# หรือหยุดทั้งหมด
pkill -f streamlit

# 3. เข้าโฟลเดอร์โปรเจค
cd /var/www/Project_AI_Grader
# หรือ
cd /home/user/Project_AI_Grader

# 4. เปิด Virtual Environment
source venv/bin/activate

# 5. รัน Home.py แทน (แบบ background)
nohup streamlit run Home.py --server.port=8501 --server.address=0.0.0.0 > streamlit.log 2>&1 &

# 6. ตรวจสอบว่ารันอยู่
ps aux | grep streamlit

# 7. ดู log ถ้ามีปัญหา
tail -f streamlit.log
```

---

### วิธีที่ 2: ใช้ systemd (ถ้ามี service ตั้งไว้)

```bash
# 1. หยุด service เดิม
sudo systemctl stop streamlit-ai-grader

# 2. แก้ไขไฟล์ service
sudo nano /etc/systemd/system/streamlit-ai-grader.service

# 3. เปลี่ยนบรรทัดนี้:
# จาก: ExecStart=...streamlit run student_view.py...
# เป็น: ExecStart=...streamlit run Home.py...

# ตัวอย่าง:
ExecStart=/var/www/Project_AI_Grader/venv/bin/streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

# 4. บันทึก (Ctrl+X, Y, Enter)

# 5. Reload systemd
sudo systemctl daemon-reload

# 6. เริ่ม service ใหม่
sudo systemctl start streamlit-ai-grader

# 7. ตรวจสอบสถานะ
sudo systemctl status streamlit-ai-grader

# 8. ดู log
sudo journalctl -u streamlit-ai-grader -f
```

---

### วิธีที่ 3: ใช้ screen (ถ้ารันด้วย screen)

```bash
# 1. ดู screen sessions ทั้งหมด
screen -ls

# 2. เข้าไปใน screen ที่รัน streamlit
screen -r streamlit
# หรือ
screen -r <screen_id>

# 3. หยุดโปรแกรม (กด Ctrl+C)

# 4. รันใหม่ด้วย Home.py
cd /var/www/Project_AI_Grader
source venv/bin/activate
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

# 5. Detach จาก screen (กด Ctrl+A แล้วกด D)
```

---

## 🔍 ตรวจสอบว่าใช้ไฟล์ถูกต้อง

```bash
# เข้า server
ssh user@project-ai.triamudomsouth.ac.th

# ดู process ที่รันอยู่
ps aux | grep streamlit

# จะเห็นคำสั่งเต็มๆ เช่น:
# streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
```

---

## 📦 ไฟล์ที่ต้องอัปโหลดขึ้น Server (ถ้ายังไม่ได้ upload)

อัปโหลดไฟล์เหล่านี้ไปแทนที่บน server:
- ✅ `Home.py`
- ✅ `pages/2_Admin_Panel.py`
- ✅ `Procfile` (ถ้าใช้ Heroku/ระบบที่อ่าน Procfile)
- ✅ `Dockerfile` (ถ้าใช้ Docker)

---

## 🚨 ถ้ายังไม่ได้ผล

### ตรวจสอบ Nginx (ถ้ามี)

```bash
# ดู nginx config
sudo nano /etc/nginx/sites-available/streamlit-ai-grader

# หา proxy_pass ต้องชี้ไปที่ port ที่ streamlit รันอยู่
# proxy_pass http://localhost:8501;

# Restart nginx
sudo systemctl restart nginx
```

### ตรวจสอบ Firewall

```bash
# ตรวจสอบว่า port 8501 เปิดอยู่
sudo ufw status

# เปิด port (ถ้าจำเป็น)
sudo ufw allow 8501
```

### ดู Error Log

```bash
# ดู log ของ streamlit
tail -f streamlit.log

# หรือถ้าใช้ systemd
sudo journalctl -u streamlit-ai-grader -n 50 --no-pager
```

---

## ✅ หลังแก้ไข

เข้าเว็บ: `https://project-ai.triamudomsouth.ac.th/`

ควรเห็น:
- ✨ หน้า Home ใหม่พร้อม SVG icon
- 📦 Grid cards 6 ฟีเจอร์
- 📖 คู่มือการใช้งาน 2 cards
- 👥 Footer จัดกึ่งกลาง

---

## 📞 สำหรับผู้ดูแล Server

ถ้าไม่แน่ใจว่า server ใช้วิธีไหน ให้รันคำสั่งนี้:

```bash
# ดูว่ามี systemd service หรือไม่
sudo systemctl list-units | grep streamlit

# ดูว่ามี screen หรือไม่
screen -ls

# ดูว่ามี process ใดรันอยู่
ps aux | grep streamlit

# ดูว่ามี nginx หรือไม่
sudo systemctl status nginx
```

จากผลลัพธ์จะรู้ว่าใช้วิธีไหนในการรัน แล้วใช้วิธีแก้ไขที่ตรงกัน
