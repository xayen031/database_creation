from src.instruction_collector.instruction_collector import InstructionCollector
from src.excel_database_creator.excel_database_creator import create_database
from src.match_products import match_product_names

if __name__ == "__main__":
    collector = InstructionCollector()
    collector.collect()
    create_database()
    match_product_names("database.csv", "instructions", "database_updated.csv")
