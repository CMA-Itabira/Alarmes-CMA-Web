from playwright.sync_api import sync_playwright, BrowserContext, Page
from config import Config
from utils.logger import Logger

logger = Logger.get()

class BrowserManager:
    """Gerencia instância do navegador Playwright"""
    
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None
    
    def launch(self) -> Page:
        """Lança o navegador e retorna a página"""
        try:
            logger.info("Iniciando navegador Edge...")
            
            self.playwright = sync_playwright().start()
            
            cache_args = []
            if Config.DISABLE_CACHE:
                cache_args = [
                    '--disable-cache',
                    '--disable-application-cache',
                    '--disable-offline-load-stale-cache',
                    '--disk-cache-size=0'
                ]
            
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=Config.EDGE_PROFILE_PATH,
                executable_path=Config.EDGE_EXECUTABLE_PATH,
                headless=Config.HEADLESS_MODE,
                channel="msedge",
                args=cache_args
            )
            
            self.page = self.context.new_page()
            logger.info("✓ Navegador iniciado com sucesso")
            logger.info("✓ Cache limpos")
            
            return self.page
        
        except Exception as e:
            logger.error(f"Erro ao iniciar navegador: {e}")
            raise
    
    def close(self):
        """Fecha o navegador e libera recursos"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Navegador fechado")
        except Exception as e:
            logger.error(f"Erro ao fechar navegador: {e}")