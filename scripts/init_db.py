"""
Database Initialization Script
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from loguru import logger

from config.config import Config
from database.db_manager import DatabaseManager


def main():
    """Initialize database"""
    # Load environment variables
    load_dotenv()
    
    logger.info("Initializing database...")
    
    try:
        # Load configuration
        config = Config()
        
        # Initialize database
        db_manager = DatabaseManager(config)
        db_manager.initialize()
        
        logger.success("✓ Database initialized successfully!")
        logger.info(f"Database location: {config.database_path}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
