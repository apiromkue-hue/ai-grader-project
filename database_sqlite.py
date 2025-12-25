#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite database module for storing and retrieving project analysis history
Uses SQLAlchemy ORM for better data management
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database base
Base = declarative_base()


class AnalysisRecord(Base):
    """โมเดล SQLAlchemy สำหรับเก็บข้อมูลการวิเคราะห์"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    file_size_chars = Column(Integer, default=0)
    result = Column(Text, nullable=False)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "file_name": self.file_name,
            "timestamp": self.timestamp.isoformat(),
            "file_size_chars": self.file_size_chars,
            "result": self.result
        }


class AnalysisDatabaseSQLite:
    """SQLite ฐานข้อมูลสำหรับจัดการข้อมูลประวัติการวิเคราะห์"""
    
    def __init__(self, db_file: str = "analysis.db"):
        """
        Initialize SQLite database
        
        Args:
            db_file: Path to SQLite database file
        """
        self.db_file = db_file
        self.engine = create_engine(f"sqlite:///{db_file}")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def save_analysis(self, username: str, file_name: str, analysis_result: str) -> bool:
        """
        บันทึกผลการวิเคราะห์ลงฐานข้อมูล
        
        Args:
            username: ชื่อผู้ใช้
            file_name: ชื่อไฟล์
            analysis_result: ผลการวิเคราะห์
        
        Returns:
            True ถ้าบันทึกสำเร็จ
        """
        try:
            session = self.get_session()
            
            record = AnalysisRecord(
                username=username,
                file_name=file_name,
                file_size_chars=len(analysis_result),
                result=analysis_result
            )
            
            session.add(record)
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
            return False
    
    def get_user_history(self, username: str) -> List[Dict]:
        """
        ดึงประวัติการวิเคราะห์ของผู้ใช้
        
        Args:
            username: ชื่อผู้ใช้
        
        Returns:
            List of analysis records sorted by most recent first
        """
        try:
            session = self.get_session()
            
            records = session.query(AnalysisRecord)\
                .filter(AnalysisRecord.username == username)\
                .order_by(AnalysisRecord.timestamp.desc())\
                .all()
            
            history = [
                {
                    "id": r.id,
                    "timestamp": r.timestamp.isoformat(),
                    "file_name": r.file_name,
                    "file_size_chars": r.file_size_chars,
                    "result": r.result
                }
                for r in records
            ]
            
            session.close()
            return history
            
        except Exception as e:
            print(f"❌ Error retrieving history: {e}")
            return []
    
    def get_analysis_by_id(self, username: str, analysis_id: int) -> Optional[Dict]:
        """ดึงผลการวิเคราะห์ครั้งใดครั้งหนึ่ง"""
        try:
            session = self.get_session()
            
            record = session.query(AnalysisRecord)\
                .filter(AnalysisRecord.id == analysis_id, AnalysisRecord.username == username)\
                .first()
            
            result = record.to_dict() if record else None
            session.close()
            return result
            
        except Exception as e:
            print(f"❌ Error retrieving analysis: {e}")
            return None
    
    def delete_analysis(self, username: str, analysis_id: int) -> bool:
        """ลบการวิเคราะห์หนึ่งรายการ"""
        try:
            session = self.get_session()
            
            session.query(AnalysisRecord)\
                .filter(AnalysisRecord.id == analysis_id, AnalysisRecord.username == username)\
                .delete()
            
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            print(f"❌ Error deleting analysis: {e}")
            return False
    
    def delete_all_user_history(self, username: str) -> bool:
        """ลบประวัติทั้งหมดของผู้ใช้"""
        try:
            session = self.get_session()
            
            session.query(AnalysisRecord)\
                .filter(AnalysisRecord.username == username)\
                .delete()
            
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            print(f"❌ Error deleting user history: {e}")
            return False
    
    def get_statistics(self, username: str) -> Dict:
        """ดึงสถิติของผู้ใช้"""
        try:
            session = self.get_session()
            
            count = session.query(func.count(AnalysisRecord.id))\
                .filter(AnalysisRecord.username == username)\
                .scalar()
            
            if count == 0:
                session.close()
                return {
                    "total_analyses": 0,
                    "last_analysis_date": "ยังไม่มีการวิเคราะห์",
                    "avg_file_size": 0
                }
            
            last_record = session.query(AnalysisRecord)\
                .filter(AnalysisRecord.username == username)\
                .order_by(AnalysisRecord.timestamp.desc())\
                .first()
            
            avg_size = session.query(func.avg(AnalysisRecord.file_size_chars))\
                .filter(AnalysisRecord.username == username)\
                .scalar()
            
            session.close()
            
            return {
                "total_analyses": count,
                "last_analysis_date": last_record.timestamp.isoformat() if last_record else None,
                "avg_file_size": int(avg_size) if avg_size else 0
            }
            
        except Exception as e:
            print(f"❌ Error retrieving statistics: {e}")
            return {}
    
    def get_all_statistics(self) -> Dict:
        """ดึงสถิติระบบทั้งหมด"""
        try:
            session = self.get_session()
            
            total_users = session.query(func.count(func.distinct(AnalysisRecord.username))).scalar()
            total_analyses = session.query(func.count(AnalysisRecord.id)).scalar()
            
            user_counts = {}
            users = session.query(func.distinct(AnalysisRecord.username)).all()
            
            for (user,) in users:
                count = session.query(func.count(AnalysisRecord.id))\
                    .filter(AnalysisRecord.username == user)\
                    .scalar()
                if count > 0:
                    user_counts[user] = count
            
            session.close()
            
            return {
                "total_users": total_users or 0,
                "total_analyses": total_analyses or 0,
                "users": user_counts
            }
            
        except Exception as e:
            print(f"❌ Error retrieving all statistics: {e}")
            return {}
    
    @staticmethod
    def migrate_from_json(json_file: str, sqlite_db: "AnalysisDatabaseSQLite") -> bool:
        """
        Migrate data from JSON file to SQLite
        
        Args:
            json_file: Path to JSON database file
            sqlite_db: SQLite database instance
        
        Returns:
            True if migration successful
        """
        try:
            if not os.path.exists(json_file):
                print(f"ℹ️ JSON file not found: {json_file}")
                return True
            
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            migrated_count = 0
            for username, analyses in json_data.items():
                for entry in analyses:
                    sqlite_db.save_analysis(
                        username=username,
                        file_name=entry['file_name'],
                        analysis_result=entry['result']
                    )
                    migrated_count += 1
            
            print(f"✅ Migrated {migrated_count} records from JSON to SQLite")
            return True
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            return False


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print("SQLite Database Module")
    print("-" * 50)
    
    # Create database
    db = AnalysisDatabaseSQLite("test_analysis.db")
    
    # Test: Save analysis
    success = db.save_analysis(
        username="test_user",
        file_name="test_project.pdf",
        analysis_result="This is a test analysis result"
    )
    print(f"Save test: {'✅ Passed' if success else '❌ Failed'}")
    
    # Test: Get history
    history = db.get_user_history("test_user")
    print(f"History retrieved: {len(history)} records")
    
    # Test: Get statistics
    stats = db.get_statistics("test_user")
    print(f"Statistics: {stats}")
    
    # Migrate from JSON
    if os.path.exists("history.json"):
        print("\nMigrating from JSON to SQLite...")
        db.migrate_from_json("history.json", db)
    
    print("\n✅ Database test completed")
