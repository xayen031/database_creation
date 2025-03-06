import requests
import os
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebPageDownloader:
    """Handles webpage downloading with proper encoding detection and error handling."""
    
    def __init__(self, url: str, output_dir: str = 'temp'):
        self.url = url
        self.output_dir = Path(output_dir)
        self.output_file = self.output_dir / 'index2.html'
        
    def _create_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _validate_url(self) -> bool:
        """Validate the URL format."""
        try:
            result = urlparse(self.url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
            
    def _detect_encoding(self, content: bytes) -> Optional[str]:
        """Detect the encoding of the content."""
        try:
            import chardet
            result = chardet.detect(content)
            return result['encoding']
        except Exception as e:
            logger.error(f"Error detecting encoding: {e}")
            return None
            
    def download(self) -> bool:
        """
        Download the webpage with proper encoding detection and save as UTF-8.
        Returns True if successful, False otherwise.
        """
        try:
            # Validate URL
            if not self._validate_url():
                logger.error("Invalid URL format")
                return False
                
            # Create output directory
            self._create_output_dir()
            
            # Download the webpage
            logger.info(f"Downloading webpage from {self.url}")
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            
            # Detect encoding
            encoding = self._detect_encoding(response.content)
            if not encoding:
                logger.error("Could not detect encoding")
                return False
                
            # Decode and save content
            content = response.content.decode(encoding)
            self.output_file.write_text(content, encoding='utf-8')
            
            logger.info(f"Successfully downloaded and saved the webpage with {encoding} encoding")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Network error while downloading: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False

def download_webpage(url: str = "https://ifu.imicryl.com/index2.html") -> bool:
    """
    Convenience function to download the webpage.
    Returns True if successful, False otherwise.
    """
    downloader = WebPageDownloader(url)
    return downloader.download()

if __name__ == "__main__":
    download_webpage() 