from datetime import datetime
from pathlib import Path  # IMPORTANTE: Adicionado para manipular caminhos de pastas/arquivos
from utils.browser import BrowserManager
from utils.automation import WebAutomation
from utils.logger import Logger

logger = Logger.get()

class ExtractionBase:
    """Classe base para todas as extrações"""
    
    def __init__(self, site_name: str, output_filename: str):
        self.site_name = site_name
        self.output_filename = output_filename
        self.browser_manager = None
        self.automation = None
    
    def run(self):
        """Executa o fluxo de extração completo"""
        try:
            self._print_header()
            
            # Iniciar navegador
            self.browser_manager = BrowserManager()
            page = self.browser_manager.launch()
            self.automation = WebAutomation(page)
            
            # -------------------------------------------------------------
            # FLUXO 1: EXTRAÇÃO DE PONTOS ALARMADOS
            # -------------------------------------------------------------
            self.automation.navigate_to_alarms()
            
            if self.automation.open_configuration_dialog():
                try:
                    self.automation.configure_extraction(self.site_name)
                except Exception as e:
                    logger.error(f"✗ Erro ao preencher configuração: {e}")
            else:
                logger.warning("✗ Não foi possível abrir o diálogo de configuração")
                logger.warning("⚠ O script pode não funcionar corretamente")
            
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            
            self.automation.select_locations()
            self.automation.clear_responsibles()
            self.automation.set_date_range()
            self.automation.uncheck_pending_only()
            self.automation.search()
            self.automation.export_data(self.output_filename)
            
            page.wait_for_timeout(3000)
            
            # -------------------------------------------------------------
            # FLUXO 2: EXTRAÇÃO DE ANÁLISES REALIZADAS
            # -------------------------------------------------------------
            
            # Preparar o caminho do arquivo de análises
            original_path = Path(self.output_filename)
            
            # Criar a subpasta /Tratativas baseada no caminho original
            pasta_tratativas = original_path.parent / "Tratativas"
            pasta_tratativas.mkdir(exist_ok=True, parents=True)
            
            # Formar o novo nome do arquivo: Ex: ITABIRA_CONCEICAO1_ANALISES.xlsx
            novo_nome_arquivo = f"{original_path.stem}_ANALISES{original_path.suffix}"
            analises_output_path = str(pasta_tratativas / novo_nome_arquivo)
            
            # Executar automação de Análises
            self.automation.navigate_to_analises()
            self.automation.clear_responsibles_analises()
            self.automation.set_date_range_analises()
            self.automation.search_analises()
            self.automation.export_analises_table(analises_output_path)
            
            page.wait_for_timeout(3000)

            self._print_footer()
            return True
        
        except Exception as e:
            logger.error(f"✗ Erro na extração: {e}")
            return False
        
        finally:
            if self.browser_manager:
                self.browser_manager.close()
    
    def _print_header(self):
        """Imprime cabeçalho da execução"""
        logger.info("=" * 70)
        logger.info(f"EXTRAÇÃO CMA WEB - {self.site_name.upper()}")
        logger.info("=" * 70)
        logger.info(f"Horário de início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    def _print_footer(self):
        """Imprime rodapé da execução"""
        logger.info("\n" + "=" * 70)
        logger.info("PROCESSO FINALIZADO COM SUCESSO!")
        logger.info("=" * 70)