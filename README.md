# Extrator de Base de Alarmes - CMA Web

Este script automatiza o processo de extração da base de dados de alarmes do sistema CMA Web. Ele utiliza a biblioteca Playwright para navegar pela interface web, preencher os filtros necessários e realizar o download de um arquivo Excel (`.xlsx`) com os dados.

## Funcionalidades

- Abre o navegador Microsoft Edge utilizando um perfil de usuário já autenticado.
- Navega automaticamente até a seção "Análise de pontos alarmados" do CMA Web.
- Seleciona todos os sites e áreas para a consulta.
- Define um período de consulta para os últimos 2 dias.
- Realiza a pesquisa e faz o download do relatório gerado.
- Salva o arquivo baixado em um caminho pré-definido.

## Pré-requisitos

Antes de executar, você precisa ter instalado:

1.  **Python 3.x**
2.  **Biblioteca Playwright**:
    ```bash
    pip install playwright
    ```
3.  **Navegadores para o Playwright**:
    ```bash
    playwright install
    ```
4.  **Navegador Microsoft Edge** instalado no sistema.

## Configuração

Antes de executar o script pela primeira vez, você **precisa** ajustar as seguintes variáveis no código para que correspondam ao seu ambiente:

1.  `caminho_edge`: O caminho para o executável do Microsoft Edge no seu computador.
    ```python
    # Exemplo:
    caminho_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ```

2.  `caminho_perfil`: A pasta onde o Playwright irá salvar (e de onde irá ler) o seu perfil de usuário autenticado. É importante que você faça login no CMA Web manualmente pelo menos uma vez para que suas credenciais fiquem salvas.
    ```python
    # Exemplo:
    caminho_perfil = r"C:\Users\SEU_USUARIO\playwright_edge_profile"
    ```

3.  `caminho_destino`: O caminho completo, incluindo o nome do arquivo, onde o relatório de alarmes (`.xlsx`) será salvo.
    ```python
    # Exemplo:
    caminho_destino = "C:/Users/SEU_USUARIO/Pasta/arquivo_cma.xlsx"
    ```

## Como Usar

1.  Garanta que todos os [Pré-requisitos](#pré-requisitos) estão instalados e a [Configuração](#configuração) foi realizada.
2.  Execute o script através de um terminal:
    ```bash
    python seu_script.py
    ```
3.  O script abrirá uma janela do navegador e executará todos os passos automaticamente. Ao final, a mensagem "Download concluído e salvo em: [caminho]" será exibida no terminal.

## Observações

-   O script é executado em modo "visível" (`headless=False`), então você verá a janela do navegador abrir e realizar as ações.
-   A automação depende diretamente da estrutura HTML do site CMA Web. Se houverem atualizações na interface do site, os seletores (especialmente os `xpath`) podem precisar de ajuste.
-   A autenticação é persistida através do perfil de usuário. Se sua sessão expirar, pode ser necessário fazer login manualmente no site outra vez para que o script volte a funcionar.