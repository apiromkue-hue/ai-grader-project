#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database module for storing and retrieving project analysis history
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class AnalysisDatabase:
    """คลาสสำหรับจัดการข้อมูลประวัติการวิเคราะห์โครงงาน"""
    
    def __init__(self, db_file: str = "history.json"):
        """
        Initialize the database
        
        Args:
            db_file: Path to the JSON database file (default: history.json)
        """
        self.db_file = db_file
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """สร้างไฟล์ database ถ้ายังไม่มี"""
        if not os.path.exists(self.db_file):
            self._write_db({})
    
    def _read_db(self) -> Dict:
        """อ่านข้อมูลจาก database"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_db(self, data: Dict):
        """บันทึกข้อมูลลง database"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_analysis(self, username: str, file_name: str, analysis_result: str) -> bool:
        """
        บันทึกผลการวิเคราะห์หนึ่งครั้งลงในประวัติ
        
        Args:
            username: ชื่อผู้ใช้ที่ทำการวิเคราะห์
            file_name: ชื่อไฟล์ที่วิเคราะห์
            analysis_result: ผลการวิเคราะห์จาก AI
        
        Returns:
            True ถ้าบันทึกสำเร็จ, False ถ้าล้มเหลว
        """
        try:
            db_data = self._read_db()
            
            # สร้างรายการใหม่สำหรับผู้ใช้นี้ถ้ายังไม่มี
            if username not in db_data:
                db_data[username] = []
            
            # สร้างรูปแบบข้อมูลการวิเคราะห์
            analysis_entry = {
                "id": len(db_data[username]) + 1,
                "timestamp": datetime.now().isoformat(),
                "file_name": file_name,
                "file_size_chars": len(analysis_result),
                "result": analysis_result
            }
            
            # เพิ่มเข้าประวัติ
            db_data[username].append(analysis_entry)
            
            # บันทึกลง database
            self._write_db(db_data)
            return True
            
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return False
    
    def get_user_history(self, username: str) -> List[Dict]:
        """
        ดึงประวัติการวิเคราะห์ของผู้ใช้คนหนึ่ง
        
        Args:
            username: ชื่อผู้ใช้ที่ต้องการดูประวัติ
        
        Returns:
            List of analysis entries, sorted by most recent first
        """
        db_data = self._read_db()
        
        if username not in db_data:
            return []
        
        # เรียงลำดับจากใหม่ไปเก่า
        history = db_data[username]
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    def get_analysis_by_id(self, username: str, analysis_id: int) -> Optional[Dict]:
        """
        ดึงผลการวิเคราะห์ครั้งใดครั้งหนึ่งตามเลข ID
        
        Args:
            username: ชื่อผู้ใช้
            analysis_id: เลข ID ของการวิเคราะห์
        
        Returns:
            Analysis entry dict หรือ None ถ้าไม่เจอ
        """
        history = self.get_user_history(username)
        
        for entry in history:
            if entry['id'] == analysis_id:
                return entry
        
        return None
    
    def delete_analysis(self, username: str, analysis_id: int) -> bool:
        """
        ลบการวิเคราะห์หนึ่งรายการจากประวัติ
        
        Args:
            username: ชื่อผู้ใช้
            analysis_id: เลข ID ของการวิเคราะห์ที่ต้องการลบ
        
        Returns:
            True ถ้าลบสำเร็จ, False ถ้าล้มเหลว
        """
        try:
            db_data = self._read_db()
            
            if username not in db_data:
                return False
            
            # ค้นหาและลบ
            db_data[username] = [
                entry for entry in db_data[username]
                if entry['id'] != analysis_id
            ]
            
            self._write_db(db_data)
            return True
            
        except Exception as e:
            print(f"Error deleting analysis: {e}")
            return False
    
    def delete_all_user_history(self, username: str) -> bool:
        """
        ลบประวัติทั้งหมดของผู้ใช้คนหนึ่ง
        
        Args:
            username: ชื่อผู้ใช้ที่ต้องการลบประวัติ
        
        Returns:
            True ถ้าลบสำเร็จ
        """
        try:
            db_data = self._read_db()
            
            if username in db_data:
                db_data[username] = []
            
            self._write_db(db_data)
            return True
            
        except Exception as e:
            print(f"Error deleting user history: {e}")
            return False
    
    def get_statistics(self, username: str) -> Dict:
        """
        ดึงสถิติการใช้งานของผู้ใช้
        
        Args:
            username: ชื่อผู้ใช้
        
        Returns:
            Dictionary with statistics: total_analyses, last_analysis_date, avg_file_size, etc.
        """
        history = self.get_user_history(username)
        
        if not history:
            return {
                "total_analyses": 0,
                "last_analysis_date": "ยังไม่มีการวิเคราะห์",
                "avg_file_size": 0
            }
        
        # คำนวณสถิติ
        total = len(history)
        last_date = history[0]['timestamp'] if history else None
        avg_size = sum([entry.get('file_size_chars', 0) for entry in history]) / total if total > 0 else 0
        
        return {
            "total_analyses": total,
            "last_analysis_date": last_date,
            "avg_file_size": int(avg_size)
        }
    
    def get_all_statistics(self) -> Dict:
        """
        ดึงสถิติการใช้งานระบบทั้งหมด (สำหรับ Admin)
        
        Returns:
            Dictionary with system-wide statistics
        """
        db_data = self._read_db()
        
        total_users = len([u for u in db_data if len(db_data[u]) > 0])
        total_analyses = sum([len(db_data[u]) for u in db_data])
        
        return {
            "total_users": total_users,
            "total_analyses": total_analyses,
            "users": {u: len(db_data[u]) for u in db_data if len(db_data[u]) > 0}
        }


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # สร้าง instance ของ database
    db = AnalysisDatabase()
    
    # ตัวอย่าง: บันทึกการวิเคราะห์
    print("ตัวอย่างการใช้งาน Database:")
    print("-" * 50)
    
    # บันทึก
    result = db.save_analysis(
        username="teacher",
        file_name="โครงงาน_ของเด็กน้อย.pdf",
        analysis_result="## ผลการวิเคราะห์\n- วัตถุประสงค์: ชัดเจน\n- สรุปผล: สอดคล้อง"
    )
    print(f"บันทึกสำเร็จ: {result}")
    
    # ดึงประวัติ
    history = db.get_user_history("teacher")
    print(f"\nประวัติของ teacher: {len(history)} รายการ")
    
    # ดึงสถิติ
    stats = db.get_statistics("teacher")
    print(f"\nสถิติ teacher:")
    print(f"  - ทั้งหมด: {stats['total_analyses']} ครั้ง")
    print(f"  - ครั้งล่าสุด: {stats['last_analysis_date']}")
