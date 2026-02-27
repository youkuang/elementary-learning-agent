"""
Elementary Learning Agent - Main Entry Point
Using OpenClaw Framework
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from loguru import logger

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
    logger.info("Powered by OpenClaw")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        config = Config()
        logger.info(f"Configuration loaded: {config.ai_model}")
        
        # Initialize database
        db_manager = DatabaseManager(config)
        db_manager.initialize()
        logger.info("Database initialized")
        
        # Start OpenClaw
        logger.info("Starting OpenClaw...")
        logger.info("=" * 60)
        logger.info("System is ready! Listening for Slack messages...")
        logger.info("=" * 60)
        
        # TODO: Start OpenClaw with openclaw_config.yaml
        # This will be implemented once OpenClaw is installed
        # For now, show instructions
        
        logger.warning("OpenClaw not yet started.")
        logger.info("To start the system:")
        logger.info("1. Install OpenClaw: pip install openclaw")
        logger.info("2. Run: openclaw start --config openclaw_config.yaml")
        
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
