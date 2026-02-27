"""
Configuration Management
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    """Application configuration"""
    
    # Slack
    slack_bot_token: str = Field(default="", env="SLACK_BOT_TOKEN")
    slack_app_token: str = Field(default="", env="SLACK_APP_TOKEN")
    
    # AI Model
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ai_model: str = Field(default="claude-3-5-sonnet-20241022", env="AI_MODEL")
    
    # Database
    database_type: str = Field(default="sqlite", env="DATABASE_TYPE")
    database_path: str = Field(default="./data/learning.db", env="DATABASE_PATH")
    database_host: Optional[str] = Field(default=None, env="DATABASE_HOST")
    database_port: Optional[int] = Field(default=None, env="DATABASE_PORT")
    database_name: Optional[str] = Field(default=None, env="DATABASE_NAME")
    database_user: Optional[str] = Field(default=None, env="DATABASE_USER")
    database_password: Optional[str] = Field(default=None, env="DATABASE_PASSWORD")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", env="LOG_FILE")
    
    # Scheduler
    enable_scheduler: bool = Field(default=True, env="ENABLE_SCHEDULER")
    daily_plan_time: str = Field(default="08:00", env="DAILY_PLAN_TIME")
    weekly_report_day: int = Field(default=0, env="WEEKLY_REPORT_DAY")
    weekly_report_time: str = Field(default="20:00", env="WEEKLY_REPORT_TIME")
    
    # System
    timezone: str = Field(default="Asia/Shanghai", env="TIMEZONE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def get_database_url(self) -> str:
        """Get database connection URL"""
        if self.database_type == "sqlite":
            return f"sqlite:///{self.database_path}"
        elif self.database_type == "postgresql":
            return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")
    
    def get_ai_api_key(self) -> str:
        """Get AI API key based on model"""
        if "claude" in self.ai_model.lower():
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required for Claude models")
            return self.anthropic_api_key
        elif "gpt" in self.ai_model.lower():
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for GPT models")
            return self.openai_api_key
        else:
            raise ValueError(f"Unsupported AI model: {self.ai_model}")
