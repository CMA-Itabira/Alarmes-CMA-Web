from config import Config
from extractions.base import ExtractionBase

class ExtractionCaue(ExtractionBase):
    """Extração para o site Cauê"""
    
    def __init__(self):
        site_name = "FEIT-BFC - Benef. Cauê"
        output_file = Config.get_extraction_path("ITABIRA_CAUE.xlsx")
        super().__init__(site_name, output_file)

def run():
    extraction = ExtractionCaue()
    extraction.run()

if __name__ == "__main__":
    run()