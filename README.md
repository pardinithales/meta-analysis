# API de Meta-análise para Neurocisticercose

API REST para gerenciar dados de estudos sobre neurocisticercose.

## Estrutura do Projeto
meta-analysis_neurocisticercosis/
├── 02_searches/
│ ├── api/
│ │ └── main.py
│ ├── data/
│ │ └── .json
│ └── outputs/
│ └── .xlsx
├── documentation/
└── scripts/




## Instalação

1. Clone o repositório
2. Crie um ambiente virtual Python:

python -m venv venv


3. Instale as dependências:

pip install fastapi uvicorn pandas openpyxl


4. Inicie o servidor:


cd 02_searches/api

cd 02_searches/api

uvicorn main:app --reload


## Endpoints

- `POST /study/`: Criar/atualizar estudo
- `GET /study/{study_id}`: Obter estudo específico
- `GET /studies/`: Listar todos os estudos
- `DELETE /study/{study_id}`: Deletar estudo
- `GET /export`: Exportar estudos para Excel

## Uso

Acesse a documentação interativa em: http://localhost:8000/docs

## Exemplos

### Adicionar Estudo

$jsonBody = @{

$jsonBody = @{
"Study_ID" = "Example_2024"
"First_Author" = "Silva, J."
"Year" = "2024"
# ... outros campos
}
Invoke-RestMethod -Uri "http://localhost:8000/study/" -Method Post
-Body ($jsonBody | ConvertTo-Json) -ContentType "application/json"

Exportar para Excel

Invoke-RestMethod -Uri "http://localhost:8000/export" `
                 -Method Get `
                 -OutFile "estudos.xlsx"

