import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from config import Config

class Logger:
    """Sistema centralizado de logging com suporte a SharePoint"""
    
    _logger = None
    _log_file = None
    
    @classmethod
    def setup(cls):
        """Configura o logger"""
        if cls._logger is not None:
            return cls._logger
        
        # Criar diretório local de logs se não existir
        os.makedirs(Config.LOG_DIRECTORY, exist_ok=True)
        
        # Criar logger
        cls._logger = logging.getLogger("ExtracaoDados")
        cls._logger.setLevel(Config.LOG_LEVEL)
        
        # Limpar handlers anteriores
        cls._logger.handlers.clear()
        
        # Formato com quebra de linha
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        
        # Nome do arquivo de log
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"extracaodados_{timestamp}.log"
        cls._log_file = os.path.join(Config.LOG_DIRECTORY, log_filename)
        
        # Handler para arquivo local
        file_handler = logging.FileHandler(cls._log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(Config.LOG_LEVEL)
        cls._logger.addHandler(file_handler)
        
        # Handler para console com flush automático
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(Config.LOG_LEVEL)
        cls._logger.addHandler(console_handler)
        
        # Força flush após cada mensagem
        cls._logger.propagate = False
        
        return cls._logger
    
    @classmethod
    def get(cls):
        """Retorna o logger"""
        if cls._logger is None:
            cls.setup()
        return cls._logger
    
    @classmethod
    def get_log_file(cls):
        """Retorna o caminho do arquivo de log"""
        return cls._log_file
    
    @classmethod
    def save_to_sharepoint(cls):
        """Copia o arquivo de log para o SharePoint"""
        if not Config.SAVE_LOG_SHAREPOINT or not cls._log_file:
            return False
        
        try:
            # Criar diretório no SharePoint se não existir
            sharepoint_path = os.path.normpath(Config.SHAREPOINT_LOG_PATH)
            os.makedirs(sharepoint_path, exist_ok=True)
            
            # Nome do arquivo
            log_filename = os.path.basename(cls._log_file)
            destination = os.path.join(sharepoint_path, log_filename)
            
            # Copiar arquivo
            shutil.copy2(cls._log_file, destination)
            
            cls._logger.info(f"✓ Log salvo no SharePoint: {destination}")
            return True
        
        except Exception as e:
            cls._logger.error(f"⚠ Erro ao salvar log no SharePoint: {e}")
            return False