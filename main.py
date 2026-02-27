"""
Elementary Learning Agent - Main Entry Point
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from loguru import logger

from agents.coordinator import CoordinatorAgent
from agents.chinese_tutor import ChineseTutorAgent
from agents.math_tutor import MathTutorAgent
from agents.english_tutor import EnglishTutorAgent
from database.db_manager import DatabaseManager
from config.config import Config


def setup_logging():
    """Configure logging"""
    config = Config()
    
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stderr,
        level=config.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    
    # Add file logger
    log_file = Path(config.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        config.log_file,
        level=config.log_level,
        rotation="10 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
    )


def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("Starting Elementary Learning Agent System")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        config = Config()
        logger.info(f"Configuration loaded: {config.ai_model}")
        
        # Initialize database
        db_manager = DatabaseManager(config)
        db_manager.initialize()
        logger.info("Database initialized")
        
        # Initialize agents
        logger.info("Initializing agents...")
        
        chinese_agent = ChineseTutorAgent(config, db_manager)
        math_agent = MathTutorAgent(config, db_manager)
        english_agent = EnglishTutorAgent(config, db_manager)
        coordinator = CoordinatorAgent(config, db_manager)
        
        logger.info("✓ Chinese Tutor Agent initialized")
        logger.info("✓ Math Tutor Agent initialized")
        logger.info("✓ English Tutor Agent initialized")
        logger.info("✓ Coordinator Agent initialized")
        
        # Start the system
        logger.info("=" * 60)
        logger.info("System is ready! Listening for Slack messages...")
        logger.info("=" * 60)
        
        # Start Slack bot (blocking call)
        coordinator.start()
        
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
