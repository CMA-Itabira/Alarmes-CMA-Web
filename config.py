import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env com caminho absoluto
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    """Gerenciador centralizado de configuracoes"""
    
    # Navegador
    EDGE_EXECUTABLE_PATH = os.getenv("EDGE_EXECUTABLE_PATH")
    EDGE_PROFILE_PATH = os.getenv("EDGE_PROFILE_PATH")
    
    # URLs
    CMA_WEB_URL = os.getenv("CMA_WEB_URL")
    CMA_WEB_ANALISES_URL = os.getenv("CMA_WEB_ANALISES_URL")
    
    # Caminhos
    BASE_SHAREPOINT_PATH = os.getenv("BASE_SHAREPOINT_PATH")
    SCRIPTS_DIRECTORY = os.getenv("SCRIPTS_DIRECTORY")
    
    # LOG_DIRECTORY com caminho absoluto
    _log_dir_env = os.getenv("LOG_DIRECTORY", "logs")
    if os.path.isabs(_log_dir_env):
        LOG_DIRECTORY = _log_dir_env
    else:
        LOG_DIRECTORY = str(Path(__file__).parent / _log_dir_env)
    
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
    
    # Extracao
    EXTRACTION_AREA = os.getenv("EXTRACTION_AREA", "Mineracao")
    EXTRACTION_PROFILE = os.getenv("EXTRACTION_PROFILE", "Normativo")
    DAYS_BACK = int(os.getenv("DAYS_BACK", 3))
    DAYS_BACK_ANALISES = int(os.getenv("DAYS_BACK_ANALISES", 90))
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
    DISABLE_CACHE = os.getenv("DISABLE_CACHE", "true").lower() == "true"
    
    @staticmethod
    def get_extraction_path(filename: str) -> str:
        """Retorna o caminho completo para um arquivo de extracao"""
        return f"{Config.BASE_SHAREPOINT_PATH}/{filename}"
    
    @staticmethod
    def validate():
        """Valida se todas as configuracoes obrigatorias estao presentes"""
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
            raise ValueError(f"Configuracoes obrigatorias faltando: {', '.join(missing)}")
        
        return True