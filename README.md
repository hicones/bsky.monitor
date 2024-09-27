# BlueSky Monitor

Este projeto monitora perfis no BlueSky e envia notificações via WebSocket sempre que novos posts são encontrados. O sistema usa `SQLite` para registrar os CIDs (Content Identifiers) dos posts já notificados e evitar duplicações de notificações.

## Requisitos

- Python 3.x instalado na máquina.
- Acesso à API pública do BlueSky para coletar posts de perfis.

## Passo a Passo para Configuração

### 1. Clone o Repositório

Se o código estiver em um repositório Git, clone-o:

```bash
git clone https://github.com/hicones/bsky.monitor.git
cd bsky.monitor
```

### 2. Crie um Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python3 -m venv venv
```

### 3. Ative o Ambiente Virtual

Ative o ambiente virtual para começar a trabalhar no projeto.

- No **Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

- No **Windows**:

  ```bash
  venv\Scripts\activate
  ```

### 4. Instale as Dependências

Instale todas as dependências necessárias usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` deve incluir todas as bibliotecas necessárias:

```
python-dotenv==1.0.0
requests==2.28.1
websockets==10.2
```

### 5. Configure o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto e defina os IDs dos perfis que você deseja monitorar no BlueSky. Exemplo de conteúdo do arquivo `.env`:

```bash
PROFILE_IDS=perfil1,perfil2,perfil3
```

Substitua `perfil1`, `perfil2`, e `perfil3` pelos IDs reais dos perfis do BlueSky que você deseja monitorar.

### 6. Execute o Monitor de Perfis

Para iniciar o monitoramento dos perfis, execute o arquivo `monitor.py`:

```bash
python monitor.py
```

O monitor ficará rodando e, a cada 60 segundos, verificará se há novos posts nos perfis configurados. Quando um novo post for detectado, uma notificação será enviada via WebSocket para os clientes conectados.

### 7. Verificar as Notificações (Opcional)

Para verificar as notificações enviadas pelo WebSocket, você pode utilizar um WebSocket client. Abaixo está um exemplo de código para ser executado no console do navegador (JavaScript):

```javascript
let ws = new WebSocket("ws://localhost:6789");

ws.onmessage = function (event) {
  console.log("Nova notificação: " + event.data);
};
```

Esse código irá conectar-se ao servidor WebSocket e exibirá as notificações de novos posts diretamente no console do navegador.

## Estrutura do Projeto

A estrutura de arquivos do projeto deve ser organizada da seguinte maneira:

```
blue_sky_monitor/
│
├── .env                   # Variáveis de ambiente (não versionado)
├── .gitignore              # Arquivos a serem ignorados no versionamento
├── requirements.txt        # Dependências do projeto
├── venv/                   # Ambiente virtual (não versionado)
├── monitor.py              # Código principal do monitoramento
└── README.md               # Instruções para o projeto
```

### Explicação dos Arquivos:

- **`.env`**: Contém as variáveis de ambiente, como os IDs dos perfis que estão sendo monitorados.
- **`.gitignore`**: Arquivo para excluir do versionamento o ambiente virtual e o arquivo `.env`.
- **`requirements.txt`**: Lista de dependências necessárias para o projeto.
- **`venv/`**: Ambiente virtual onde as dependências são instaladas (não deve ser versionado).
- **`monitor.py`**: O script principal que executa o monitoramento dos perfis e notifica via WebSocket.

## Detalhes Técnicos

### 1. Monitoramento de Perfis

O script `monitor.py` faz requisições periódicas para a API do BlueSky, consultando os perfis especificados no arquivo `.env`. Para cada post encontrado, o sistema verifica se o CID (identificador único) já foi registrado no banco de dados SQLite. Se o CID for novo, ele é salvo e uma notificação é enviada.

### 2. Banco de Dados SQLite

O sistema usa o SQLite para registrar apenas os CIDs dos posts que já foram notificados. Dessa forma, evita-se a duplicação de notificações, mesmo que o monitor seja reiniciado.

### 3. WebSocket

O WebSocket server é executado no mesmo script, permitindo que clientes conectem-se ao servidor para receber notificações em tempo real sempre que um novo post for encontrado.

## Recriando o Ambiente em Outras Máquinas

Se alguém precisar recriar o ambiente em outra máquina, basta seguir estes passos:

1. Clone o repositório.
2. Crie e ative o ambiente virtual.
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o arquivo `.env` com os IDs dos perfis.
5. Execute o monitor:
   ```bash
   python monitor.py
   ```
