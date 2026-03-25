import os
import csv
from datetime import datetime
from config import Config
from utils.logger import Logger

logger = Logger.get()

class StatusExecucao:
    """Enum para status de execução"""
    SUCESSO = "Sucesso"
    SUCESSO_COM_EXCECAO = "Sucesso com Exceção"
    FALHA_PARCIAL = "Falha Parcial"
    FALHA_TOTAL = "Falha Total"

class ResumoDados:
    """Gerencia o arquivo CSV de resumo de execução"""
    
    SCRIPT_ID = 1
    SCRIPT_NAME = "Extracao CMA Web"
    
    @staticmethod
    def _ensure_file_exists():
        """Garante que o arquivo CSV existe com headers"""
        resumo_path = os.path.normpath(Config.RESUMO_EXECUCAO_PATH)
        
        # Criar diretório pai se não existir
        os.makedirs(os.path.dirname(resumo_path), exist_ok=True)
        
        # Se não existir, criar com headers
        if not os.path.exists(resumo_path):
            with open(resumo_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['ID', 'Nome_Script', 'Data_Hora', 'Status', 'Detalhes'])
    
    @staticmethod
    def adicionar_resultado(status: str, detalhes: str = ""):
        """
        Adiciona uma nova linha ao arquivo de resumo
        
        Args:
            status: Status da execução (use StatusExecucao)
            detalhes: Detalhes resumidos do que aconteceu (máx 200 caracteres)
        """
        try:
            ResumoDados._ensure_file_exists()
            
            resumo_path = os.path.normpath(Config.RESUMO_EXECUCAO_PATH)
            data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            # Limitar detalhes a 200 caracteres
            detalhes = detalhes[:200] if detalhes else ""
            
            # Adicionar nova linha
            with open(resumo_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    ResumoDados.SCRIPT_ID, 
                    ResumoDados.SCRIPT_NAME, 
                    data_hora, 
                    status, 
                    detalhes
                ])
            
            logger.info(f"✓ Resumo atualizado: {status}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar resumo: {e}")
            return False