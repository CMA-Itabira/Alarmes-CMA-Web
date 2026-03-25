import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

class Config:
    """Gerenciador centralizado de configurações"""
    
    # Navegador
    EDGE_EXECUTABLE_PATH = os.getenv("EDGE_EXECUTABLE_PATH")
    EDGE_PROFILE_PATH = os.getenv("EDGE_PROFILE_PATH")
    
    # URLs
    CMA_WEB_URL = os.getenv("CMA_WEB_URL")
    
    # Caminhos
    BASE_SHAREPOINT_PATH = os.getenv("BASE_SHAREPOINT_PATH")
    SCRIPTS_DIRECTORY = os.getenv("SCRIPTS_DIRECTORY")
    LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "logs")
    SHAREPOINT_LOG_PATH = os.getenv("SHAREPOINT_LOG_PATH")
    RESUMO_EXECUCAO_PATH = os.getenv("RESUMO_EXECUCAO_PATH")
    
    # Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SAVE_LOG_SHAREPOINT = os.getenv("SAVE_LOG_SHAREPOINT", "true").lower() == "true"
    
    # Timeouts
    INPUT_TIMEOUT = int(os.getenv("INPUT_TIMEOUT", 15))
    WAIT_FOR_DOWNLOAD_TIMEOUT = int(os.getenv("WAIT_FOR_DOWNLOAD_TIMEOUT", 50000))
    NETWORK_IDLE_TIMEOUT = int(os.getenv("NETWORK_IDLE_TIMEOUT", 6000))
    DIALOG_OPEN_TIMEOUT = int(os.getenv("DIALOG_OPEN_TIMEOUT", 5000))
    
    # Extração
    EXTRACTION_AREA = os.getenv("EXTRACTION_AREA", "Mineração")
    EXTRACTION_PROFILE = os.getenv("EXTRACTION_PROFILE", "Normativo")
    DAYS_BACK = int(os.getenv("DAYS_BACK", 3))
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
    DISABLE_CACHE = os.getenv("DISABLE_CACHE", "true").lower() == "true"
    
    @staticmethod
    def get_extraction_path(filename: str) -> str:
        """Retorna o caminho completo para um arquivo de extração"""
        return f"{Config.BASE_SHAREPOINT_PATH}/{filename}"
    
    @staticmethod
    def validate():
        """Valida se todas as configurações obrigatórias estão presentes"""
        required_fields = [
            "EDGE_EXECUTABLE_PATH",
            "EDGE_PROFILE_PATH",
            "CMA_WEB_URL",
            "BASE_SHAREPOINT_PATH",
            "SCRIPTS_DIRECTORY",
            "SHAREPOINT_LOG_PATH",
            "RESUMO_EXECUCAO_PATH"
        ]
        
        missing = [field for field in required_fields if not getattr(Config, field, None)]
        
        if missing:
            raise ValueError(f"Configurações obrigatórias faltando: {', '.join(missing)}")
        
        return True