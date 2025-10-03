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
    pagina.goto("https://scma.valenet.valeglobal.net/cma/")

    # Clicar no CMA WEB
    pagina.wait_for_selector('xpath=//*[@id="CMA WEB"]/div/div[1]/div[2]/img')
    pagina.click('xpath=//*[@id="CMA WEB"]/div/div[1]/div[2]/img')

    # Selecionar área de negócio
    pagina.select_option("#idAreaNegocio", label="Mineração")
    pagina.wait_for_timeout(500)

    # Selecionar site
    pagina.select_option("#idSite", label="FEIT-BFC - Benef. Cauê")
    pagina.wait_for_timeout(500)

    # Clicar no botão OK
    pagina.click("#ok")

    # Navegar até "CMA Local"
    pagina.wait_for_selector('xpath=//*[@id="labelCMA"]/a')
    pagina.click('xpath=//*[@id="labelCMA"]/a')

    # Clicar em "Análise de pontos alarmados"
    pagina.wait_for_selector('xpath=//*[@id="pontosAlarmados"]')
    pagina.click('xpath=//*[@id="pontosAlarmados"]')

    # Abrir dropdown e marcar todos os itens
    pagina.wait_for_selector('xpath=//*[@id="dropdownMenu"]/span[1]')
    pagina.click('xpath=//*[@id="dropdownMenu"]/span[1]')

    pagina.wait_for_selector('xpath=//*[@id="site"]/div/div/div[1]/div[4]/div/a')
    pagina.click('xpath=//*[@id="site"]/div/div/div[1]/div[4]/div/a')
    pagina.wait_for_timeout(500)
    pagina.click('xpath=//*[@id="site"]/div/div/div[1]/div[4]/div/a')

    # Clique fora da área para fechar dropdown
    pagina.click('xpath=/html/body/div/div[5]/div/div/section/div/div/div[1]/div')
    pagina.wait_for_timeout(500)
    # Clicar no dropdownMenu dentro da área
    pagina.wait_for_selector('xpath=//*[@id="area"]//button[@id="dropdownMenu"]', state="visible")
    pagina.locator('xpath=//*[@id="area"]//button[@id="dropdownMenu"]').click(force=True)
    pagina.wait_for_timeout(500)
    # Clicar uma vez no botão "Marcar todos" da área
    pagina.wait_for_selector('xpath=//*[@id="area"]/div/div/div[1]/div[4]/div/a', state="visible")
    pagina.click('xpath=//*[@id="area"]/div/div/div[1]/div[4]/div/a')

    # Clique fora da área para fechar dropdown
    pagina.click('xpath=/html/body/div/div[5]/div/div/section/div/div/div[1]/div')

    # Espera o elemento estar visível
    pagina.wait_for_selector('xpath=//*[@id="vigentes"]', state="visible")

    # Localiza o checkbox
    checkbox = pagina.locator('xpath=//*[@id="vigentes"]')

    # Desmarca o checkbox (se estiver marcado)
    if checkbox.is_checked():
        checkbox.uncheck()

    pagina.wait_for_timeout(500)
    # Preencher datas
    data_fim = datetime.today()
    data_inicio = data_fim - timedelta(days=2)
    data_inicio_formatada = data_inicio.strftime("%d/%m/%Y")
    data_fim_formatada = data_fim.strftime("%d/%m/%Y")

    pagina.fill('xpath=//*[@id="periodoInicio"]', data_inicio_formatada)
    pagina.fill('xpath=//*[@id="periodoFim"]', data_fim_formatada)


    # Esperar botão "Pesquisar" estar habilitado
    botao_pesquisar = pagina.locator('xpath=//*[@id="pesquisar"]')
    botao_pesquisar.wait_for(state="visible")
    if botao_pesquisar.is_enabled():
        botao_pesquisar.click()
    else:
        print("Botão 'Pesquisar' ainda está desabilitado.")

    # Aguarda carregamento
    pagina.wait_for_timeout(5000)

    # Download
    pagina.wait_for_selector('xpath=//*[@id="downloadBtn"]', state="visible")
    with pagina.expect_download() as download_info:
        pagina.locator('xpath=//*[@id="downloadBtn"]').click(force=True)

    download = download_info.value
    caminho_destino = "C:/Users/81037712/Vale S.A/PREDITIVA COMPLEXO ITABIRA - Alarmes_Senseup/arquivo_cma.xlsx"
   # caminho_destino = "C:/Users/81037712/Downloads/arquivo_cma.xlsx"
    download.save_as(caminho_destino)

    print(f"Download concluído e salvo em: {caminho_destino}")

    pagina.wait_for_timeout(3000)
    context.close()
