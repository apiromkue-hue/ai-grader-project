#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email notification module for sending analysis completion notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


class EmailNotifier:
    """ส่งการแจ้งเตือนทางอีเมล"""
    
    def __init__(self, 
                 smtp_server: str = None,
                 smtp_port: int = None,
                 sender_email: str = None,
                 sender_password: str = None):
        """
        Initialize email notifier
        
        Args:
            smtp_server: SMTP server address (default: smtp.gmail.com)
            smtp_port: SMTP port (default: 587)
            sender_email: Sender email address
            sender_password: Sender email password (use App Password for Gmail)
        """
        self.smtp_server = smtp_server or os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("EMAIL_SMTP_PORT", 587))
        self.sender_email = sender_email or os.getenv("EMAIL_SENDER")
        self.sender_password = sender_password or os.getenv("EMAIL_PASSWORD")
        self.is_configured = bool(self.sender_email and self.sender_password)
    
    def send_analysis_notification(self,
                                   recipient_email: str,
                                   username: str,
                                   file_name: str,
                                   analysis_result: str) -> bool:
        """
        ส่งการแจ้งเตือนเมื่อเสร็จการวิเคราะห์
        
        Args:
            recipient_email: อีเมลของผู้รับ
            username: ชื่อผู้ใช้
            file_name: ชื่อไฟล์ที่วิเคราะห์
            analysis_result: ผลการวิเคราะห์
        
        Returns:
            True ถ้าส่งสำเร็จ, False ถ้าล้มเหลว
        """
        if not self.is_configured:
            print("⚠️ Email notifier is not configured")
            return False
        
        try:
            # สร้างข้อความ
            message = MIMEMultipart("alternative")
            message["Subject"] = f"✅ การวิเคราะห์โครงงานสำเร็จ - {file_name}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Plain text version
            text = f"""
สวัสดี {username},

การวิเคราะห์โครงงานของคุณเสร็จสิ้นแล้ว

📄 ชื่อไฟล์: {file_name}
⏰ เวลา: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
👤 ผู้ใช้: {username}

📊 ผลการวิเคราะห์:
{analysis_result[:500]}...

โปรดเข้าสู่ระบบเพื่อดูรายละเอียดทั้งหมด

--
ระบบตรวจโครงงาน AI
            """
            
            # HTML version
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                            <h1 style="margin: 0;">✅ การวิเคราะห์สำเร็จ</h1>
                        </div>
                        
                        <div style="background: white; padding: 20px; border-radius: 0 0 10px 10px;">
                            <p>สวัสดี <strong>{username}</strong>,</p>
                            
                            <p>การวิเคราะห์โครงงานของคุณเสร็จสิ้นแล้ว</p>
                            
                            <div style="background-color: #f0f4ff; padding: 15px; border-left: 4px solid #667eea; border-radius: 5px; margin: 20px 0;">
                                <p><strong>📄 ชื่อไฟล์:</strong> {file_name}</p>
                                <p><strong>⏰ เวลา:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                                <p><strong>👤 ผู้ใช้:</strong> {username}</p>
                            </div>
                            
                            <h3 style="color: #667eea;">📊 ผลการวิเคราะห์ (สรุป):</h3>
                            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #ddd;">
                                <p style="white-space: pre-wrap; font-size: 14px;">{analysis_result[:500]}...</p>
                            </div>
                            
                            <p style="margin-top: 20px;">
                                <a href="http://localhost:8502" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                                    ดูรายละเอียดทั้งหมด
                                </a>
                            </p>
                            
                            <hr style="margin: 20px 0; border: 1px solid #ddd;">
                            
                            <p style="color: #999; font-size: 12px; text-align: center;">
                                ระบบตรวจโครงงาน AI<br>
                                {datetime.now().strftime("%Y-%m-%d")}
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Attach both versions
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            
            # ส่งอีเมล
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"✅ Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def send_teacher_notification(self,
                                  recipient_email: str,
                                  student_name: str,
                                  file_name: str) -> bool:
        """
        ส่งการแจ้งเตือนให้อาจารย์เมื่อนักเรียนส่งการวิเคราะห์
        
        Args:
            recipient_email: อีเมลของอาจารย์
            student_name: ชื่อนักเรียน
            file_name: ชื่อไฟล์
        
        Returns:
            True ถ้าส่งสำเร็จ
        """
        if not self.is_configured:
            return False
        
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = f"📋 นักเรียน {student_name} ได้ส่งการวิเคราะห์ใหม่"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            text = f"""
สวัสดีอาจารย์,

นักเรียน {student_name} ได้ส่งการวิเคราะห์โครงงานใหม่

📄 ไฟล์: {file_name}
⏰ เวลา: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

โปรดเข้าสู่ระบบเพื่อตรวจสอบ

--
ระบบตรวจโครงงาน AI
            """
            
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #667eea;">📋 มีการส่งงานใหม่</h2>
                        <p>นักเรียน <strong>{student_name}</strong> ได้ส่งการวิเคราะห์โครงงานใหม่</p>
                        <p>📄 ไฟล์: {file_name}</p>
                        <p>⏰ เวลา: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                </body>
            </html>
            """
            
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send teacher notification: {e}")
            return False


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print("Email Notifier Module")
    print("-" * 50)
    
    # สร้าง instance
    notifier = EmailNotifier()
    
    if notifier.is_configured:
        print("✅ Email notifier is configured and ready to use")
        
        # ตัวอย่างการส่งอีเมล (ต้อง set environment variables ก่อน)
        # result = notifier.send_analysis_notification(
        #     recipient_email="student@example.com",
        #     username="student1",
        #     file_name="โครงงาน_test.pdf",
        #     analysis_result="ผลการวิเคราะห์..."
        # )
    else:
        print("⚠️ Email notifier is NOT configured")
        print("To enable email notifications, set these environment variables:")
        print("  - EMAIL_SENDER")
        print("  - EMAIL_PASSWORD")
        print("  - EMAIL_SMTP_SERVER (optional, default: smtp.gmail.com)")
        print("  - EMAIL_SMTP_PORT (optional, default: 587)")
