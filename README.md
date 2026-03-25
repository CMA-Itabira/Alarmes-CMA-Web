# Extrator de Base de Alarmes - CMA Web

Sistema automatizado de extração de dados de alarmes do CMA Web. Executa extrações sequenciais para múltiplos sites (Cauê, Conceição I, Conceição II e Mina Itabira), com logging centralizado, resumo de execução e sincronização com SharePoint.

## Funcionalidades

- Automação Web com Playwright para navegação na interface CMA Web
- Extração de dados para 4 sites diferentes de forma sequencial
- Autenticação persistente via perfil de usuário do Microsoft Edge
- Limpeza automática de cópias locais do OneDrive
- Configuração automática de filtros (área, site, perfil, período)
- Download e salvamento de relatórios Excel (.xlsx)
- Sistema de logging centralizado com sincronização SharePoint
- Histórico de execução em formato CSV
- Tratamento de erros com opção de continuar execução
- Estrutura modular e fácil de manter

## Pré-requisitos

- Python 3.8+
- Microsoft Edge instalado no sistema
- Acesso ao CMA Web com credenciais válidas
- pip (gerenciador de pacotes Python)

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
```bash
copy .env.example .env
```

3. Edite o arquivo `.env` com seus dados:
```
EDGE_EXECUTABLE_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
EDGE_PROFILE_PATH=C:\Users\seu-usuario\AppData\Local\Microsoft\Edge\User Data\Profile 1
BASE_SHAREPOINT_PATH=C:/Users/seu-usuario/Vale S.A/PREDITIVA COMPLEXO ITABIRA - Alarmes_Senseup/CMA 2.0
SHAREPOINT_LOG_PATH=C:/Users/seu-usuario/.../CMA 2.0/Historico
RESUMO_EXECUCAO_PATH=C:/Users/seu-usuario/.../CMA 2.0/Resumo_Execucao.csv
SAVE_LOG_SHAREPOINT=true
```

## Estrutura do Projeto

```
Alarmes-CMA-Web/
├── .env                          # Configurações (não commitar)
├── .env.example                  # Template de referência
├── .gitignore
├── README.md
├── requirements.txt
├── config.py                     # Gerenciador de configurações
├── ExtracaoDados.py             # Script principal
├── utils/
│   ├── __init__.py
│   ├── logger.py                # Sistema de logging
│   ├── resumo.py                # Gerenciador de resumo CSV
│   ├── browser.py               # Gerenciador de navegador
│   ├── automation.py            # Lógica de automação
│   └── files.py                 # Manipulação de arquivos
├── extractions/
│   ├── __init__.py
│   ├── base.py                  # Classe base para extrações
│   ├── caue.py                  # Extração Cauê
│   ├── conceicao1.py            # Extração Conceição I
│   ├── conceicao2.py            # Extração Conceição II
│   └── mina.py                  # Extração Mina Itabira
└── logs/                        # Logs locais (criado automaticamente)
```

## Como Usar

Execute o script principal:
```bash
python ExtracaoDados.py
```

O script irá:
1. Validar configurações do `.env`
2. Liberar espaço em arquivos OneDrive
3. Executar extrações sequencialmente para cada site
4. Ao encontrar falha, perguntar se deseja continuar (padrão: sim)
5. Salvar logs localmente e no SharePoint
6. Atualizar arquivo de resumo com status da execução

## Saídas Geradas

- `logs/extracaodados_YYYYMMDD_HHMMSS.log` - Arquivo de log local
- `Historico/extracaodados_YYYYMMDD_HHMMSS.log` - Cópia no SharePoint
- `Resumo_Execucao.csv` - Histórico de execuções com status
- `ITABIRA_CAUE.xlsx` - Arquivo de dados Cauê
- `ITABIRA_CONCEICAO1.xlsx` - Arquivo de dados Conceição I
- `ITABIRA_CONCEICAO2.xlsx` - Arquivo de dados Conceição II
- `ITABIRA_MINA.xlsx` - Arquivo de dados Mina Itabira

## Variáveis de Configuração (.env)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| EDGE_EXECUTABLE_PATH | Caminho do executável Edge | - |
| EDGE_PROFILE_PATH | Perfil autenticado do Edge | - |
| CMA_WEB_URL | URL do CMA Web | https://prd.webapp.cmaweb.valenet.valeglobal.net/analises/pontos-alarmados |
| BASE_SHAREPOINT_PATH | Caminho base SharePoint | - |
| SHAREPOINT_LOG_PATH | Diretório logs SharePoint | - |
| RESUMO_EXECUCAO_PATH | Caminho do CSV de resumo | - |
| EXTRACTION_AREA | Área de extração | Mineração |
| EXTRACTION_PROFILE | Perfil de acesso | Normativo |
| DAYS_BACK | Dias para trás na busca | 3 |
| SAVE_LOG_SHAREPOINT | Salvar logs no SharePoint | true |
| HEADLESS_MODE | Executar sem interface | true |
| DISABLE_CACHE | Limpar cache navegador | true |
| LOG_LEVEL | Nível de log | INFO |

## Status de Execução

O arquivo `Resumo_Execucao.csv` registra o status de cada execução:

- **Sucesso**: Todas as extrações concluídas sem erros
- **Sucesso com Exceção**: Extrações concluídas mas com timeouts ou erros recuperáveis
- **Falha Parcial**: Algumas extrações falharam, outras tiveram sucesso
- **Falha Total**: Todas as extrações falharam

## Autenticação

O script utiliza o perfil existente do Microsoft Edge. Certifique-se de estar logado no CMA Web manualmente antes de executar pela primeira vez.

## Troubleshooting

**"Erro de configuração"**
- Verifique se o arquivo `.env` existe com todas as variáveis obrigatórias

**"Script não encontrado"**
- Atualize `SCRIPTS_DIRECTORY` no `.env` com o caminho correto

**"Timeout ao aguardar autenticação"**
- Verifique conexão com internet e se está logado no CMA Web

**"Erro ao salvar no SharePoint"**
- Verifique permissões de escrita no caminho especificado

## Desenvolvimento

Para adicionar um novo site:

1. Crie arquivo em `extractions/novo_site.py` herdando de `ExtractionBase`
2. Implemente o construtor com nome do site e caminho de saída
3. Importe e adicione à lista de extrações em `ExtracaoDados.py`