from pathlib import Path
from typing import Dict, Any
import pandas as pd
import json
from loguru import logger
from .config import Config

class ExcelProcessor:
    """Handles the processing of Excel data and JSON mappings."""
    
    def __init__(self, config: Config):
        """Initialize the data processor with configuration."""
        self.config = config
        self.product_names_mapping: Dict[str, str] = {}
        self.product_types_mapping: Dict[str, str] = {}
        
    def load_json_mappings(self) -> None:
        """Load product name and type mappings from JSON files."""
        try:
            with open(self.config.product_names_json, 'r', encoding='utf-8') as f:
                self.product_names_mapping = json.load(f)
            with open(self.config.product_types_json, 'r', encoding='utf-8') as f:
                self.product_types_mapping = json.load(f)
            logger.info("Successfully loaded JSON mappings")
        except Exception as e:
            logger.error(f"Error loading JSON mappings: {e}")
            raise

    def read_excel(self) -> pd.DataFrame:
        """Read and preprocess the Excel file."""
        try:
            df = pd.read_excel(
                self.config.input_excel,
                sheet_name=self.config.excel_config.sheet_name,
                engine='openpyxl',
                usecols=self.config.excel_config.columns_to_keep
            )
            logger.info(f"Successfully read Excel file: {self.config.input_excel}")
            return df
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            raise

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the DataFrame with all necessary transformations."""
        try:
            # Rename columns
            df.rename(columns=self.config.excel_config.column_rename_map, inplace=True)
            
            # Drop header rows and reset index
            df = df.drop(index=[0, 1]).reset_index(drop=True)
            
            # Clean product variants and colors
            self._clean_product_variants(df)
            
            # Filter rows
            df = df[df['UTS'] == 'KAYITLI'].reset_index(drop=True)
            
            # Apply mappings
            df['PRODUCT_NAME'] = df['PRODUCT_CODE'].map(self.product_names_mapping)
            df['PRODUCT_TYPE'] = df['PRODUCT_CODE'].map(self.product_types_mapping)
            
            # Reorder columns
            df = df[self.config.excel_config.desired_column_order]
            
            logger.info("Successfully processed DataFrame")
            return df
        except Exception as e:
            logger.error(f"Error processing DataFrame: {e}")
            raise

    def _clean_product_variants(self, df: pd.DataFrame) -> None:
        """Clean product variants and colors by removing redundant information."""
        # Clean product colors
        mask_color = df['PRODUCT_COLOR'].notna() & df['PRODUCT_VARIANT'].notna()
        df.loc[mask_color, 'PRODUCT_COLOR'] = [
            color.replace(variant, '')
            for color, variant in zip(
                df.loc[mask_color, 'PRODUCT_COLOR'],
                df.loc[mask_color, 'PRODUCT_VARIANT']
            )
        ]
        
        # Clean product variants
        mask_variant = df['PRODUCT_VARIANT'].notna() & df['PRODUCT_CODE'].notna()
        df.loc[mask_variant, 'PRODUCT_VARIANT'] = [
            variant.replace(code, '')
            for variant, code in zip(
                df.loc[mask_variant, 'PRODUCT_VARIANT'],
                df.loc[mask_variant, 'PRODUCT_CODE']
            )
        ]

    def save_to_csv(self, df: pd.DataFrame) -> None:
        """Save the processed DataFrame to CSV."""
        try:
            df.to_csv(self.config.output_csv, index=False)
            logger.info(f"Successfully saved data to: {self.config.output_csv}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            raise

    def process(self) -> None:
        """Execute the complete data processing pipeline."""
        try:
            self.load_json_mappings()
            df = self.read_excel()
            processed_df = self.process_dataframe(df)
            self.save_to_csv(processed_df)
            logger.info("Data processing completed successfully")
        except Exception as e:
            logger.error(f"Error in processing pipeline: {e}")
            raise 