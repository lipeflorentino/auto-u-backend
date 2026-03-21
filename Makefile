# ==============================================================================
# Projeto: Auto-U Backend
# Desenvolvedor: Filipe F. Lima
# Finalidade: Automação de triagem de e-mails com mDeBERTa-v3 e Llama-3
# ==============================================================================

# Variáveis Globais
IMAGE_NAME=auto-u-backend
DOCKER_COMPOSE=docker-compose
PYTHON=python3
PIP=pip3

# Variáveis de Cloud
GCP_PROJECT_ID ?= auto-u-project
GCP_REGION ?= southamerica-east1
AWS_ACCOUNT_ID ?= 000000000000
AWS_REGION ?= us-east-1

.PHONY: help install-local test-local build-docker run-docker deploy-gcp deploy-aws clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Desenvolvimento Local ---

install-local: ## Instala dependências locais e modelos de NLP
	$(PIP) install -r requirements.txt
	$(PYTHON) -m spacy download pt_core_news_sm

test-local: ## Executa os testes unitários com Pytest
	pytest src/tests -v --cov=src

run-dev: ## Inicia o servidor FastAPI em modo reload
	uvicorn src.interfaces.main:app --reload --port 8000

# --- Docker & Containerização ---

build-docker: ## Build da imagem utilizando Multi-Stage (Otimizado)
	docker build -t $(IMAGE_NAME):latest .

run-docker: ## Executa o container localmente para validação
	docker run -p 8000:8000 --env-file .env $(IMAGE_NAME):latest

# --- Cloud Deployment (Agnóstico) ---

deploy-gcp: build-docker ## Build e Deploy para Google Cloud Run
	@echo "🚀 Iniciando Deploy no Google Cloud Run..."
	docker tag $(IMAGE_NAME):latest $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(repository_id)/$(IMAGE_NAME):latest
	docker push $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(repository_id)/$(IMAGE_NAME):latest
	gcloud run deploy $(service_name) --image $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(repository_id)/$(IMAGE_NAME):latest \
		--platform managed \
		--region $(GCP_REGION) \
		--allow-unauthenticated

deploy-aws: build-docker ## Build e Deploy para AWS App Runner (via ECR)
	@echo "🚀 Iniciando Deploy no AWS App Runner..."
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	docker tag $(IMAGE_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME):latest
	@echo "Aguardando sincronização do App Runner..."

# --- Utilidades ---

clean: ## Remove arquivos temporários e caches do Python
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage

up: ## Sobe todo o ecossistema (API + DB) em background
	$(DOCKER_COMPOSE) up -d

down: ## Para e remove todos os containers do projeto
	$(DOCKER_COMPOSE) down

logs: ## Exibe os logs em tempo real do backend
	$(DOCKER_COMPOSE) logs -f api

db-shell: ## Acessa o terminal do banco de dados
	docker exec -it auto-u-db psql -U admin -d autou_db

test: ## Executa os testes unitários com cobertura
	export PYTHONPATH=. && pytest src/tests -v

get-service-url: # Para capturar a URL do serviço via make
	@cd infra/gcp && terraform output -raw service_url