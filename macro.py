from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    caminho_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    caminho_perfil = r"C:\Users\81057638\AppData\Local\Microsoft\Edge\User Data\Default"
    
    print("="*70)
    print("GRAVADOR AUTOMÁTICO DE AÇÕES - CMA WEB")
    print("="*70)
    print(f"Edge: {caminho_edge}")
    print(f"Perfil: {caminho_perfil}")
    print("\n⚠️  IMPORTANTE:  Feche todas as janelas do Edge antes de continuar!")
    input("Pressione ENTER para continuar...")
    
    # Iniciar com inspector habilitado
    context = p. chromium.launch_persistent_context(
        user_data_dir=caminho_perfil,
        executable_path=caminho_edge,
        headless=False,
        args=['--start-maximized']
    )
    
    pagina = context.new_page()
    
    print("\n" + "="*70)
    print("INSTRUÇÕES:")
    print("="*70)
    print("1. Uma janela do Playwright Inspector vai abrir")
    print("2. Clique no botão 'Record' (círculo vermelho)")
    print("3. Faça suas ações normalmente no navegador")
    print("4. O código será gerado automaticamente")
    print("5. Quando terminar, clique em 'Stop' no Inspector")
    print("="*70)
    input("\nPressione ENTER para iniciar a gravação...")
    
    # Pausar e abrir o inspector
    pagina.pause()
    
    # Navegar para a página
    pagina.goto("https://prd.webapp.cmaweb.valenet.valeglobal.net/analises/pontos-alarmados")
    
    context.close()