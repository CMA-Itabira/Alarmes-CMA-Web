from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def run():
    with sync_playwright() as p:
        # Configurações do Edge
        caminho_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        caminho_perfil = r"C:\Users\81057638\AppData\Local\Microsoft\Edge\User Data\Default"
        
        print("="*70)
        print("EXTRAÇÃO CMA WEB - PONTOS ALARMADOS")
        print("="*70)
        print(f"Perfil: {caminho_perfil}\n")
        
        # Iniciar navegador com perfil persistente
        context = p.chromium. launch_persistent_context(
            user_data_dir=caminho_perfil,
            executable_path=caminho_edge,
            headless=False,
            channel="msedge",
            args=[
                '--disable-cache',
                '--disable-application-cache',
                '--disable-offline-load-stale-cache',
                '--disk-cache-size=0'
            ]
        )
        
        page = context.new_page()
        
        print("✓ Cache limpos")
        
        # Passo 1: Navegar para a página
        print("1. Navegando para a página...")
        page.goto("https://prd.webapp.cmaweb.valenet.valeglobal.net/analises/pontos-alarmados")
        
        # Aguardar autenticação automática
        print("2. Aguardando autenticação...")
        page.wait_for_url("**/analises/pontos-alarmados", timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        
        # Verificar se o diálogo de configuração aparece
        print("3. Verificando diálogo de configuração...")

        dialogo_visivel = False

        # PRIMEIRO: Verificar se o diálogo JÁ está aberto
        try:
            dialogo = page.locator("mat-dialog-container, . mat-mdc-dialog-container").first
            dialogo.wait_for(state="visible", timeout=2000)
            dialogo_visivel = True
            print("   ✓ Diálogo já está aberto")
        except:
            print("   ℹ Diálogo está fechado, abrindo...")

        # Se NÃO estiver aberto, abrir agora
        if not dialogo_visivel: 
            try:
                # Clicar no ícone expand_more para abrir o diálogo
                page.get_by_text("expand_more").click()
                page.wait_for_timeout(1500)
                
                # Verificar se abriu
                dialogo = page.locator("mat-dialog-container, .mat-mdc-dialog-container").first
                dialogo.wait_for(state="visible", timeout=5000)
                dialogo_visivel = True
                print("   ✓ Diálogo aberto com sucesso")
            except Exception as e:
                print(f"   ✗ Erro ao abrir diálogo: {e}")
                print("   ⚠ Não será possível configurar.  Continuando...")

        # AGORA SIM: Preencher o diálogo (só se estiver aberto)
        if dialogo_visivel:
            try: 
                # Selecionar Área - Mineração
                print("   - Selecionando Área: Mineração...")
                page.locator("#mat-select-value-3").click()
                page.wait_for_timeout(500)
                page.locator("[id=\"Mineração-option\"]").get_by_text("Mineração").click()
                page.wait_for_timeout(1000)
                
                # Selecionar Site - FEIT-BFC
                print("   - Selecionando Site:  FEIT-BFC - Benef. Conceição I...")
                # Apenas para limpar o input de perfil - isso caso o site de Conceição I já esteja selecionado
                page.get_by_label("Site").click()
                page.locator("[id=\"45-option\"]").get_by_text("FEIT-BFC - Benef.  Cauê").click()
                page.wait_for_timeout(500)
                
                page.wait_for_timeout(1000)

                # Seleção Real do Site
                page.get_by_label("Site").click()
                page.wait_for_timeout(500)
                page.locator("[id=\"55-option\"]").get_by_text("FEIT-BFO - Benef. Conceição I").click()
                page.wait_for_timeout(1000)
                
                # Selecionar Perfil - Analista
                print("   - Selecionando Perfil: Analista...")
                page.get_by_label("Perfil").click()
                page.wait_for_timeout(500)
                page.locator("[id=\"[object Object]-option\"]").get_by_text("Analista").click()
                page.wait_for_timeout(1500)
                
            except Exception as e:
                print(f"   ✗ Erro ao preencher configuração: {e}")
        else:
            print("   ✗ Não foi possível abrir o diálogo de configuração")
            print("   ⚠ O script pode não funcionar corretamente")
        
        # Aguardar página principal carregar
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Passo 4: Selecionar todos os locais
        print("4. Selecionando todos os locais...")
        try:
            page.get_by_label("", exact=True).check()
            page.wait_for_timeout(1000)
            print("✓ Locais selecionados")
        except Exception as e:
            print(f"   ⚠ Erro ao selecionar locais: {e}")
        
        #Passo 5: Limpar seleção de responsáveis
        print("5. Limpando responsáveis...")
        try:
            page.locator("[id=\"'inputMultiSelectOpenOpcoes\"]").click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"'idBotaoLimparSelecionado'\"]").click()
            page.wait_for_timeout(1000)
            print("   - Fechando dropdown...")
            try:
                if page.locator("#cdk-overlay-0").is_visible():
                    # Clicar em uma posição fixa no canto superior esquerdo
                    page.mouse.click(50, 50)
                    page.wait_for_timeout(500)
                    print("   ✓ Dropdown fechado")
            except Exception as e:
                print(f"   ⚠ Erro:  {e}")
            print("✓ Responsáveis limpos")
        except Exception as e:
            print(f"   ⚠ Erro ao limpar responsáveis: {e}")
        
        # Calcular datas
        data_hoje = datetime.today()
        data_inicio = data_hoje - timedelta(days=3)
        
        # Passo 6: Selecionar data inicial
        print(f"6. Selecionando data inicial: {data_inicio.strftime('%d/%m/%Y')}...")
        try:
            page.locator("#selectPeriodoInicio--toggle").get_by_role("button", name="Open calendar").click()
            page.wait_for_timeout(1000)
            
            # Clicar no dia específico (ajuste conforme necessário)
            dia_inicio = data_inicio.day
            page.get_by_role("button", name=f"{dia_inicio}/", exact=False).first.click()
            page.wait_for_timeout(1000)
            print(f"✓ Data inicial selecionada: {data_inicio.strftime('%d/%m/%Y')}")
        except Exception as e:
            print(f"   ⚠ Erro ao selecionar data inicial:  {e}")
            # Fallback:  preencher manualmente
            try:
                page.locator("#selectPeriodoInicio").fill(data_inicio.strftime("%d/%m/%Y"))
                page.keyboard.press("Enter")
                page.wait_for_timeout(1000)
            except: 
                print("   ⚠ Não foi possível definir data inicial")
        
        # Passo 7: Selecionar data final
        print(f"7. Selecionando data final: {data_hoje.strftime('%d/%m/%Y')}...")
        try:
            page.locator("#codigo-1").click()
            page.wait_for_timeout(500)
            
            # Clicar no dia atual
            dia_hoje = data_hoje.day
            page.get_by_role("button", name=f"{dia_hoje}/", exact=False).first.click()
            page.wait_for_timeout(1000)
            print(f"✓ Data final selecionada:  {data_hoje.strftime('%d/%m/%Y')}")
        except Exception as e:
            print(f"   ⚠ Erro ao selecionar data final: {e}")
            # Fallback: preencher manualmente
            try:
                page.locator("#codigo-1").fill(data_hoje.strftime("%d/%m/%Y"))
                page.keyboard.press("Enter")
                page.wait_for_timeout(1000)
            except:
                print("   ⚠ Não foi possível definir data final")
        
        # Passo 8: Desmarcar "Apenas Pendente"
        print("8. Desmarcando 'Apenas Pendente'...")
        try:
            checkbox_pendente = page.get_by_role("checkbox", name="Apenas Pendente")
            if checkbox_pendente.is_checked():
                checkbox_pendente. uncheck()
            page.wait_for_timeout(1000)
            print("✓ 'Apenas Pendente' desmarcado")
        except Exception as e:
            print(f"   ⚠ Erro ao desmarcar pendente: {e}")
        
        # Passo 9: Pesquisar
        print("9. Realizando pesquisa...")
        try:
            page.get_by_role("button", name="Pesquisar").click()
            page.wait_for_timeout(5000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(6000)
            print("✓ Pesquisa realizada com sucesso")
        except Exception as e:
            print(f"   ✗ Erro ao pesquisar: {e}")
            context.close()
            return
        
        # Passo 10: Exportar dados
        print("10. Exportando dados...")
        try:
            with page.expect_download(timeout=30000) as download_info:
                page.get_by_role("button", name="Exportar Dados").click()
            
            download = download_info.value
            
            # Salvar arquivo
            caminho_destino = "C:/Users/81057638/OneDrive - Vale S.A/PREDITIVA COMPLEXO ITABIRA - CMA 2.0/ITABIRA_CONCEICAO1.xlsx"
            download.save_as(caminho_destino)
            
            print(f"✓ Download concluído!")
            print(f"✓ Arquivo salvo em:  {caminho_destino}")
        except Exception as e:
            print(f"   ✗ Erro ao exportar dados: {e}")
        
        # Finalizar
        page.wait_for_timeout(3000)
        context.close()
        
        print("\n" + "="*70)
        print("PROCESSO FINALIZADO COM SUCESSO!")
        print("="*70)

if __name__ == "__main__":
    run()