from playwright.sync_api import Page
from datetime import datetime, timedelta
from config import Config
from utils.logger import Logger

logger = Logger.get()

class WebAutomation:
    """Automações reutilizáveis para a página CMA Web"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to_analises(self):
        """Navega para a página de análises realizadas"""
        logger.info("11. Navegando para Análises Realizadas...")
        self.page.goto(Config.CMA_WEB_ANALISES_URL)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)

    
    def clear_responsibles_analises(self):
        """Limpa todos os filtros clicando no botão 'Limpar Filtro'"""
        logger.info("12. Limpando filtros da tela...")
        try:
            # Localiza o botão que contém o texto "Limpar Filtro" e clica nele
            btn_limpar = self.page.locator('button:has-text("Limpar Filtro")').first
            btn_limpar.click(force=True)
            
            # Aguarda 1 segundo para a tela resetar os campos
            self.page.wait_for_timeout(1000)
            
            logger.info("   ✓ Filtros limpos com sucesso")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao clicar no botão Limpar Filtro: {e}")

    def set_date_range_analises(self, days_back: int = None):
        """Define o intervalo de datas usando navegação pelo calendário"""
        if days_back is None:
            days_back = Config.DAYS_BACK_ANALISES
            
        today = datetime.today()
        start_date = today - timedelta(days=days_back)
        
        logger.info(f"13. Definindo período de análises ({start_date.strftime('%d/%m/%Y')} a {today.strftime('%d/%m/%Y')})...")
        try:
            # --- 1. PREENCHER DATA DE INÍCIO ---
            logger.info("   - Abrindo calendário de Início...")
            btn_calendario_inicio = self.page.locator('app-reusable-datepicker[formcontrolname="dataInicio"] button[aria-label="Open calendar"]')
            btn_calendario_inicio.click(force=True)
            self.page.wait_for_timeout(1000)
            
            # Calcula a diferença de meses para voltar
            meses_diferenca = (today.year - start_date.year) * 12 + today.month - start_date.month
            
            if meses_diferenca > 0:
                logger.info(f"   - Voltando {meses_diferenca} mês(es) no calendário...")
                botao_mes_anterior = self.page.locator("button.mat-calendar-previous-button")
                for _ in range(meses_diferenca):
                    botao_mes_anterior.click(force=True)
                    self.page.wait_for_timeout(500)
            
            # Formata a data para achar o aria-label exato (ex: "13/05/2026")
            str_data_inicio = start_date.strftime("%d/%m/%Y")
            logger.info(f"   - Clicando no dia {str_data_inicio}...")
            
            # Busca o botão do dia exato globalmente (usando a classe mat-calendar-body-cell e o aria-label)
            btn_dia_inicio = self.page.locator(f'button.mat-calendar-body-cell[aria-label="{str_data_inicio}"]')
            btn_dia_inicio.click(force=True)
            self.page.wait_for_timeout(1000)
            
            # --- 2. PREENCHER DATA DE FIM ---
            logger.info("   - Abrindo calendário de Fim...")
            btn_calendario_fim = self.page.locator('app-reusable-datepicker[formcontrolname="dataFim"] button[aria-label="Open calendar"]')
            btn_calendario_fim.click(force=True)
            self.page.wait_for_timeout(1000)
            
            # Clica no botão HOJE da interface
            logger.info("   - Clicando no botão HOJE...")
            btn_hoje = self.page.locator("button.today-action-button")
            btn_hoje.click(force=True)
            self.page.wait_for_timeout(1000)
            
            logger.info("   ✓ Período de análises definido")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao definir datas nas análises usando calendário: {e}")

    def search_analises(self):
        """Realiza a pesquisa na tela de análises"""
        logger.info("14. Realizando pesquisa de análises...")
        try:
            self.page.get_by_role("button", name="Pesquisar").click()
            self.page.wait_for_timeout(3000)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(Config.NETWORK_IDLE_TIMEOUT)
            logger.info("   ✓ Pesquisa concluída")
        except Exception as e:
            logger.error(f"   ✗ Erro ao pesquisar análises: {e}")
            raise

    def export_analises_table(self, output_path: str):
        """Exporta a tabela de análises para o Excel"""
        logger.info(f"15. Exportando tabela de análises...")
        try:
            with self.page.expect_download(timeout=Config.WAIT_FOR_DOWNLOAD_TIMEOUT) as download_info:
                # Usa o wrapper customizado do Angular e clica no botão dentro dele
                btn_exportar = self.page.locator('app-export-excel-from-backend button').first
                btn_exportar.click(force=True)
            
            download = download_info.value
            download.save_as(output_path)
            
            logger.info("   ✓ Download de análises concluído!")
            logger.info(f"   ✓ Arquivo salvo em: {output_path}")
        except Exception as e:
            logger.error(f"   ✗ Erro ao exportar tabela de análises: {e}")
            raise

    def navigate_to_alarms(self):
        """Navega para a página de pontos alarmados"""
        logger.info("1. Navegando para a página...")
        self.page.goto(Config.CMA_WEB_URL)
        
        logger.info("2. Aguardando autenticação...")
        self.page.wait_for_url("**/analises/pontos-alarmados", timeout=60000)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
    
    def open_configuration_dialog(self) -> bool:
        """Abre o diálogo de configuração. Retorna True se aberto com sucesso"""
        logger.info("3. Verificando diálogo de configuração...")
        
        dialog_visible = False
        
        # Verificar se já está aberto
        try:
            dialog = self.page.locator("mat-dialog-container, .mat-mdc-dialog-container").first
            dialog.wait_for(state="visible", timeout=2000)
            dialog_visible = True
            logger.info("   ✓ Diálogo já está aberto")
        except:
            logger.info("   ℹ Diálogo está fechado, abrindo...")
        
        # Se não estiver aberto, abrir
        if not dialog_visible:
            try:
                self.page.get_by_text("expand_more").click()
                self.page.wait_for_timeout(1500)
                
                dialog = self.page.locator("mat-dialog-container, .mat-mdc-dialog-container").first
                dialog.wait_for(state="visible", timeout=Config.DIALOG_OPEN_TIMEOUT)
                dialog_visible = True
                logger.info("   ✓ Diálogo aberto com sucesso")
            except Exception as e:
                logger.warning(f"   ✗ Erro ao abrir diálogo: {e}")
                logger.warning("   ⚠ Não será possível configurar. Continuando...")
        
        return dialog_visible
    
    def configure_extraction(self, site_name: str):
        """
        Configura a extração com a área, site e perfil
        
        Args:
            site_name: Nome do site a ser selecionado (ex: "FEIT-BFC - Benef. Cauê")
        """
        logger.info(f"   - Selecionando Área: {Config.EXTRACTION_AREA}...")
        self.page.locator("#areaInputTest").click()
        self.page.wait_for_timeout(500)
        self.page.locator(f"[id=\"{Config.EXTRACTION_AREA}-option\"]").get_by_text(Config.EXTRACTION_AREA).click()
        self.page.wait_for_timeout(1000)
        
        logger.info(f"   - Selecionando Site: {site_name}...")
        
        self.page.locator("[id=\"siteInputTree\"]").click()
        self.page.wait_for_timeout(500)
        self.page.locator("[id=\"item.name\"]").get_by_text(site_name).click()
        self.page.wait_for_timeout(1000)
        
        logger.info(f"   - Selecionando Perfil: {Config.EXTRACTION_PROFILE}...")
        self.page.get_by_label("Perfil").click()
        self.page.wait_for_timeout(500)
        self.page.locator("[id=\"[object Object]-option\"]").get_by_text(Config.EXTRACTION_PROFILE).click()
        self.page.wait_for_timeout(1500)
    
    def select_locations(self):
        """Seleciona todos os locais"""
        logger.info("4. Selecionando todos os locais...")
        try:
            self.page.wait_for_timeout(1000)
            logger.info("✓ Locais selecionados")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao selecionar locais: {e}")
    
    def clear_responsibles(self):
        """Limpa a seleção de responsáveis"""
        logger.info("5. Limpando responsáveis...")
        try:
            self.page.locator("[id=\"'inputMultiSelectOpenOpcoes\"]").click()
            self.page.wait_for_timeout(1000)
            self.page.locator("[id=\"'idBotaoLimparSelecionado'\"]").click()
            self.page.wait_for_timeout(1000)
            
            logger.info("   - Fechando dropdown...")
            try:
                if self.page.locator("#cdk-overlay-0").is_visible():
                    self.page.mouse.click(50, 50)
                    self.page.wait_for_timeout(500)
                    logger.info("   ✓ Dropdown fechado")
            except Exception as e:
                logger.warning(f"   ⚠ Erro: {e}")
            
            logger.info("✓ Responsáveis limpos")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao limpar responsáveis: {e}")
    
    def set_date_range(self, days_back: int = None):
        """Define o intervalo de datas"""
        if days_back is None:
            days_back = Config.DAYS_BACK
        
        today = datetime.today()
        start_date = today - timedelta(days=days_back)
        
        logger.info(f"6. Selecionando data inicial: {start_date.strftime('%d/%m/%Y')}...")
        try:
            self.page.locator("#selectPeriodoInicio--toggle").get_by_role("button", name="Open calendar").click()
            self.page.wait_for_timeout(1000)
            
            if start_date.month != today.month:
                logger.info("   ↩ Voltando um mês no calendário...")
                self.page.locator("mat-datepicker-content .mat-calendar-previous-button").click()
                self.page.wait_for_timeout(700)
            
            day = start_date.day
            self.page.get_by_role("button", name=f"{day}/", exact=False).first.click()
            self.page.wait_for_timeout(1000)
            logger.info(f"✓ Data inicial selecionada: {start_date.strftime('%d/%m/%Y')}")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao selecionar data inicial: {e}")
            try:
                self.page.locator("#selectPeriodoInicio").fill(start_date.strftime("%d/%m/%Y"))
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(1000)
            except:
                logger.warning("   ⚠ Não foi possível definir data inicial")
        
        logger.info(f"7. Selecionando data final: {today.strftime('%d/%m/%Y')}...")
        try:
            self.page.locator("#codigo-1").click()
            self.page.wait_for_timeout(500)
            self.page.locator("button.today-action-button").click()
            self.page.wait_for_timeout(1000)
            logger.info(f"✓ Data final selecionada: {today.strftime('%d/%m/%Y')}")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao selecionar data final: {e}")
            try:
                self.page.locator("#codigo-1").fill(today.strftime("%d/%m/%Y"))
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(1000)
            except:
                logger.warning("   ⚠ Não foi possível definir data final")
    
    def uncheck_pending_only(self):
        """Desmarca a opção 'Apenas Pendente'"""
        logger.info("8. Desmarcando 'Apenas Pendente'...")
        try:
            checkbox = self.page.get_by_role("checkbox", name="Apenas Pendente")
            if checkbox.is_checked():
                checkbox.uncheck()
            self.page.wait_for_timeout(1000)
            logger.info("✓ 'Apenas Pendente' desmarcado")
        except Exception as e:
            logger.warning(f"   ⚠ Erro ao desmarcar pendente: {e}")
    
    def search(self):
        """Realiza a pesquisa"""
        logger.info("9. Realizando pesquisa...")
        try:
            self.page.get_by_role("button", name="Pesquisar").click()
            self.page.wait_for_timeout(6000)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(Config.NETWORK_IDLE_TIMEOUT)
            logger.info("✓ Pesquisa realizada com sucesso")
        except Exception as e:
            logger.error(f"   ✗ Erro ao pesquisar: {e}")
            raise
    
    def export_data(self, output_path: str):
        """Exporta os dados para um arquivo"""
        logger.info("10. Exportando dados...")
        try:
            with self.page.expect_download(timeout=Config.WAIT_FOR_DOWNLOAD_TIMEOUT) as download_info:
                self.page.get_by_role("button", name="Exportar Dados").click()
            
            download = download_info.value
            download.save_as(output_path)
            
            logger.info("✓ Download concluído!")
            logger.info(f"✓ Arquivo salvo em: {output_path}")
        except Exception as e:
            logger.error(f"   ✗ Erro ao exportar dados: {e}")
            raise