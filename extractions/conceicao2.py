from config import Config
from extractions.base import ExtractionBase

class ExtractionConceicao2(ExtractionBase):
    """Extração para o site Conceição II"""
    
    def __init__(self):
        site_name = "FEIT-BFI - Benef. Conceição II"
        output_file = Config.get_extraction_path("ITABIRA_CONCEICAO2.xlsx")
        super().__init__(site_name, output_file)

def run():
    extraction = ExtractionConceicao2()
    extraction.run()

if __name__ == "__main__":
    run()