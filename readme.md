# AI Project Grader System - Complete Documentation

## 🎓 Overview

**AI Project Grader System** เป็นระบบตรวจความสอดคล้องของโครงงานโดยใช้ AI (Google Gemini) ในการวิเคราะห์เอกสารอัตโนมัติ

---

## ✨ Main Features

### 👨‍🎓 Student Interface
- 📂 อัปโหลดและวิเคราะห์โครงงาน
- 📜 ดูประวัติการวิเคราะห์ทั้งหมด
- 📊 ดูสถิติการใช้งาน
- 📈 กราฟและแผนภูมิสรุปข้อมูล
- 📥 ดาวน์โหลดรายงาน (PDF/Word)
- 🔐 การรักษาความปลอดภัยแบบ Role-based

### ⚙️ Admin Panel
- 👥 จัดการผู้ใช้ (เพิ่ม/ลบ/แก้ไข)
- 📊 ดูสถิติระบบทั้งหมด
- 📜 ดูประวัติการใช้งานทั้งระบบ
- 🔧 ตั้งค่าระบบและความปลอดภัย
- 📋 สร้างและส่งออกรายงาน
- 🔒 User management และ security

---

## 🚀 Getting Started

### 1. Installation

```bash
# ไปที่โฟลเดอร์โปรเจค
cd C:\Users\User\Desktop\Project_AI_Grader

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### 2. Configuration

สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
DATABASE_FILE=history.json
```

### 3. Run Applications

#### Option A: Main Launcher (Recommended)
```bash
streamlit run app_launcher.py
```
จากนั้นเลือก Student Interface หรือ Admin Panel

#### Option B: Run Student Interface Directly
```bash
streamlit run student_view.py
```

#### Option C: Run Admin Panel Directly
```bash
streamlit run admin_panel.py
```

---

## 👥 Demo Credentials

### Student
- **Username**: student1, student2, student3
- **Password**: student123
- **Role**: Student

### Teacher
- **Username**: teacher
- **Password**: teacher123
- **Role**: Teacher

### Admin
- **Username**: admin
- **Password**: admin123
- **Role**: Admin (access to Admin Panel)

---

## 📁 Project Structure

```
Project_AI_Grader/
├── student_view.py              # Main Student Interface
├── admin_panel.py               # Admin Management Panel
├── app_launcher.py              # Main Launcher/Menu
├── database.py                  # JSON Database Handler
├── database_sqlite.py           # SQLite Database Handler
├── report_generator.py          # PDF/Word Report Generator
├── email_notifier.py            # Email Notification Module
├── api_server.py                # FastAPI REST Server
├── manifest.json                # PWA Manifest
├── static/
│   ├── service-worker.js        # Service Worker
│   └── pwa.js                   # PWA Helper Functions
├── requirements.txt             # Python Dependencies
├── .env                         # Environment Variables
├── history.json                 # User Data Storage
└── Documentation Files...
```

---

## 🎨 Design System: K-Minimal

### Color Palette
- **Primary**: #E8B4D4 (Pastel Pink)
- **Secondary**: #D4A5C8 (Darker Pastel Pink)
- **Light**: #F0D9E8 (Light Pastel Pink)
- **Accent**: #B8879F (Dark Accent)

