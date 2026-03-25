import os
import subprocess
from config import Config
from utils.logger import Logger

logger = Logger.get()

class FileManager:
    """Gerencia operações com arquivos OneDrive/SharePoint"""
    
    @staticmethod
    def free_space(file_paths: list[str]):
        """
        Remove cópias locais dos arquivos mantendo-os no SharePoint/OneDrive
        usando o comando attrib +U do Windows.
        """
        logger.info("=" * 70)
        logger.info("PREPARAÇÃO: LIBERANDO ESPAÇO DOS ARQUIVOS LOCAIS (ONEDRIVE)")
        logger.info("=" * 70)
        
        files_processed = False
        
        for path in file_paths:
            path_win = os.path.normpath(path)
            filename = os.path.basename(path_win)
            
            if os.path.exists(path_win):
                try:
                    logger.info(f"   - Liberando espaço: {filename}...")
                    os.system(f'attrib +U "{path_win}"')
                    files_processed = True
                except Exception as e:
                    logger.warning(f"   ⚠ Erro ao liberar espaço de {filename}: {e}")
            else:
                logger.info(f"   ℹ {filename} não encontrado localmente (já liberado ou não existe).")
        
        if files_processed:
            logger.info("\n⏳ Aguardando o OneDrive processar (5 segundos)...")
            import time
            time.sleep(5)
            logger.info("✓ Preparação concluída!\n")
        else:
            logger.info("\n✓ Nenhuma cópia local precisava ser liberada.\n")
    
    @staticmethod
    def get_target_files() -> list[str]:
        """Retorna a lista de arquivos alvo para liberar espaço"""
        return [
            Config.get_extraction_path("ITABIRA_CAUE.xlsx"),
            Config.get_extraction_path("ITABIRA_CONCEICAO1.xlsx"),
            Config.get_extraction_path("ITABIRA_CONCEICAO2.xlsx"),
            Config.get_extraction_path("ITABIRA_MINA.xlsx"),
        ]