import sys
import time
import msvcrt
from datetime import datetime

from config import Config
from utils.logger import Logger
from utils.files import FileManager
from utils.resumo import ResumoDados, StatusExecucao
from extractions.caue import ExtractionCaue
from extractions.conceicao1 import ExtractionConceicao1
from extractions.conceicao2 import ExtractionConceicao2
from extractions.mina import ExtractionMina

logger = Logger.get()

def input_com_timeout(prompt: str, timeout: int = 15, default: str = "n") -> str:
    """
    Lê uma linha do usuário esperando até `timeout` segundos (Windows).
    Se não houver digitação nesse tempo, retorna `default`.
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    
    inicio = time.time()
    buffer = ""
    
    while True:
        if time.time() - inicio >= timeout:
            sys.stdout.write("\n")
            sys.stdout.flush()
            return default
        
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                return buffer.strip() if buffer.strip() else default
            
            if ch == "\b":
                if buffer:
                    buffer = buffer[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            
            if ch == "\x00" or ch == "\xe0":
                _ = msvcrt.getwch()
                continue
            
            buffer += ch
            sys.stdout.write(ch)
            sys.stdout.flush()
        
        time.sleep(0.05)


def esperar_enter_ou_timeout(mensagem: str, timeout_segundos: int = 120) -> None:
    """
    Mantém o console aberto por até `timeout_segundos`, mas permite fechar antes ao pressionar ENTER.
    """
    sys.stdout.write(mensagem)
    sys.stdout.flush()
    
    inicio = time.time()
    while True:
        if time.time() - inicio >= timeout_segundos:
            logger.info("\n⏱️ Tempo esgotado. Fechando automaticamente...")
            return
        
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                return
        
        time.sleep(0.05)


def main():
    try:
        # Validar configurações
        Config.validate()
        logger.info("✓ Configurações carregadas com sucesso\n")
    except ValueError as e:
        logger.error(f"❌ Erro de configuração: {e}")
        erro_msg = f"Erro de configuração: {str(e)[:100]}"
        ResumoDados.adicionar_resultado(StatusExecucao.FALHA_TOTAL, erro_msg)
        Logger.save_to_sharepoint()
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 1 minuto para fechar automaticamente)...",
            timeout_segundos=60,
        )
        return 1
    
    logger.info("=" * 70)
    logger.info("EXTRAÇÃO CMA WEB - EXECUÇÃO SEQUENCIAL")
    logger.info("=" * 70)
    logger.info(f"Início da execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 70)
    
    # Preparação: liberar espaço dos arquivos
    logger.info("\n📁 Liberando espaço em OneDrive...")
    target_files = FileManager.get_target_files()
    FileManager.free_space(target_files)
    
    # Lista de extrações a executar (nome, classe)
    extractions_list = [
        ("Cauê", ExtractionCaue()),
        ("Conceição I", ExtractionConceicao1()),
        ("Conceição II", ExtractionConceicao2()),
        ("Mina Itabira", ExtractionMina()),
    ]
    
    resultados = {}
    excecoes_encontradas = []
    inicio_total = datetime.now()
    total_extractions = len(extractions_list)
    sucessos = 0
    
    # Executar cada extração sequencialmente
    for nome_extracao, extraction in extractions_list:
        try:
            sucesso = extraction.run()
            resultados[nome_extracao] = sucesso
            
            if sucesso:
                sucessos += 1
                logger.info(f"✓ {nome_extracao} concluída com sucesso")
            else:
                logger.error(f"✗ {nome_extracao} falhou")
            
            # Se uma extração falhar, perguntar se deseja continuar
            if not sucesso:
                logger.warning("\n" + "⚠" * 35)
                
                resposta = input_com_timeout(
                    f"\n{nome_extracao} falhou. Deseja continuar com as próximas? (s/n) [auto: s em 15s]: ",
                    timeout=15,
                    default="s",
                ).strip().lower()
                
                if resposta == "s":
                    logger.info(f"➡️ Continuando com próximas extrações...")
                else:
                    logger.error("\n❌ Execução interrompida pelo usuário.")
                    break
        
        except TimeoutError as e:
            logger.warning(f"⚠ Timeout na extração {nome_extracao}: {e}")
            resultados[nome_extracao] = True  # Considerar como sucesso com exceção
            excecoes_encontradas.append(f"Timeout em {nome_extracao}")
            sucessos += 1
            logger.info(f"➡️ Continuando com próximas extrações...")
        
        except Exception as e:
            logger.error(f"❌ Erro ao executar extração {nome_extracao}: {e}")
            resultados[nome_extracao] = False
            
            # Extrair módulo/função do erro
            error_type = type(e).__name__
            excecoes_encontradas.append(f"{error_type} em {nome_extracao}")
            
            logger.info(f"➡️ Continuando com próximas extrações...")
    
    # Resumo final
    fim_total = datetime.now()
    duracao = fim_total - inicio_total
    
    logger.info("\n" + "=" * 70)
    logger.info("RESUMO DA EXECUÇÃO")
    logger.info("=" * 70)
    
    for nome_extracao, sucesso in resultados.items():
        status = "✅ Sucesso" if sucesso else "❌ Falhou"
        logger.info(f"{status} - {nome_extracao}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"Início:   {inicio_total.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Término:  {fim_total.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Duração:  {duracao}")
    logger.info(f"Sucessos: {sucessos}/{total_extractions}")
    logger.info("=" * 70)
    
    # Determinar status final
    todos_sucesso = all(resultados.values()) if resultados else False
    
    if todos_sucesso and not excecoes_encontradas:
        status_final = StatusExecucao.SUCESSO
        observacao = "Todas as extrações concluídas com sucesso"
        logger.info("\n🎉 Todas as extrações foram concluídas com sucesso!")
    elif todos_sucesso and excecoes_encontradas:
        status_final = StatusExecucao.SUCESSO_COM_EXCECAO
        observacao = "; ".join(excecoes_encontradas[:3])  # Máximo 3 exceções
        logger.warning("\n⚠️ Extrações concluídas com algumas exceções (timeouts, etc).")
    elif sucessos > 0 and sucessos < total_extractions:
        status_final = StatusExecucao.FALHA_PARCIAL
        falhas = [nome for nome, sucesso in resultados.items() if not sucesso]
        observacao = f"Falhas em: {', '.join(falhas[:2])}"
        logger.warning("\n⚠️ Algumas extrações falharam, mas outras foram concluídas.")
    else:
        status_final = StatusExecucao.FALHA_TOTAL
        observacao = "Todas as extrações falharam"
        logger.error("\n❌ Todas as extrações falharam!")
    
    # Adicionar resumo final ao arquivo
    logger.info(f"\n📊 Status Final: {status_final}")
    logger.info(f"📝 Observação: {observacao}\n")
    ResumoDados.adicionar_resultado(status_final, observacao)
    
    # Salvar log no SharePoint
    if Config.SAVE_LOG_SHAREPOINT:
        logger.info("📁 Salvando logs no SharePoint...")
        Logger.save_to_sharepoint()
    
    # Determinar código de saída e tempo de espera
    if status_final == StatusExecucao.SUCESSO:
        logger.info("✅ Fechando em 5 segundos...")
        time.sleep(5)
        return 0
    elif status_final == StatusExecucao.SUCESSO_COM_EXCECAO:
        logger.info("✅ Fechando em 5 segundos...")
        time.sleep(5)
        return 0
    else:
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 1 minuto para fechar automaticamente)...",
            timeout_segundos=60,
        )
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.error("\n\n❌ Execução cancelada pelo usuário (Ctrl+C)")
        ResumoDados.adicionar_resultado(
            StatusExecucao.FALHA_TOTAL, 
            "Cancelado pelo usuário (Ctrl+C)"
        )
        Logger.save_to_sharepoint()
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 1 minuto para fechar automaticamente)...",
            timeout_segundos=60,
        )
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        
        # Extrair tipo do erro
        error_type = type(e).__name__
        ResumoDados.adicionar_resultado(
            StatusExecucao.FALHA_TOTAL, 
            f"{error_type}: {str(e)[:80]}"
        )
        Logger.save_to_sharepoint()
        
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 1 minuto para fechar automaticamente)...",
            timeout_segundos=60,
        )
        sys.exit(1)