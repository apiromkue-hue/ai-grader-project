# 🚀 System Launch Guide

## Quick Start - Run Any Application

### Option 1: App Launcher (Recommended)
```bash
cd C:\Users\User\Desktop\Project_AI_Grader
streamlit run app_launcher.py
```
**Then**: Choose Student Interface or Admin Panel from the menu

---

### Option 2: Run Student Interface
```bash
streamlit run student_view.py
```
**Access**: `http://localhost:8501` (or auto-displayed URL)

---

### Option 3: Run Admin Panel
```bash
streamlit run admin_panel.py
```
**Access**: `http://localhost:8501` (or auto-displayed URL)

---

## 📱 Demo Credentials

### Student Access
```
Username: student1
Password: student123
Role: Student
```

### Teacher Access
```
Username: teacher
Password: teacher123
Role: Teacher
```

### Admin Access
```
Username: admin
Password: admin123
Role: Admin (Admin Panel)
```

---

## 🎯 What Each App Does

### App Launcher (app_launcher.py)
- Shows system overview
- Choose between Student Interface and Admin Panel
- Displays quick start guide
- Shows system status

### Student Interface (student_view.py)
- Upload and analyze projects
- View analysis history
- See statistics and reports
- View charts
- Download PDF/Word reports
- Admin users see Admin Panel link

### Admin Panel (admin_panel.py)
- Manage all users (Add/Edit/Delete)
- View system-wide statistics
- Track all user activities
- Configure system settings
- Generate and export reports

---

## 📊 Default Ports

```
Streamlit App (Student/Admin): 8501, 8502, 8503 (auto-increment)
API Server: 8000
```

**Note**: Port auto-increments if previous is occupied

---

## ✨ Features at a Glance

### Student Interface
- 📂 Project Analysis
- 📜 History Tracking
- 📊 Statistics
- 📈 Charts & Graphs
- 📥 Report Export
- 🔐 Role-based Access

### Admin Panel
- 👥 User Management
- 📊 System Statistics
- 📜 Usage History
- 🔧 System Configuration
- 📋 Report Generation
- 🔒 Security Controls

---

## 🎨 Design System

Both interfaces use:
- **K-Minimal Design** - Pastel Pink Color Scheme
- **Prompt Font** - From Google Fonts
- **Responsive Layout** - Works on all devices
- **Modern UI** - Smooth animations & transitions

---

## 📁 Project Structure

```
Project_AI_Grader/
├── app_launcher.py        ← Main Launcher (Start Here!)
├── student_view.py        ← Student Interface
├── admin_panel.py         ← Admin Panel
├── database.py            ← JSON Database
├── report_generator.py    ← Report Export
├── email_notifier.py      ← Email Notifications
├── api_server.py          ← REST API Server
└── documentation/         ← Help Files
```

---

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill existing Streamlit process
taskkill /F /IM streamlit.exe

# Try again
streamlit run app_launcher.py
```

### Cannot Import Module
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Error
```
1. Create .env file in project root
2. Add: GOOGLE_API_KEY=your_api_key
3. Restart application
```

---

## 📚 Documentation Files

| File | For | Purpose |
|------|-----|---------|
| README.md | Everyone | System overview |
| ADMIN_PANEL_GUIDE.md | Admin | Detailed admin guide |
| ADMIN_QUICK_START.md | Admin | Quick reference |
| K_MINIMAL_DESIGN_GUIDE.md | Designers | Design system |
| API_DOCUMENTATION.md | Developers | API reference |

---

## 🎓 First Time Users

### For Students
1. Run: `streamlit run student_view.py`
2. Login with: student1 / student123
3. Click "📂 วิเคราะห์โครงงาน"
4. Upload a PDF or Word document
5. Click "🚀 เริ่มวิเคราะห์"
6. View results and download report

### For Admins
1. Run: `streamlit run admin_panel.py`
2. Login with: admin / admin123
3. Navigate through 5 tabs
4. Manage users, view stats, create reports

---

## ⚡ Quick Tips

### Increase Performance
- Close other applications
- Use latest Python 3.10+
- Install dependencies fresh: `pip install -r requirements.txt --upgrade`

### Better Results
- Upload clear PDF or Word files
- Check internet connection (for AI)
- Use Chrome/Edge for best compatibility

### Admin Tips
- Regular backups via Tab 4
- Reset cache weekly for speed
- Monitor system status daily

---

## 🔄 System Workflow

```
App Launcher
    ├── Student Interface
    │   ├── Analysis
    │   ├── History
    │   ├── Statistics
    │   ├── Charts
    │   └── Reports
    │
    └── Admin Panel
        ├── User Management
        ├── Statistics
        ├── History
        ├── Settings
        └── Reports
```

---

## 📞 Common Tasks

| Task | Steps |
|------|-------|
| **Add User** | Admin Panel → Tab 1 → Fill form → Click "➕ เพิ่ม" |
| **View Stats** | Admin Panel → Tab 2 → See metrics & charts |
| **Check History** | Admin Panel → Tab 3 → Filter & view table |
| **Reset Password** | Admin Panel → Tab 4 → Select user → Click "🔄" |
| **Export Report** | Admin Panel → Tab 5 → Select type → Click export button |
| **Analyze Project** | Student Interface → Tab 1 → Upload file → Click "🚀" |
| **See Your Stats** | Student Interface → Tab 3 → View personal metrics |

---

## 🎉 You're Ready!

Everything is set up and ready to go. Choose your starting point:

```
👨‍🎓 Students → Run student_view.py
⚙️ Admins → Run admin_panel.py
🎯 New Users → Run app_launcher.py (Recommended)
```

---

## 🆘 Need Help?

1. Check the relevant documentation file
2. Review README.md for system overview
3. See ADMIN_PANEL_GUIDE.md for admin tasks
4. Check troubleshooting section in this file

---

**Happy Learning! 🎓✨**
**Happy Managing! ⚙️✨**

Last Updated: December 15, 2025
Version: 1.0
Status: Ready to Use
