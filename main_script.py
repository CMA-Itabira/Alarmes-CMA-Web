import subprocess
import sys
import os
from datetime import datetime
import time

def executar_script(caminho_completo_script, nome_script):
    """
    Executa um script Python e retorna True se bem-sucedido
    """
    print("\n" + "="*70)
    print(f"INICIANDO:   {nome_script}")
    print("="*70)
    print(f"Horário de início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    try:
        # Executar o script sem capturar output (deixa exibir diretamente)
        resultado = subprocess.run(
            [sys.executable, caminho_completo_script],
            encoding='utf-8',
            errors='ignore'
        )
        
        # Verificar se houve erro
        if resultado.returncode == 0:
            print(f"\n✅ {nome_script} concluído com sucesso!")
            print(f"Horário de término: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            return True
        else:  
            print(f"\n❌ {nome_script} falhou com código de erro: {resultado.returncode}")
            return False
            
    except Exception as e:  
        print(f"\n❌ Erro ao executar {nome_script}: {e}")
        return False

def main():
    print("="*70)
    print("EXTRAÇÃO CMA WEB - EXECUÇÃO SEQUENCIAL")
    print("="*70)
    print(f"Início da execução: {datetime. now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70)
    
    # *** DEFINA O CAMINHO DOS SCRIPTS AQUI ***
    caminho_scripts = r"C:\Dev\Alarmes-CMA-Web"
    # OU use o diretório atual: 
    # caminho_scripts = os.getcwd()
    
    print(f"Diretório dos scripts: {caminho_scripts}\n")
    
    # Lista de scripts a executar na ordem
    scripts = [
        "ExtracaoDados_CA.py",
        "ExtracaoDados_CE_I.py",
        "ExtracaoDados_CE_II.py"
    ]
    
    # Verificar se os arquivos existem
    print("Verificando arquivos...")
    scripts_completos = []
    for script in scripts:
        caminho_completo = os.path.join(caminho_scripts, script)
        if os.path.exists(caminho_completo):
            print(f"✅ {script} encontrado")
            scripts_completos.append((caminho_completo, script))
        else:
            print(f"❌ {script} NÃO encontrado em:  {caminho_completo}")
            input("\nPressione ENTER para fechar...")
            return 1
    
    resultados = {}
    inicio_total = datetime. now()
    
    # Executar cada script sequencialmente
    for caminho_completo, nome_script in scripts_completos: 
        sucesso = executar_script(caminho_completo, nome_script)
        resultados[nome_script] = sucesso
        
        # Se um script falhar, perguntar se deseja continuar
        if not sucesso:
            print("\n" + "⚠"*35)
            resposta = input(f"\n{nome_script} falhou.  Deseja continuar com os próximos?   (s/n): ").strip().lower()
            if resposta != 's':
                print("\n❌ Execução interrompida pelo usuário.")
                break
    
    # Resumo final
    fim_total = datetime.now()
    duracao = fim_total - inicio_total
    
    print("\n" + "="*70)
    print("RESUMO DA EXECUÇÃO")
    print("="*70)
    
    for script, sucesso in resultados.items():
        status = "✅ Sucesso" if sucesso else "❌ Falhou"
        print(f"{status} - {script}")
    
    print("\n" + "="*70)
    print(f"Início:   {inicio_total. strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Término:  {fim_total.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Duração:  {duracao}")
    print("="*70)
    
    # Verificar se todos foram bem-sucedidos
    todos_sucesso = all(resultados.values())
    
    if todos_sucesso:
        print("\n🎉 Todas as extrações foram concluídas com sucesso!")
        print("\nFechando em 5 segundos...")
        time.sleep(5)
        return 0
    else:
        print("\n⚠️ Algumas extrações falharam.  Verifique os logs acima.")
        input("\nPressione ENTER para fechar...")
        return 1

if __name__ == "__main__":  
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:  
        print("\n\n❌ Execução cancelada pelo usuário (Ctrl+C)")
        input("\nPressione ENTER para fechar...")
        sys.exit(1)
    except Exception as e:  
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para fechar...")
        sys.exit(1)