from config import Config
from extractions.base import ExtractionBase

class ExtractionConceicao1(ExtractionBase):
    """Extração para o site Conceição I"""
    
    def __init__(self):
        site_name = "FEIT-BFO - Benef. Conceição I"
        output_file = Config.get_extraction_path("ITABIRA_CONCEICAO1.xlsx")
        super().__init__(site_name, output_file)

def run():
    extraction = ExtractionConceicao1()
    extraction.run()

if __name__ == "__main__":
    run()