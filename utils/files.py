import os
import subprocess
from config import Config
from utils.logger import Logger

logger = Logger.get()

class FileManager:
    """Gerencia operações com arquivos OneDrive/SharePoint"""
    
    @staticmethod
    def free_space_folder(folder_path: str):
        """
        Remove cópia local de uma pasta inteira mantendo no SharePoint/OneDrive
        usando o comando attrib +U do Windows.
        
        Args:
            folder_path: Caminho completo da pasta
        """
        folder_path = os.path.normpath(folder_path)
        folder_name = os.path.basename(folder_path)
        
        if not os.path.exists(folder_path):
            logger.info(f"   Pasta '{folder_name}' nao encontrada localmente (ja liberada ou nao existe).")
            return False
        
        try:
            logger.info(f"   - Liberando espaco da pasta: {folder_name}...")
            
            # Aplicar atributo +U recursivamente na pasta
            os.system(f'attrib +U "{folder_path}" /S /D')
            
            logger.info(f"   OK - Pasta '{folder_name}' liberada com sucesso")
            return True
        
        except Exception as e:
            logger.warning(f"   AVISO - Erro ao liberar espaco da pasta '{folder_name}': {e}")
            return False