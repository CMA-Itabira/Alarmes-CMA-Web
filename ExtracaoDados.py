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
    Le uma linha do usuario esperando ate `timeout` segundos (Windows).
    Se nao houver digitacao nesse tempo, retorna `default`.
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
    Mantem o console aberto por ate `timeout_segundos`, mas permite fechar antes ao pressionar ENTER.
    """
    sys.stdout.write(mensagem)
    sys.stdout.flush()
    
    inicio = time.time()
    while True:
        if time.time() - inicio >= timeout_segundos:
            logger.info("\nTempo esgotado. Fechando automaticamente...")
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
        # Validar configuracoes
        Config.validate()
        logger.info("Configuracoes carregadas com sucesso\n")
    except ValueError as e:
        logger.error(f"Erro de configuracao: {e}")
        erro_msg = f"Erro de configuracao: {str(e)[:100]}"
        ResumoDados.adicionar_resultado(StatusExecucao.FALHA_TOTAL, erro_msg)
        Logger.save_to_sharepoint()
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 1 minuto para fechar automaticamente)...",
            timeout_segundos=60,
        )
        return 1
    
    logger.info("=" * 70)
    logger.info("EXTRACAO CMA WEB - EXECUCAO SEQUENCIAL")
    logger.info("=" * 70)
    logger.info(f"Inicio da execucao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 70)
    
    # Preparacao: liberar espaco da pasta inteira
    logger.info("\nLiberando espaco em OneDrive...")
    folder_path = Config.BASE_SHAREPOINT_PATH
    FileManager.free_space_folder(folder_path)
    
    # Lista de extracoes a executar (nome, classe)
    extractions_list = [
        ("Caue", ExtractionCaue()),
        ("Conceicao I", ExtractionConceicao1()),
        ("Conceicao II", ExtractionConceicao2()),
        ("Mina Itabira", ExtractionMina()),
    ]
    
    resultados = {}
    excecoes_encontradas = []
    inicio_total = datetime.now()
    total_extractions = len(extractions_list)
    sucessos = 0
    
    # Executar cada extracao sequencialmente
    for nome_extracao, extraction in extractions_list:
        try:
            sucesso = extraction.run()
            resultados[nome_extracao] = sucesso
            
            if sucesso:
                sucessos += 1
                logger.info(f"OK - {nome_extracao} concluida com sucesso")
            else:
                logger.error(f"ERRO - {nome_extracao} falhou")
            
            # Se uma extracao falhar, perguntar se deseja continuar
            if not sucesso:
                logger.warning("\n" + "!" * 35)
                
                resposta = input_com_timeout(
                    f"\n{nome_extracao} falhou. Deseja continuar com as proximas? (s/n) [auto: s em 15s]: ",
                    timeout=15,
                    default="s",
                ).strip().lower()
                
                if resposta == "s":
                    logger.info(f"Continuando com proximas extracoes...")
                else:
                    logger.error("\nExecucao interrompida pelo usuario.")
                    break
        
        except TimeoutError as e:
            logger.warning(f"Timeout na extracao {nome_extracao}: {e}")
            resultados[nome_extracao] = True
            excecoes_encontradas.append(f"Timeout em {nome_extracao}")
            sucessos += 1
            logger.info(f"Continuando com proximas extracoes...")
        
        except Exception as e:
            logger.error(f"Erro ao executar extracao {nome_extracao}: {e}")
            resultados[nome_extracao] = False
            
            # Extrair modulo/funcao do erro
            error_type = type(e).__name__
            excecoes_encontradas.append(f"{error_type} em {nome_extracao}")
            
            logger.info(f"Continuando com proximas extracoes...")
    
    # Resumo final
    fim_total = datetime.now()
    duracao = fim_total - inicio_total
    
    logger.info("\n" + "=" * 70)
    logger.info("RESUMO DA EXECUCAO")
    logger.info("=" * 70)
    
    for nome_extracao, sucesso in resultados.items():
        status = "OK" if sucesso else "ERRO"
        logger.info(f"{status} - {nome_extracao}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"Inicio:   {inicio_total.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Termino:  {fim_total.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Duracao:  {duracao}")
    logger.info(f"Sucessos: {sucessos}/{total_extractions}")
    logger.info("=" * 70)
    
    # Determinar status final
    todos_sucesso = all(resultados.values()) if resultados else False
    
    if todos_sucesso and not excecoes_encontradas:
        status_final = StatusExecucao.SUCESSO
        observacao = "Todas as extracoes concluidas com sucesso"
        logger.info("\nTodas as extracoes foram concluidas com sucesso!")
    elif todos_sucesso and excecoes_encontradas:
        status_final = StatusExecucao.SUCESSO_COM_EXCECAO
        observacao = "; ".join(excecoes_encontradas[:3])
        logger.warning("\nExtracoes concluidas com algumas excecoes (timeouts, etc).")
    elif sucessos > 0 and sucessos < total_extractions:
        status_final = StatusExecucao.FALHA_PARCIAL
        falhas = [nome for nome, sucesso in resultados.items() if not sucesso]
        observacao = f"Falhas em: {', '.join(falhas[:2])}"
        logger.warning("\nAlgumas extracoes falharam, mas outras foram concluidas.")
    else:
        status_final = StatusExecucao.FALHA_TOTAL
        observacao = "Todas as extracoes falharam"
        logger.error("\nTodas as extracoes falharam!")
    
    # Adicionar resumo final ao arquivo
    logger.info(f"\nStatus Final: {status_final}")
    logger.info(f"Observacao: {observacao}\n")
    ResumoDados.adicionar_resultado(status_final, observacao)
    
    # Salvar log no SharePoint
    if Config.SAVE_LOG_SHAREPOINT:
        logger.info("Salvando logs no SharePoint...")
        Logger.save_to_sharepoint()
    
    # Determinar codigo de saida e tempo de espera
    if status_final == StatusExecucao.SUCESSO:
        logger.info("Fechando em 5 segundos...")
        time.sleep(5)
        return 0
    elif status_final == StatusExecucao.SUCESSO_COM_EXCECAO:
        logger.info("Fechando em 5 segundos...")
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
        logger.error("\n\nExecucao cancelada pelo usuario (Ctrl+C)")
        ResumoDados.adicionar_resultado(
            StatusExecucao.FALHA_TOTAL, 
            "Cancelado pelo usuario (Ctrl+C)"
        )
        Logger.save_to_sharepoint()
        esperar_enter_ou_timeout(
            "\nPressione ENTER para fechar (ou aguarde 1 minuto para fechar automaticamente)...",
            timeout_segundos=60,
        )
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\nErro inesperado: {e}")
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