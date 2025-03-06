import logging
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

from .src.download_webpage import WebPageDownloader
from .src.process_html import HTMLProcessor
from .src.separate_sections import SectionSeparator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class InstructionCollector:
    """Main class to orchestrate the instruction collection process."""
    
    url: str
    temp_dir: Path
    instructions_dir: Path
    
    def __init__(
        self,
        url: str = "https://ifu.imicryl.com/index2.html",
        temp_dir: str = "temp",
        instructions_dir: str = "instructions"
    ):
        self.url = url
        self.temp_dir = Path(temp_dir)
        self.instructions_dir = Path(instructions_dir)
        
    def _create_directories(self) -> None:
        """Create necessary directories."""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.instructions_dir.mkdir(parents=True, exist_ok=True)
        
    def _download_webpage(self) -> bool:
        """Download the webpage."""
        downloader = WebPageDownloader(self.url, str(self.temp_dir))
        return downloader.download()
        
    def _process_html(self) -> bool:
        """Process the downloaded HTML file."""
        processor = HTMLProcessor(
            input_file=str(self.temp_dir / 'index2.html'),
            output_file=str(self.temp_dir / 'processed.html')
        )
        return processor.process()
        
    def _separate_sections(self) -> bool:
        """Separate the processed HTML into sections."""
        separator = SectionSeparator(
            input_file=str(self.temp_dir / 'processed.html'),
            output_dir=str(self.instructions_dir)
        )
        return separator.separate()
        
    def collect(self) -> bool:
        """
        Orchestrate the entire instruction collection process:
        1. Create necessary directories
        2. Download the webpage
        3. Process the HTML
        4. Separate sections into individual files
        """
        try:
            logger.info("Starting the instruction collection process...")
            
            # Create directories
            self._create_directories()
            
            # Step 1: Download webpage
            if not self._download_webpage():
                logger.error("Failed to download webpage. Exiting...")
                return False
                
            # Step 2: Process HTML
            if not self._process_html():
                logger.error("Failed to process HTML. Exiting...")
                return False
                
            # Step 3: Separate sections
            if not self._separate_sections():
                logger.error("Failed to separate sections. Exiting...")
                return False
                
            logger.info("Process completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Unexpected error during process: {e}")
            return False

def main() -> None:
    """Main entry point for the instruction collector."""
    collector = InstructionCollector()
    collector.collect()

if __name__ == "__main__":
    main() 