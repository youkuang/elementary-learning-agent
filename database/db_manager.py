"""
Database Manager
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from loguru import logger

from database.models import Task, KnowledgePoint, LearningHistory, TeachingStrategy
from config.config import Config


class DatabaseManager:
    """Database management class"""
    
    def __init__(self, config: Config):
        self.config = config
        self.db_path = Path(config.database_path)
        self.connection = None
    
    def initialize(self):
        """Initialize database"""
        # Create data directory if not exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create database and tables
        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        
        # Read and execute schema
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        self.connection.executescript(schema_sql)
        self.connection.commit()
        
        logger.info(f"Database initialized at {self.db_path}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    # Task operations
    def create_task(self, task: Task) -> bool:
        """Create a new task"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO tasks (task_id, subject, title, content, created_date, target_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id, task.subject, task.title, task.content,
                task.created_date, task.target_date, task.status, task.notes
            ))
            self.connection.commit()
            logger.info(f"Task created: {task.task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = cursor.fetchone()
        if row:
            return Task(**dict(row))
        return None
    
    def get_tasks_by_subject(self, subject: str, status: Optional[str] = None) -> List[Task]:
        """Get tasks by subject"""
        cursor = self.connection.cursor()
        if status:
            cursor.execute("SELECT * FROM tasks WHERE subject = ? AND status = ?", (subject, status))
        else:
            cursor.execute("SELECT * FROM tasks WHERE subject = ?", (subject,))
        return [Task(**dict(row)) for row in cursor.fetchall()]
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (status, task_id))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to update task status: {e}")
            return False
    
    # Knowledge point operations
    def create_knowledge_point(self, kp: KnowledgePoint) -> bool:
        """Create a new knowledge point"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO knowledge_points 
                (kp_id, task_id, content, type, error_count, correct_count, mastery_level, next_review_date, last_test_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                kp.kp_id, kp.task_id, kp.content, kp.type,
                kp.error_count, kp.correct_count, kp.mastery_level,
                kp.next_review_date, kp.last_test_date, kp.notes
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to create knowledge point: {e}")
            return False
    
    def get_knowledge_point(self, kp_id: str) -> Optional[KnowledgePoint]:
        """Get knowledge point by ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM knowledge_points WHERE kp_id = ?", (kp_id,))
        row = cursor.fetchone()
        if row:
            return KnowledgePoint(**dict(row))
        return None
    
    def get_knowledge_points_by_task(self, task_id: str) -> List[KnowledgePoint]:
        """Get all knowledge points for a task"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM knowledge_points WHERE task_id = ?", (task_id,))
        return [KnowledgePoint(**dict(row)) for row in cursor.fetchall()]
    
    def update_knowledge_point(self, kp: KnowledgePoint) -> bool:
        """Update knowledge point"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE knowledge_points 
                SET error_count = ?, correct_count = ?, mastery_level = ?, 
                    next_review_date = ?, last_test_date = ?, notes = ?
                WHERE kp_id = ?
            """, (
                kp.error_count, kp.correct_count, kp.mastery_level,
                kp.next_review_date, kp.last_test_date, kp.notes, kp.kp_id
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to update knowledge point: {e}")
            return False
    
    def get_knowledge_points_for_review(self, review_date: date) -> List[KnowledgePoint]:
        """Get knowledge points that need review"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM knowledge_points 
            WHERE next_review_date <= ? AND mastery_level != '已掌握'
            ORDER BY next_review_date
        """, (review_date,))
        return [KnowledgePoint(**dict(row)) for row in cursor.fetchall()]
    
    # Learning history operations
    def create_learning_history(self, history: LearningHistory) -> bool:
        """Create learning history record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO learning_history (record_id, kp_id, test_date, result, parent_feedback, agent_response)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                history.record_id, history.kp_id, history.test_date,
                history.result, history.parent_feedback, history.agent_response
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to create learning history: {e}")
            return False
    
    def get_learning_history(self, kp_id: str) -> List[LearningHistory]:
        """Get learning history for a knowledge point"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM learning_history 
            WHERE kp_id = ? 
            ORDER BY test_date DESC
        """, (kp_id,))
        return [LearningHistory(**dict(row)) for row in cursor.fetchall()]
    
    # Teaching strategy operations
    def create_teaching_strategy(self, strategy: TeachingStrategy) -> bool:
        """Create teaching strategy record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO teaching_strategies (strategy_id, kp_id, strategy_type, content, used_date, effectiveness)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                strategy.strategy_id, strategy.kp_id, strategy.strategy_type,
                strategy.content, strategy.used_date, strategy.effectiveness
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to create teaching strategy: {e}")
            return False
    
    def get_teaching_strategies(self, kp_id: str) -> List[TeachingStrategy]:
        """Get teaching strategies for a knowledge point"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM teaching_strategies 
            WHERE kp_id = ? 
            ORDER BY used_date DESC
        """, (kp_id,))
        return [TeachingStrategy(**dict(row)) for row in cursor.fetchall()]
