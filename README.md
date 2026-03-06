# 🛡️ EPI Scan - Back-End

API back-end do **EPI Scan**, um sistema de detecção de Equipamentos de Proteção Individual (EPIs) em imagens utilizando inteligência artificial (YOLO).

---

## 🚀 Tecnologias

- **Python** 3.11
- **FastAPI** — Framework web assíncrono
- **Uvicorn** — Servidor ASGI
- **SQLAlchemy** — ORM para banco de dados
- **Alembic** — Migrações de banco de dados
- **PostgreSQL** — Banco de dados relacional
- **Ultralytics (YOLOv8)** — Modelo de detecção de objetos (IA)
- **Boto3** — Integração com AWS S3 (armazenamento de imagens)
- **Python-Jose** — Autenticação JWT
- **Bcrypt** — Hash de senhas

---

## 📋 Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- Conta AWS com bucket S3 configurado (para upload de imagens)

---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/EnzoDPrado/epi-scan-back-end.git
cd epi-scan-back-end
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### ATENÇÃO INSTALE A VERSÃO CORRETA DO PYTHORCH PARA A SUA PLACA DE VIDEO MANUALMENTE

```bash
 pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com as suas configurações:

```env
# DATABASE
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=seu_host
DB_PORT=5432
DB_NAME=seu_banco

# AUTH
SECRET_KEY=sua_chave_secreta
ALGORITH=HS256

# YOLO
YOLO_MODEL_PATH=yolov8n.pt

# IMAGE MAX
IMAGE_MAX_WIDTH=4000
IMAGE_MAX_HEIGHT=4000

# IMAGE MIN
IMAGE_MIN_WIDTH=400
IMAGE_MIN_HEIGHT=400

# AWS S3
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_REGION=us-east-2
AWS_S3_BUCKET_NAME=seu_bucket
```

### 5. Execute as migrações do banco de dados

```bash
alembic upgrade head
```

---

## ▶️ Como rodar o projeto

```bash
uvicorn app.infrastructure.api.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

A documentação interativa (Swagger) estará em: **http://localhost:8000/docs**

