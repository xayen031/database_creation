from bs4 import BeautifulSoup
import logging
from pathlib import Path
from typing import List, Set
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class HTMLProcessor:
    """Handles HTML processing operations with proper error handling."""
    
    input_file: Path
    output_file: Path
    texts_to_remove: Set[str]
    classes_to_remove: Set[str]
    
    def __init__(
        self,
        input_file: str = 'temp/index2.html',
        output_file: str = 'temp/processed.html',
        texts_to_remove: List[str] = None,
        classes_to_remove: List[str] = None
    ):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.texts_to_remove = set(texts_to_remove or [
            "Kullanım Kılavuzu",
            "KULLANIM KILAVUZU",
            "Instructions For Use",
            "KULLANIM KLAVUZU"
        ])
        self.classes_to_remove = set(classes_to_remove or ['scroll-buttons', 'nav-buttons'])
        
    def _read_html(self) -> str:
        """Read the HTML file."""
        try:
            return self.input_file.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Error reading HTML file: {e}")
            raise
            
    def _write_html(self, content: str) -> None:
        """Write the processed HTML to file."""
        try:
            self.output_file.write_text(content, encoding='utf-8')
        except Exception as e:
            logger.error(f"Error writing HTML file: {e}")
            raise
            
    def _process_h2_tags(self, soup: BeautifulSoup) -> None:
        """Process h2 tags by removing specific texts."""
        h2_tags = soup.find_all('h2')
        logger.info(f"Found {len(h2_tags)} h2 tags")
        
        for h2 in h2_tags:
            h2_text = h2.get_text().strip()
            for text in self.texts_to_remove:
                if text in h2_text:
                    new_text = h2_text.replace(text, '').strip()
                    h2.string = new_text
                    logger.info(f"Removed text '{text}' from h2 tag. New text: '{new_text}'")
                    
    def _remove_elements_by_class(self, soup: BeautifulSoup) -> None:
        """Remove elements with specific classes."""
        for class_name in self.classes_to_remove:
            elements = soup.find_all(class_=class_name)
            for element in elements:
                element.decompose()
                logger.info(f"Removed element with class '{class_name}'")
                
    def _remove_first_h2(self, soup: BeautifulSoup) -> None:
        """Remove the first h2 tag."""
        first_h2 = soup.find('h2')
        if first_h2:
            first_h2.decompose()
            logger.info("Removed first h2 tag")
            
    def process(self) -> bool:
        """
        Process the HTML file by:
        1. Removing specific texts from h2 tags
        2. Removing elements with specific classes
        3. Removing the first h2 tag
        4. Saving the processed HTML
        """
        try:
            # Read and parse HTML
            content = self._read_html()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Process the HTML
            self._process_h2_tags(soup)
            self._remove_elements_by_class(soup)
            self._remove_first_h2(soup)
            
            # Save the processed HTML
            self._write_html(str(soup))
            
            logger.info("Successfully processed the HTML file")
            return True
            
        except Exception as e:
            logger.error(f"Error processing HTML: {e}")
            return False

def process_html() -> bool:
    """
    Convenience function to process the HTML file.
    Returns True if successful, False otherwise.
    """
    processor = HTMLProcessor()
    return processor.process()

if __name__ == "__main__":
    process_html() 