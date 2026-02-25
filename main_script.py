import subprocess
import sys
import os
from datetime import datetime
import time
import msvcrt


def input_com_timeout(prompt: str, timeout: int = 15, default: str = "n") -> str:
    """
    Lê uma linha do usuário esperando até `timeout` segundos (Windows).
    Se não houver digitação nesse tempo, retorna `default`.

    Observação: o usuário precisa finalizar com ENTER para confirmar.
    """
    print(prompt, end="", flush=True)

    inicio = time.time()
    buffer = ""

    while True:
        # Timeout
        if time.time() - inicio >= timeout:
            print()  # quebra linha após o prompt
            return default

        # Há tecla pressionada?
        if msvcrt.kbhit():
            ch = msvcrt.getwch()

            # Enter finaliza
            if ch in ("\r", "\n"):
                print()  # nova linha
                return buffer.strip()

            # Backspace
            if ch == "\b":
                if buffer:
                    buffer = buffer[:-1]
                    # apaga um char na tela
                    print("\b \b", end="", flush=True)
                continue

            # Ignora teclas especiais (setas, F1 etc.)
            if ch == "\x00" or ch == "\xe0":
                _ = msvcrt.getwch()
                continue

            buffer += ch
            print(ch, end="", flush=True)

        time.sleep(0.05)


def esperar_enter_ou_timeout(mensagem: str, timeout_segundos: int = 120) -> None:
    """
    Mantém o console aberto por até `timeout_segundos`, mas permite fechar antes ao pressionar ENTER.
    (Windows via msvcrt)
    """
    print(mensagem, end="", flush=True)

    inicio = time.time()
    while True:
        if time.time() - inicio >= timeout_segundos:
            print("\n⏱️ Tempo esgotado. Fechando automaticamente...")
            return

        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                print()  # quebra linha
                return

            # descarta qualquer outra tecla (pra não "sujar" a tela)
        time.sleep(0.05)


def executar_script(caminho_completo_script, nome_script):
    """
    Executa um script Python e retorna True se bem-sucedido
    """
    print("\n" + "=" * 70)
    print(f"INICIANDO:   {nome_script}")
    print("=" * 70)
    print(f"Horário de início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    try:
        # Executar o script sem capturar output (deixa exibir diretamente)
        resultado = subprocess.run(
            [sys.executable, caminho_completo_script],
            encoding="utf-8",
            errors="ignore",
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
    print("=" * 70)
    print("EXTRAÇÃO CMA WEB - EXECUÇÃO SEQUENCIAL")
    print("=" * 70)
    print(f"Início da execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)

    # *** DEFINA O CAMINHO DOS SCRIPTS AQUI ***
    caminho_scripts = r"C:\Dev\Alarmes-CMA-Web"
    # OU use o diretório atual:
    # caminho_scripts = os.getcwd()

    print(f"Diretório dos scripts: {caminho_scripts}\n")

    # Lista de scripts a executar na ordem
    scripts = [
        "ExtracaoDados_CA.py",
        "ExtracaoDados_CE_I.py",
        "ExtracaoDados_CE_II.py",
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
            esperar_enter_ou_timeout(
                "\nPressione ENTER para fechar (ou aguarde 2 minutos para fechar automaticamente)...",
                timeout_segundos=120,
            )
            return 1

    resultados = {}
    inicio_total = datetime.now()

    # Executar cada script sequencialmente
    for caminho_completo, nome_script in scripts_completos:
        sucesso = executar_script(caminho_completo, nome_script)
        resultados[nome_script] = sucesso

        # Se um script falhar, perguntar se deseja continuar (aguarda 15s, padrão "s")
        if not sucesso:
            print("\n" + "⚠" * 35)

            resposta = input_com_timeout(
                f"\n{nome_script} falhou. Deseja continuar com os próximos? (s/n) [auto: n em 15s]: ",
                timeout=15,
                default="n",
            ).strip().lower()

            # Se o usuário só der ENTER, tratar como "n" também
            if resposta == "":
                resposta = "n"

            if resposta != "s":
                print("\n❌ Execução interrompida pelo usuário.")
                break

    # Resumo final
    fim_total = datetime.now()
    duracao = fim_total - inicio_total

    print("\n" + "=" * 70)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 70)

    for script, sucesso in resultados.items():
        status = "✅ Sucesso" if sucesso else "❌ Falhou"
        print(f"{status} - {script}")

    print("\n" + "=" * 70)
    print(f"Início:   {inicio_total.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Término:  {fim_total.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Duração:  {duracao}")
    print("=" * 70)

    # Verificar se todos foram bem-sucedidos
    todos_sucesso = all(resultados.values()) if resultados else False

    if todos_sucesso:
        print("\n🎉 Todas as extrações foram concluídas com sucesso!")
        print("\nFechando em 5 segundos...")
        time.sleep(5)
        return 0
    else:
        print("\n⚠️ Algumas extrações falharam. Verifique os logs acima.")
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 2 minutos para fechar automaticamente)...",
            timeout_segundos=120,
        )
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Execução cancelada pelo usuário (Ctrl+C)")
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 2 minutos para fechar automaticamente)...",
            timeout_segundos=120,
        )
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback

        traceback.print_exc()
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 2 minutos para fechar automaticamente)...",
            timeout_segundos=120,
        )
        sys.exit(1)