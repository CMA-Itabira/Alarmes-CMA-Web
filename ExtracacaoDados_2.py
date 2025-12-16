from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

with sync_playwright() as p:
    # Caminho para o executável do Microsoft Edge
    caminho_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    # Caminho para o perfil autenticado do Edge
    caminho_perfil = r"C:\Users\81037712\playwright_edge_profile"

    context = p.chromium.launch_persistent_context(
        user_data_dir=caminho_perfil,
        executable_path=caminho_edge,
        headless=False
    )

    pagina = context.new_page()
    
    # Navegação inicial e aguardo da autenticação
    print("Navegando para a página e aguardando autenticação...")
    pagina.goto("https://prd.webapp.cmaweb.valenet.valeglobal.net/analises/pontos-alarmados")
    
    # Aguardar redirecionamento para /analises/pontos-alarmados após autenticação
    print("Aguardando conclusão da autenticação automática...")
    pagina.wait_for_url("**/analises/pontos-alarmados", timeout=60000)
    pagina.wait_for_load_state("networkidle")
    pagina.wait_for_timeout(3000)
    
    # Passo 0: Verificar se o dialog de configuração está visível
    print("Verificando se o diálogo de configuração está visível...")
    dialog_visible = False
    try:
        dialog = pagina.locator('#mat-mdc-dialog-0.mat-mdc-dialog-container. mdc-dialog. cdk-dialog-container.mdc-dialog--open')
        dialog. wait_for(state="visible", timeout=5000)
        dialog_visible = True
        print("Diálogo de configuração detectado.  Iniciando configuração...")
    except:
        print("Diálogo não encontrado ou já foi preenchido anteriormente.")
    
    if dialog_visible:
        # Passo 1: Selecionar Área de Negócio - Mineração
        print("Passo 1: Selecionando Área de Negócio - Mineração...")
        pagina.wait_for_timeout(1000)
        
        # Localizar o mat-select da área (após o elemento <p>Área de Negócio</p>)
        area_select = pagina.locator('#areaInputTest')
        area_select.wait_for(state="visible")
        area_select.click()
        pagina.wait_for_timeout(1000)
        
        # Selecionar a opção Mineração
        opcao_mineracao = pagina. locator('#Mineração-option')
        opcao_mineracao.wait_for(state="visible")
        opcao_mineracao.click()
        pagina.wait_for_timeout(1500)
        
        # Passo 2: Selecionar Site
        print("Passo 2: Selecionando Site...")
        
        # Localizar o mat-select do site
        site_select = pagina. locator('#siteInputTest')
        site_select.wait_for(state="visible")
        site_select.click()
        pagina.wait_for_timeout(1000)
        
        # Selecionar a opção com id 45-option
        opcao_site = pagina.locator('#\\34 5-option')  # Escapando o número inicial com \3 seguido do número
        opcao_site. wait_for(state="visible")
        opcao_site.click()
        pagina.wait_for_timeout(1500)
        
        # Passo 3: Selecionar Perfil - Analista
        print("Passo 3: Selecionando Perfil - Analista...")
        
        # Localizar o mat-select do perfil
        perfil_select = pagina.locator('#perfilInputTest')
        perfil_select.wait_for(state="visible")
        perfil_select.click()
        pagina.wait_for_timeout(1000)
        
        # Selecionar a opção Analista
        opcao_analista = pagina.locator('mat-option: has-text("Analista")')
        opcao_analista. wait_for(state="visible")
        opcao_analista. click()
        pagina.wait_for_timeout(1500)
        
        # Procurar e clicar no botão de confirmação/OK do diálogo
        print("Confirmando seleções...")
        botao_confirmar = pagina. locator('button:has-text("Confirmar"), button:has-text("OK"), button:has-text("Avançar")')
        try:
            botao_confirmar.first.wait_for(state="visible", timeout=3000)
            botao_confirmar.first.click()
            pagina.wait_for_timeout(2000)
        except:
            print("Botão de confirmação não encontrado ou não necessário.")
    
    # Aguardar página carregar completamente após configuração
    pagina.wait_for_load_state("networkidle")
    pagina.wait_for_timeout(2000)
    
    # Início do fluxo principal de extração
    print("\n=== Iniciando fluxo de extração ===\n")
    
    # Passo 2 (original): Selecionar todos os locais
    print("Selecionando todos os locais...")
    try:
        # Aguardar o checkbox estar disponível
        pagina.wait_for_selector('input[id*="checkbox-input"]', state="visible", timeout=10000)
        
        # Tentar localizar o checkbox específico de locais
        checkbox_locais = pagina.locator('input[id*="0100000000000319446-checkbox-input"]').first
        if not checkbox_locais. is_checked():
            checkbox_locais. click()
        pagina.wait_for_timeout(1000)
        print("✓ Locais selecionados")
    except Exception as e: 
        print(f"Aviso: Não foi possível selecionar locais automaticamente. Erro: {e}")

    # Passo 3 (original): Expandir lista de responsáveis
    print("Expandindo lista de responsáveis...")
    try:
        pagina.wait_for_selector('div. mat-mdc-form-field-infix', state="visible")
        # Procurar pela div relacionada aos responsáveis
        form_fields = pagina.locator('div.mat-mdc-form-field-infix')
        # Tentar diferentes índices se necessário
        form_fields.nth(1).click()
        pagina.wait_for_timeout(1000)
        print("✓ Lista de responsáveis expandida")
    except Exception as e:
        print(f"Aviso:  Problema ao expandir responsáveis. Erro: {e}")

    # Passo 4 (original): Selecionar todos os responsáveis
    print("Selecionando todos os responsáveis...")
    try:
        pagina.wait_for_selector('input[id*="idBotaoSelecionarTodos"]', state="visible", timeout=5000)
        checkbox_responsaveis = pagina. locator('input[id*="idBotaoSelecionarTodos-input"]').first
        checkbox_responsaveis.click()
        pagina.wait_for_timeout(1000)
        
        # Fechar dropdown clicando fora
        pagina.click('body')
        pagina.wait_for_timeout(500)
        print("✓ Responsáveis selecionados")
    except Exception as e:
        print(f"Aviso: Não foi possível selecionar responsáveis.  Erro: {e}")

    # Passo 5 (original): Selecionar data inicial (3 dias atrás)
    print("Selecionando data inicial...")
    try:
        data_hoje = datetime.today()
        data_inicio = data_hoje - timedelta(days=3)
        
        # Localizar o datepicker de início
        datepicker_inicio = pagina.locator('app-reusable-datepicker[formcontrolname="periodoInicio"]')
        datepicker_inicio.click()
        pagina.wait_for_timeout(1000)
        
        # Aguardar o calendário aparecer
        pagina.wait_for_selector('#mat-datepicker-0', state="visible", timeout=5000)
        
        # Preencher a data
        input_data_inicio = datepicker_inicio.locator('input')
        input_data_inicio. fill(data_inicio.strftime("%d/%m/%Y"))
        pagina.keyboard.press("Enter")
        pagina.wait_for_timeout(1000)
        print(f"✓ Data inicial selecionada: {data_inicio.strftime('%d/%m/%Y')}")
    except Exception as e:
        print(f"Aviso: Problema ao selecionar data inicial.  Erro: {e}")

    # Passo 6 (original): Selecionar data final (hoje)
    print("Selecionando data final...")
    try:
        datepicker_fim = pagina. locator('app-reusable-datepicker[formcontrolname="periodoFim"]')
        datepicker_fim. click()
        pagina.wait_for_timeout(1000)
        
        # Aguardar o calendário aparecer
        pagina.wait_for_selector('#mat-datepicker-1', state="visible", timeout=5000)
        
        # Preencher a data
        input_data_fim = datepicker_fim.locator('input')
        input_data_fim. fill(data_hoje.strftime("%d/%m/%Y"))
        pagina.keyboard.press("Enter")
        pagina.wait_for_timeout(1000)
        print(f"✓ Data final selecionada: {data_hoje. strftime('%d/%m/%Y')}")
    except Exception as e:
        print(f"Aviso: Problema ao selecionar data final. Erro: {e}")

    # Passo 7 (original): Desmarcar checkbox "apenas pendentes"
    print("Desmarcando opção 'apenas pendentes'...")
    try:
        pagina.wait_for_selector('#mat-mdc-checkbox-1-input', state="visible", timeout=5000)
        checkbox_pendentes = pagina.locator('#mat-mdc-checkbox-1-input')
        if checkbox_pendentes.is_checked():
            checkbox_pendentes. click()
        pagina.wait_for_timeout(1000)
        print("✓ Opção 'apenas pendentes' desmarcada")
    except Exception as e:
        print(f"Aviso: Problema com checkbox pendentes. Erro: {e}")

    # Passo 8 (original): Clicar no botão Pesquisar
    print("Clicando em Pesquisar...")
    try:
        # Localizar o botão através do ícone e texto
        botao_pesquisar = pagina.locator('button:has(mat-icon: text("search")):has(span. text: text("Pesquisar"))')
        botao_pesquisar. wait_for(state="visible", timeout=10000)
        botao_pesquisar.click()
        
        # Aguardar carregamento dos resultados
        print("Aguardando carregamento dos resultados...")
        pagina.wait_for_timeout(5000)
        
        # Aguardar indicador de carregamento desaparecer (se existir)
        pagina.wait_for_load_state("networkidle")
        pagina.wait_for_timeout(3000)
        print("✓ Pesquisa realizada com sucesso")
    except Exception as e:
        print(f"Erro ao realizar pesquisa: {e}")

    # Passo 9 (original): Clicar no botão Exportar Dados
    print("Exportando dados...")
    try:
        botao_exportar = pagina. locator('button:has(mat-icon:text("download")):has(span.text:text("Exportar Dados"))')
        botao_exportar.wait_for(state="visible", timeout=15000)
        
        # Configurar download
        with pagina.expect_download() as download_info:
            botao_exportar.click()

        download = download_info.value
        caminho_destino = "C:/Users/81037712/Vale S. A/PREDITIVA COMPLEXO ITABIRA - Alarmes_Senseup/arquivo_cma.xlsx"
        download.save_as(caminho_destino)

        print(f"✓ Download concluído e salvo em: {caminho_destino}")
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")

    pagina.wait_for_timeout(3000)
    context.close()
    
    print("\n=== Processo finalizado com sucesso! ===")