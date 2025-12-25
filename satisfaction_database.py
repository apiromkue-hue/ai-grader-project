#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Satisfaction Survey Database Module
เก็บข้อมูลแบบสอบถามความพึงพอใจสำหรับการวิจัย
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class SatisfactionDatabase:
    """จัดการฐานข้อมูลแบบสอบถามความพึงพอใจ"""
    
    def __init__(self, db_file: str = "satisfaction_data.json"):
        self.db_file = db_file
        self._initialize_database()
    
    def _initialize_database(self):
        """สร้างไฟล์ฐานข้อมูลถ้ายังไม่มี"""
        if not os.path.exists(self.db_file):
            initial_data = {
                "surveys": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_responses": 0,
                    "teacher_responses": 0,
                    "student_responses": 0
                }
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict:
        """โหลดข้อมูลจากไฟล์"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database: {e}")
            return {
                "surveys": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_responses": 0,
                    "teacher_responses": 0,
                    "student_responses": 0
                }
            }
    
    def _save_data(self, data: Dict):
        """บันทึกข้อมูลลงไฟล์"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def add_survey_response(self, 
                           user_type: str,
                           username: str,
                           name: str,
                           responses: Dict) -> bool:
        """
        เพิ่มคำตอบแบบสอบถาม
        
        Args:
            user_type: ประเภทผู้ใช้ ('teacher' หรือ 'student')
            username: ชื่อผู้ใช้
            name: ชื่อจริง
            responses: คำตอบทั้งหมด (dict)
        
        Returns:
            True ถ้าบันทึกสำเร็จ
        """
        try:
            data = self._load_data()
            
            # สร้างรายการใหม่
            survey_entry = {
                "id": f"SURVEY_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(data['surveys']) + 1}",
                "timestamp": datetime.now().isoformat(),
                "user_type": user_type,
                "username": username,
                "name": name,
                "responses": responses,
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # เพิ่มลงในรายการ
            data["surveys"].append(survey_entry)
            
            # อัพเดท metadata
            data["metadata"]["total_responses"] = len(data["surveys"])
            data["metadata"][f"{user_type}_responses"] = len([
                s for s in data["surveys"] if s["user_type"] == user_type
            ])
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # บันทึก
            self._save_data(data)
            return True
            
        except Exception as e:
            print(f"Error adding survey response: {e}")
            return False
    
    def get_all_surveys(self) -> List[Dict]:
        """ดึงข้อมูลแบบสอบถามทั้งหมด"""
        data = self._load_data()
        return data.get("surveys", [])
    
    def get_surveys_by_type(self, user_type: str) -> List[Dict]:
        """ดึงข้อมูลแบบสอบถามตามประเภทผู้ใช้"""
        surveys = self.get_all_surveys()
        return [s for s in surveys if s["user_type"] == user_type]
    
    def get_metadata(self) -> Dict:
        """ดึงข้อมูล metadata"""
        data = self._load_data()
        return data.get("metadata", {})
    
    def calculate_statistics(self, user_type: Optional[str] = None) -> Dict:
        """
        คำนวณสถิติความพึงพอใจ
        
        Args:
            user_type: ถ้าระบุจะคำนวณเฉพาะประเภทนั้น, ถ้าไม่ระบุจะคำนวณทั้งหมด
        
        Returns:
            Dict ของสถิติ
        """
        surveys = self.get_surveys_by_type(user_type) if user_type else self.get_all_surveys()
        
        if not surveys:
            return {}
        
        # เก็บคะแนนแต่ละด้าน
        stats = {
            "total_responses": len(surveys),
            "categories": {}
        }
        
        # รวบรวมคะแนนแต่ละคำถาม
        question_scores = {}
        
        for survey in surveys:
            responses = survey.get("responses", {})
            for question_key, value in responses.items():
                if isinstance(value, (int, float)) and value > 0:
                    if question_key not in question_scores:
                        question_scores[question_key] = []
                    question_scores[question_key].append(value)
        
        # คำนวณค่าเฉลี่ย
        for question_key, scores in question_scores.items():
            if scores:
                stats["categories"][question_key] = {
                    "mean": sum(scores) / len(scores),
                    "min": min(scores),
                    "max": max(scores),
                    "count": len(scores),
                    "scores": scores
                }
        
        # คำนวณค่าเฉลี่ยรวม
        all_scores = [score for scores in question_scores.values() for score in scores]
        if all_scores:
            stats["overall_mean"] = sum(all_scores) / len(all_scores)
        else:
            stats["overall_mean"] = 0
        
        return stats
    
    def get_satisfaction_level(self, score: float) -> str:
        """แปลงคะแนนเป็นระดับความพึงพอใจ"""
        if score >= 4.5:
            return "มากที่สุด"
        elif score >= 3.5:
            return "มาก"
        elif score >= 2.5:
            return "ปานกลาง"
        elif score >= 1.5:
            return "น้อย"
        else:
            return "น้อยที่สุด"
    
    def export_for_research(self) -> Dict:
        """ส่งออกข้อมูลสำหรับการวิจัย"""
        data = self._load_data()
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "metadata": data.get("metadata", {}),
            "summary": {
                "teacher_stats": self.calculate_statistics("teacher"),
                "student_stats": self.calculate_statistics("student"),
                "overall_stats": self.calculate_statistics()
            },
            "raw_data": data.get("surveys", [])
        }
        
        return export_data
    
    def check_if_user_responded(self, username: str) -> bool:
        """ตรวจสอบว่าผู้ใช้เคยตอบแบบสอบถามแล้วหรือยัง"""
        surveys = self.get_all_surveys()
        return any(s["username"] == username for s in surveys)
