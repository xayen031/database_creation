from bs4 import BeautifulSoup
import logging
from pathlib import Path
import re
from typing import List, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SectionSeparator:
    """Handles HTML section separation and file creation."""
    
    input_file: Path
    output_dir: Path
    
    def __init__(
        self,
        input_file: str = 'temp/processed.html',
        output_dir: str = 'instructions'
    ):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        
    def _create_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _read_html(self) -> str:
        """Read the HTML file."""
        try:
            return self.input_file.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Error reading HTML file: {e}")
            raise
            
    @staticmethod
    def clean_filename(text: str) -> str:
        """
        Clean the text to create a valid filename.
        Removes invalid characters and replaces spaces with underscores.
        """
        # Remove invalid characters and replace spaces with underscores
        cleaned = re.sub(r'[<>:"/\\|?*]', '', text)
        cleaned = cleaned.replace(' ', '_')
        return cleaned.strip() or 'unnamed_section'
        
    def _get_section_content(self, start_tag: BeautifulSoup, end_tag: Optional[BeautifulSoup] = None) -> List[str]:
        """Get content between two h2 tags."""
        content = []
        current = start_tag.next_sibling
        
        while current and current != end_tag:
            if isinstance(current, str):
                text = current.strip()
            else:
                text = current.get_text().strip()
            if text:
                content.append(text)
            current = current.next_sibling
            
        return content
        
    def _save_section(self, filename: str, content: List[str]) -> None:
        """Save section content to a file."""
        try:
            file_path = self.output_dir / f"{filename}.txt"
            file_path.write_text('\n'.join(content), encoding='utf-8')
            logger.info(f"Saved section to {file_path}")
        except Exception as e:
            logger.error(f"Error saving section {filename}: {e}")
            raise
            
    def separate(self) -> bool:
        """
        Separate the HTML content into sections based on h2 tags
        and save each section as a separate text file.
        """
        try:
            # Create output directory
            self._create_output_dir()
            
            # Read and parse HTML
            content = self._read_html()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find all h2 tags
            h2_tags = soup.find_all('h2')
            logger.info(f"Found {len(h2_tags)} sections to process")
            
            # Process each section
            for i, h2 in enumerate(h2_tags):
                # Get section content
                if i < len(h2_tags) - 1:
                    section_content = self._get_section_content(h2, h2_tags[i + 1])
                else:
                    section_content = self._get_section_content(h2)
                    
                # Create filename from h2 text
                filename = self.clean_filename(h2.get_text())
                
                # Save the section
                self._save_section(filename, section_content)
                
            logger.info("Successfully separated sections into text files")
            return True
            
        except Exception as e:
            logger.error(f"Error separating sections: {e}")
            return False

def separate_sections() -> bool:
    """
    Convenience function to separate sections from the HTML file.
    Returns True if successful, False otherwise.
    """
    separator = SectionSeparator()
    return separator.separate()

if __name__ == "__main__":
    separate_sections() 