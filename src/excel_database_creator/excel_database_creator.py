import os
from loguru import logger
from pathlib import Path
from .src.config import Config
from .src.excel_processor import ExcelProcessor

def create_database():
    """Create database from Excel file."""
    try:
        # Get config with default paths
        current_dir = Path(__file__).parent
        config = Config(
            input_excel=current_dir / "mainbook.xlsx",
            product_names_json=current_dir / "product_names.json",
            product_types_json=current_dir / "product_types.json",
            output_csv="database.csv"
        )
        
        # Create excel processor
        processor = ExcelProcessor(config)
        
        # Process excel file
        processor.process()
        return True
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        return False

if __name__ == "__main__":
    create_database() 