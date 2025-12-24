# 🚀 คู่มือการรัน Streamlit บน Server

## สำหรับ Linux Server (Ubuntu/Debian)

### ขั้นตอนที่ 1: เตรียม Server และติดตั้ง Python

```bash
# อัปเดตระบบ
sudo apt update
sudo apt upgrade -y

# ติดตั้ง Python 3 และ pip
sudo apt install python3 python3-pip python3-venv -y

# ตรวจสอบเวอร์ชัน
python3 --version
pip3 --version
```

---

### ขั้นตอนที่ 2: อัปโหลดไฟล์ขึ้น Server

**วิธีที่ 1: ใช้ SCP/SFTP**
```bash
# จากเครื่อง Local (Windows PowerShell)
scp -r C:\Users\User\Desktop\Project_AI_Grader user@project-ai.triamudomsouth.ac.th:/home/user/
```

**วิธีที่ 2: ใช้ FTP Client (FileZilla)**
- เชื่อมต่อ server ผ่าน SFTP
- อัปโหลดทั้งโฟลเดอร์ Project_AI_Grader

**วิธีที่ 3: ใช้ Git**
```bash
# บน Server
cd /var/www
sudo git clone <your-repo-url> Project_AI_Grader
cd Project_AI_Grader
```

---

### ขั้นตอนที่ 3: ติดตั้ง Dependencies บน Server

```bash
# เข้าไปในโฟลเดอร์โปรเจค
cd /home/user/Project_AI_Grader  # หรือ /var/www/Project_AI_Grader

# สร้าง Virtual Environment
python3 -m venv venv

# เปิดใช้งาน Virtual Environment
source venv/bin/activate

# ติดตั้ง packages จาก requirements.txt
pip install -r requirements.txt

# ตรวจสอบการติดตั้ง
pip list
```

---

### ขั้นตอนที่ 4: ตั้งค่า Environment Variables

```bash
# สร้างไฟล์ .env
nano .env

# ใส่ข้อมูลดังนี้:
GOOGLE_API_KEY=AIzaSyBo6hkCPcydSvtzwPLHYNqPiO-4mvNGy-Q
DATABASE_FILE=analysis.db

# บันทึก: Ctrl+X, Y, Enter
```

---

### ขั้นตอนที่ 5: รัน Streamlit แบบทดสอบ

```bash
# รันแบบพื้นฐาน (port 8501 default)
streamlit run student_view.py

# หรือระบุ port และ address เอง
streamlit run student_view.py --server.port=8501 --server.address=0.0.0.0

# ทดสอบเปิดในเบราว์เซอร์
# http://your-server-ip:8501
```

**หยุดการทำงาน:** กด `Ctrl+C`

---

### ขั้นตอนที่ 6: รัน Streamlit แบบ Background (Production)

**วิธีที่ 1: ใช้ nohup (ง่ายที่สุด)**
```bash
# รันเป็น background process
nohup streamlit run student_view.py --server.port=8501 --server.address=0.0.0.0 > streamlit.log 2>&1 &

# ดู process ID
ps aux | grep streamlit

# ดู log
tail -f streamlit.log

# หยุดการทำงาน (ใช้ PID จากคำสั่ง ps aux)
kill <PID>
```

**วิธีที่ 2: ใช้ screen (แนะนำ)**
```bash
# ติดตั้ง screen
sudo apt install screen -y

# สร้าง screen session ใหม่
screen -S streamlit

# รัน Streamlit
streamlit run student_view.py --server.port=8501 --server.address=0.0.0.0

# Detach จาก screen: กด Ctrl+A แล้วกด D

# กลับมาดู screen อีกครั้ง
screen -r streamlit

# ดูรายการ screen ทั้งหมด
screen -ls

# ปิด screen
# (อยู่ใน screen แล้วพิมพ์ exit หรือกด Ctrl+A แล้ว K)
```

**วิธีที่ 3: ใช้ systemd (แนะนำสำหรับ Production)**
```bash
# สร้างไฟล์ service
sudo nano /etc/systemd/system/streamlit-ai-grader.service

# ใส่เนื้อหาดังนี้:
[Unit]
Description=Streamlit AI Grader Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/Project_AI_Grader
Environment="PATH=/var/www/Project_AI_Grader/venv/bin"
ExecStart=/var/www/Project_AI_Grader/venv/bin/streamlit run student_view.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# บันทึก: Ctrl+X, Y, Enter

# Reload systemd
sudo systemctl daemon-reload

# เปิดใช้งาน service
sudo systemctl enable streamlit-ai-grader

# เริ่มต้น service
sudo systemctl start streamlit-ai-grader

# ตรวจสอบสถานะ
sudo systemctl status streamlit-ai-grader

# ดู log
sudo journalctl -u streamlit-ai-grader -f

# หยุดการทำงาน
sudo systemctl stop streamlit-ai-grader

# รีสตาร์ท
sudo systemctl restart streamlit-ai-grader
```

---

### ขั้นตอนที่ 7: ตั้งค่า Nginx (Reverse Proxy)

