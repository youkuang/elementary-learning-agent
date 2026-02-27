"""
Data Models
"""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    """Learning task model"""
    task_id: str
    subject: str  # 语文/数学/英语
    title: str
    content: str
    created_date: datetime = Field(default_factory=datetime.now)
    target_date: Optional[date] = None
    status: str = "进行中"  # 进行中/已完成
    notes: Optional[str] = None


class KnowledgePoint(BaseModel):
    """Knowledge point model"""
    kp_id: str
    task_id: str
    content: str
    type: str  # 生词/古诗/公式/单词等
    error_count: int = 0
    correct_count: int = 0
    mastery_level: str = "未测试"  # 未测试/学习中/需加强/已掌握
    next_review_date: Optional[date] = None
    last_test_date: Optional[datetime] = None
    notes: Optional[str] = None


class LearningHistory(BaseModel):
    """Learning history record"""
    record_id: str
    kp_id: str
    test_date: datetime = Field(default_factory=datetime.now)
    result: str  # 正确/错误
    parent_feedback: Optional[str] = None
    agent_response: Optional[str] = None


class TeachingStrategy(BaseModel):
    """Teaching strategy record"""
    strategy_id: str
    kp_id: str
    strategy_type: str  # 记忆口诀/联想记忆/对比学习等
    content: str
    used_date: datetime = Field(default_factory=datetime.now)
    effectiveness: str = "未知"  # 有效/无效/未知
