# Meta-Analysis API

API REST para gerenciamento de dados da meta-análise de neurocisticercose.

## Instalação
Instalar dependências
pip install fastapi uvicorn pandas

Navegar até a pasta da API
cd 02_searches/api

Iniciar o servidor
uvicorn main:app --reload

## Endpoints Disponíveis

### 1. Listar Estudos
GET /studies/


### 2. Criar/Atualizar Estudo

POST /study/

Cria ou atualiza um estudo
Exemplo de corpo da requisição:
{
"Study_ID": "Kaur_2010",
"First_Author": "Kaur, Prabhjeet",
"Year": "2010"
# ... outros campos
}


### 3. Obter Estudo Específico

GET /study/{study_id}

Retorna os dados de um estudo específico
DELETE /study/{study_id}

### 5. Exportar para Excel
GET /export/excel




## Exemplos de Uso com PowerShell

### Listar Estudos

Invoke-RestMethod -Uri "http://localhost:8000/studies/" -Method Get

### Criar Novo Estudo


$jsonData = @{
Study_ID = "Exemplo_2024"
First_Author = "Autor Teste"
Year = "2024"
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8000/study/" -Method Post
-Body $jsonData -ContentType "application/json; charset=utf-8"

Obter Estudo
Invoke-RestMethod -Uri "http://localhost:8000/study/Exemplo_2024" -Method Get



### Deletar Estudo
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/study/Exemplo_2024" -Method Delete
```



### Exportar para Excel
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/export/excel" -Method Get
```


## Estrutura de Arquivos

```
02_searches/
├── api/
│   ├── main.py          # Código principal da API
├── data/                # Arquivos JSON dos estudos
└── outputs/             # Arquivos Excel exportados
```



## Campos Disponíveis

- Study_ID: Identificador único do estudo

Campos Disponíveis
Study_ID: Identificador único do estudo
First_Author: Primeiro autor
Year: Ano de publicação
Country: País do estudo
Study_Design: Desenho do estudo
Risk_of_Bias: Risco de viés
[... outros campos ...]
Notas
Todos os dados são salvos em formato JSON com codificação UTF-8
Cada estudo é identificado por seu Study_ID único
A exportação para Excel inclui timestamp no nome do arquivo
Os dados são validados automaticamente pelo modelo Pydantic
