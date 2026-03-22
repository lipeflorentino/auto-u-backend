# 🚀 Auto-U Backend: Inteligência Artificial para Triagem de E-mails

Este é o motor de processamento do **Auto-U**, uma solução desenvolvida para automatizar a classificação e resposta de e-mails em instituições financeiras. O foco principal é separar comunicações **Produtivas** (que exigem ação humana ou sistêmica) de **Improdutivas** (saudações, spans, agradecimentos), utilizando modelos de Deep Learning de última geração.

## 🧠 Decisões Técnicas & Inteligência Artificial

A escolha dos modelos de IA foi pautada pelo equilíbrio entre precisão semântica em Português e eficiência computacional.

### 1. Classificação: mDeBERTa-v3-base
Para a tarefa de *Zero-Shot Classification*, optei pelo **mDeBERTa-v3** em detrimento de modelos tradicionais como o BERT ou BART.
* **Por que Português?** O mDeBERTa (Multilingual Decoding-enhanced BERT with Disentangled Attention) utiliza um treinamento eletra-style que apresenta uma compreensão de nuances gramaticais e gírias em PT-BR muito superior, resultando em scores de confiança mais estáveis.
* **Desempenho:** Ele lida melhor com textos curtos e ruidosos, típicos de corpos de e-mail, identificando a intenção real por trás da mensagem.

### 2. Geração: Meta-Llama-3-8B-Instruct
Para a sugestão de resposta, utilizei o **Llama-3-8B** via interface de *Chat Completions*.
* **Prompt Engineering:** Implementei a técnica de *Few-Shot Prompting* no System Prompt para garantir que a IA gere respostas executivas, curtas e profissionais, evitando a prolixidade comum em modelos de larga escala.
* **Segurança:** O modelo foi instruído a nunca solicitar dados sensíveis, mantendo a conformidade com diretrizes bancárias.

---

## 🏗️ Arquitetura do Sistema

O projeto foi construído seguindo os princípios da **Clean Architecture**, garantindo que a lógica de negócio seja independente de IO, Banco de Dados ou Provedores de Nuvem.

* **Domain:** Contém as entidades e as interfaces (contracts) que definem o comportamento do sistema.
* **Application:** Implementa os casos de uso (Use Cases), orquestrando o fluxo entre a IA e as regras de negócio.
* **Infrastructure:** Implementações concretas de clientes de API (Hugging Face/Novita), serviços de NLP (spaCy) e configurações de ambiente.
* **Interfaces:** Ponto de entrada da aplicação via **FastAPI**, com DTOs validados via Pydantic para garantir o contrato com o Frontend React.

---

## 🛠️ Ferramentas & Tecnologias

| Tecnologia | Finalidade | Motivo |
| :--- | :--- | :--- |
| **Python 3.10** | Linguagem Core | Ecossistema maduro para IA e Processamento de Dados. |
| **FastAPI** | Framework Web | Alta performance (ASGI) e documentação automática com Swagger. |
| **spaCy (PT-BR)** | Pré-processamento | Limpeza de ruído e lematização para reduzir o custo de tokens na API. |
| **Uvicorn** | Servidor ASGI | Confiabilidade e baixo overhead para containers. |
| **Makefile** | Automação | Abstração de comandos complexos de build, teste e deploy. |
| **Terraform** | IaC (Infra as Code) | Provisionamento determinístico e transparente dos recursos de nuvem. |

---

### ☁️ Infraestrutura & Provisionamento

Utilizei **Terraform** para gerenciar a infraestrutura no **Google Cloud Platform (GCP)**, garantindo que o ambiente seja replicável e auditável.
* **Artifact Registry:** Repositório privado para versionamento de imagens Docker.
* **Cloud Run:** Ambiente serverless que escala conforme a demanda, otimizando custos.

### Docker Multi-Stage Build

Desenvolvi um `Dockerfile` otimizado em dois estágios:
1.  **Builder:** Compila as dependências e faz o download dos modelos pesados do spaCy.
2.  **Runner:** Uma imagem final leve (slim), contendo apenas o essencial para a execução, o que reduz drasticamente o tempo de inicialização (Cold Start) em ambientes serverless.

### Estratégia de Cloud (Agnostica)
A aplicação está preparada para rodar em:
* **Google Cloud Run:** Ideal pela simplicidade e escalabilidade baseada em requisições.
* **AWS App Runner:** Para uma integração nativa com o ecossistema AWS e ECR.

### CI/CD com GitHub Actions
Configurei pipelines automatizados que realizam:
* **Testes Automatizados:** Eu garanto a integridade do código rodando `make test` em cada Pull Request.
* **Deploy Contínuo:** O build da imagem e o push para os registros (GCR/ECR) são feitos automaticamente após o merge na branch `main`.

---

## ⚙️ Como Executar

"As credenciais de IA devem ser configuradas no arquivo .env seguindo o modelo disponível em .env.example".

**Pré-requisitos:** Docker e Terraform instalados.

1.  Clone o repositório.
2.  Crie um arquivo `.env` com seu `HUGGINGFACE_TOKEN`.
3.  **Provisionar Infra:**
    ```bash
    cd infra/gcp && terraform init && terraform apply
    ```
4.  **Execução Local:**
    ```bash
    make build-docker
    make up
    ```
5.  **Testes:**
    ```bash
    make test
    ```

---

## 🌐 API Online

A aplicação está disponível publicamente para consumo. 

> **Nota:** Por se tratar de uma infraestrutura *serverless* no Google Cloud Run, as primeiras requisições podem apresentar uma latência maior (**Cold Start**) enquanto o container é inicializado.

### Endpoints Principais

| Nome | Método | URL |
| :--- | :--- | :--- |
| **ClassifyEmail** | `POST` | `https://auto-u-backend-180653172521.southamerica-east1.run.app/classify` |
| **ExtractPDF** | `POST` | `https://auto-u-backend-180653172521.southamerica-east1.run.app/extract-pdf` |

---

## 📖 Documentação Interativa (Swagger)

O backend utiliza as capacidades nativas do **FastAPI** para expor uma documentação completa e interativa dos recursos disponíveis. Nela, é possível visualizar os esquemas de dados (DTOs) validados via **Pydantic** e realizar testes diretamente pelo navegador.

* **URL da Documentação:** [https://auto-u-backend-180653172521.southamerica-east1.run.app/docs](https://auto-u-backend-180653172521.southamerica-east1.run.app/docs)

---

---
*Desenvolvido por Filipe F. Lima - Fullstack Developer*