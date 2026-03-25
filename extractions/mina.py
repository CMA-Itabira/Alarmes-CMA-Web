from config import Config
from extractions.base import ExtractionBase

class ExtractionMina(ExtractionBase):
    """Extração para a Mina Itabira"""
    
    def __init__(self):
        site_name = "FEIT-MIN - Equip. Móveis Mina Itabira"
        output_file = Config.get_extraction_path("ITABIRA_MINA.xlsx")
        super().__init__(site_name, output_file)

def run():
    extraction = ExtractionMina()
    extraction.run()

if __name__ == "__main__":
    run()