### Typography
- **Font**: Prompt (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

### Features
- Smooth gradients
- Rounded corners (10-15px)
- Soft shadows
- Smooth transitions (0.3s)
- Responsive design

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| ADMIN_PANEL_GUIDE.md | Admin Panel User Guide |
| K_MINIMAL_DESIGN_GUIDE.md | Design System Documentation |
| COLOR_PALETTE.md | Color Reference Guide |
| CSS_VARIABLES.css | CSS Variables & Framework |
| VISUAL_GUIDE.md | Visual Examples |
| API_DOCUMENTATION.md | REST API Reference |
| DEPLOYMENT_GUIDE.md | Deployment Instructions |
| IMPLEMENTATION_CHECKLIST.md | Implementation Checklist |
| DELIVERABLES.md | Project Deliverables |
| COMPLETION_REPORT.md | Completion Report |

---

## 🔧 System Architecture

### Frontend
- **Framework**: Streamlit
- **UI Framework**: K-Minimal Design System
- **Charts**: Plotly
- **PDF Export**: ReportLab

### Backend
- **Database**: JSON (default) / SQLite (optional)
- **API**: FastAPI
- **Authentication**: Role-based Login

### AI Engine
- **Model**: Google Generative AI (Gemini)
- **Features**: Automatic text analysis and consistency checking

### Mobile
- **PWA**: Progressive Web App Support
- **Service Worker**: Offline Capabilities

---

## 🔐 Security Features

1. **Authentication**
   - User login with credentials
   - Role-based access control
   - Session management

2. **Password Management**
   - Password reset functionality
   - Secure password storage
   - Admin password management

3. **Data Protection**
   - User data isolation
   - History logging
   - Database backup support

4. **Access Control**
   - Student: Can view own analysis
   - Teacher: Can view student analyses
   - Admin: Full system access

---

## 📊 Key Components

### Student Interface (student_view.py)
- Tab 1: Project Analysis (อัปโหลดและวิเคราะห์)
- Tab 2: History (ดูประวัติ)
- Tab 3: Statistics (ดูสถิติ)
- Tab 4: Charts (กราฟและแผนภูมิ)

### Admin Panel (admin_panel.py)
- Tab 1: User Management (จัดการผู้ใช้)
- Tab 2: System Statistics (สถิติระบบ)
- Tab 3: Usage History (ประวัติการใช้งาน)
- Tab 4: System Settings (ตั้งค่าระบบ)
- Tab 5: Reports (รายงาน)

---

## 🌐 Available Ports

```
Student Interface: http://localhost:8501
Admin Panel:       http://localhost:8502
App Launcher:      http://localhost:8503
API Server:        http://localhost:8000
```

---

## 📋 Supported File Types

### Analysis
- PDF (.pdf)
- Word Document (.docx)

### Export
- PDF Report (.pdf)
- Word Document (.docx)
- Excel Spreadsheet (.xlsx)

---

## 🔄 Database Options

### JSON (Default)
- File-based storage
- Easy backup
- Good for small projects
- Location: `history.json`

### SQLite (Optional)
- Relational database
- Better for large datasets
- Migration support
- Location: `analysis.db`

---

## 🚀 Deployment

### Local Development
```bash
streamlit run student_view.py
streamlit run admin_panel.py
```

### Docker
```bash
docker build -t ai-grader .
docker run -p 8501:8502 ai-grader
```

### Cloud Deployment
- Heroku (see DEPLOYMENT_GUIDE.md)
- Google Cloud Run
- AWS EC2
- Azure App Service

---

## 📞 Troubleshooting

### Problem: "Cannot find module google.generativeai"
```bash
pip install google-generativeai==0.8.5
```

### Problem: API Key not set
1. Create `.env` file in project root
2. Add: `GOOGLE_API_KEY=your_api_key`
3. Restart the application

### Problem: Port already in use
```bash
# Kill existing Streamlit process
taskkill /F /IM streamlit.exe
# Run again
streamlit run student_view.py
```

---

## 🎯 Future Enhancements

- [ ] Dark mode support
- [ ] Multi-language support (beyond Thai)
- [ ] Advanced analytics dashboard
- [ ] Machine learning models for grading
- [ ] Mobile app (native iOS/Android)
- [ ] Real-time collaboration features
- [ ] Blockchain verification
- [ ] Integration with LMS platforms

---

## 📊 System Requirements

### Minimum
- Python 3.9+
- 4GB RAM
- 1GB Storage
- Internet connection (for AI)

### Recommended
- Python 3.10+
- 8GB RAM
- 5GB Storage
- High-speed internet

---

## 🛠️ Technologies Used

```
Frontend:
- Streamlit 1.52.1
- Plotly 5.17.0
- Prompt Font

Backend:
- Google Generative AI 0.8.5
- FastAPI 0.68.0
- SQLAlchemy 2.0.23

Database:
- JSON (default)
- SQLite 3

Utilities:
- ReportLab 4.0.7
- Python-docx 1.2.0
- PyPDF2 3.0.1
```

---

## 📜 License

This project is created for educational and administrative purposes.

---

## 👨‍💼 Support & Contact

For technical support or inquiries:
- Check documentation files
- Review ADMIN_PANEL_GUIDE.md for admin features
- Check API_DOCUMENTATION.md for API integration

---

## 🎉 Version Information

**Current Version**: 1.0
**Release Date**: December 15, 2025
**Status**: ✅ Production Ready

### Version History
- **v1.0** (Dec 15, 2025)
  - Initial release
  - Student Interface
  - Admin Panel
  - K-Minimal Design
  - Complete documentation

---

## 📝 Changelog

### December 15, 2025
✅ Created Admin Panel with full features
✅ Added App Launcher for easy navigation
✅ Created complete documentation
✅ Integrated K-Minimal design system
✅ Added user management features
✅ System ready for production

---

## 🏆 Credits

**Design**: K-Minimal Design System
**Typography**: Prompt Font (Google Fonts)
**AI Engine**: Google Generative AI (Gemini)
**Framework**: Streamlit
**Created**: December 2025

---

**Happy Grading! 🎓✨**
