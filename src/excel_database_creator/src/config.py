from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, List

class ExcelConfig(BaseModel):
    """Configuration for Excel processing."""
    sheet_name: str = Field(default="DATABASE", description="Name of the Excel sheet to process")
    columns_to_keep: List[str] = Field(
        default=[
            'Unnamed: 1', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5',
            'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 12', 'Unnamed: 13'
        ],
        description="List of columns to keep from the Excel file"
    )
    column_rename_map: Dict[str, str] = Field(
        default={
            'Unnamed: 1': 'PRODUCT_CODE',
            'Unnamed: 3': 'PRODUCT_VARIANT',
            'Unnamed: 4': 'PRODUCT_COLOR',
            'Unnamed: 7': 'PRODUCT_NAME',
            'Unnamed: 8': 'UTS',
            'Unnamed: 12': 'PRODUCT_PACKING_INFO',
            'Unnamed: 13': 'PRODUCT_ATTRIBUTES'
        },
        description="Mapping of old column names to new column names"
    )
    desired_column_order: List[str] = Field(
        default=[
            'PRODUCT_CODE', 'PRODUCT_VARIANT', 'PRODUCT_COLOR',
            'Unnamed: 5', 'Unnamed: 6', 'PRODUCT_NAME',
            'PRODUCT_TYPE', 'PRODUCT_PACKING_INFO',
            'PRODUCT_ATTRIBUTES', 'UTS'
        ],
        description="Desired order of columns in the output"
    )

class Config(BaseModel):
    """Main configuration class."""
    excel_config: ExcelConfig = Field(default_factory=ExcelConfig)
    input_excel: Path = Field(description="Path to input Excel file")
    product_names_json: Path = Field(description="Path to product names JSON file")
    product_types_json: Path = Field(description="Path to product types JSON file")
    output_csv: Path = Field(description="Path to output CSV file") 