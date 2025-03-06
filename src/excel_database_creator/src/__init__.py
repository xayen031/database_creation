"""
Excel Database Creator - A professional Python application for processing Excel data.
"""

__version__ = "1.0.0"

"""
Source modules for excel database creator
"""

from .config import Config
from .excel_processor import ExcelProcessor

__all__ = ['Config', 'ExcelProcessor'] 