**ทำไมต้องใช้ Nginx?**
- ให้ Streamlit ทำงานบน domain หลัก (ไม่ต้องระบุ :8501)
- รองรับ HTTPS
- ปลอดภัยกว่า

**ติดตั้ง Nginx:**
```bash
sudo apt install nginx -y
```

**สร้าง Config:**
```bash
sudo nano /etc/nginx/sites-available/project-ai
```

**ใส่ Config นี้:**
```nginx
server {
    listen 80;
    server_name project-ai.triamudomsouth.ac.th;

    # Serve static files (index.html, landing.html)
    root /var/www/Project_AI_Grader;
    index index.html;

    # Streamlit WebSocket support
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Serve static HTML files
    location ~ \.(html)$ {
        root /var/www/Project_AI_Grader;
        try_files $uri $uri/ =404;
    }
}
```

**บันทึก และ Enable site:**
```bash
# สร้าง symbolic link
sudo ln -s /etc/nginx/sites-available/project-ai /etc/nginx/sites-enabled/

# ทดสอบ config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# ตรวจสอบสถานะ
sudo systemctl status nginx
```

---

### ขั้นตอนที่ 8: ตั้งค่า Firewall

```bash
# เปิด port HTTP (80) และ HTTPS (443)
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22  # SSH (ถ้ายังไม่ได้เปิด)

# ตรวจสอบสถานะ
sudo ufw status
```

---

### ขั้นตอนที่ 9: ตั้งค่า HTTPS (SSL Certificate)

**ใช้ Let's Encrypt (ฟรี):**
```bash
# ติดตั้ง Certbot
sudo apt install certbot python3-certbot-nginx -y

# ขอ SSL Certificate
sudo certbot --nginx -d project-ai.triamudomsouth.ac.th

# ทดสอบ auto-renewal
sudo certbot renew --dry-run
```

**Nginx จะถูก config ให้รองรับ HTTPS อัตโนมัติ**

---

## การตรวจสอบและแก้ไขปัญหา

### ตรวจสอบว่า Streamlit ทำงานอยู่หรือไม่
```bash
# ดู process
ps aux | grep streamlit

# ตรวจสอบ port
sudo netstat -tulpn | grep 8501

# หรือใช้
sudo lsof -i :8501
```

### ดู Log
```bash
# Log ของ Streamlit (ถ้าใช้ systemd)
sudo journalctl -u streamlit-ai-grader -n 100

# Log ของ Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### แก้ไขปัญหา Permission
```bash
# ให้สิทธิ์โฟลเดอร์
sudo chown -R www-data:www-data /var/www/Project_AI_Grader
sudo chmod -R 755 /var/www/Project_AI_Grader
```

### Restart Services
```bash
# Restart Streamlit
sudo systemctl restart streamlit-ai-grader

# Restart Nginx
sudo systemctl restart nginx
```

---

## 📝 Checklist สำหรับ Production

- [ ] Python 3 และ pip ติดตั้งแล้ว
- [ ] ไฟล์ทั้งหมดอัปโหลดขึ้น server แล้ว
- [ ] Virtual environment สร้างและติดตั้ง dependencies แล้ว
- [ ] ไฟล์ .env มี GOOGLE_API_KEY ถูกต้อง
- [ ] Streamlit รันได้และ accessible ที่ localhost:8501
- [ ] Systemd service สร้างและ enable แล้ว
- [ ] Nginx ติดตั้งและ config แล้ว
- [ ] Domain ชี้มาที่ server IP ถูกต้อง
- [ ] Firewall เปิด port 80, 443 แล้ว
- [ ] SSL Certificate ติดตั้งแล้ว (optional)

---

## 🎯 ขั้นตอนย่อสำหรับผู้เริ่มต้น

```bash
# 1. เข้า Server
ssh user@project-ai.triamudomsouth.ac.th

# 2. ไปที่โฟลเดอร์โปรเจค
cd /var/www/Project_AI_Grader

# 3. เปิด virtual environment
source venv/bin/activate

# 4. รัน Streamlit แบบง่าย (ทดสอบ)
streamlit run student_view.py --server.port=8501 --server.address=0.0.0.0

# 5. ถ้าทำงาน ให้ใช้ screen เพื่อรันแบบ background
screen -S streamlit
streamlit run student_view.py --server.port=8501 --server.address=0.0.0.0
# กด Ctrl+A แล้ว D เพื่อ detach

# 6. ตั้งค่า Nginx ตามขั้นตอนด้านบน
```

---

## 🆘 ช่วยเหลือเพิ่มเติม

หากมีปัญหา ตรวจสอบ:
1. **Log files** - `sudo journalctl -u streamlit-ai-grader -f`
2. **Port availability** - `sudo lsof -i :8501`
3. **Nginx config** - `sudo nginx -t`
4. **Permissions** - `ls -la /var/www/Project_AI_Grader`

---

**หมายเหตุ:** แนะนำให้ใช้ **screen** หรือ **systemd** สำหรับ production deployment
