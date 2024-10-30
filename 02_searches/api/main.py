from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from datetime import datetime

app = FastAPI(title="Meta-Analysis API",
             description="API para gerenciar dados de meta-análise de neurocisticercose")

class StudyData(BaseModel):
    # ... (manter todos os campos existentes) ...

    class Config:
        json_encoders = {
            str: lambda v: v.encode("utf-8").decode("utf-8") if isinstance(v, str) else v
        }

# Rota para listar todos os estudos
@app.get("/studies/", response_model=List[str])
async def list_studies():
    """Lista todos os estudos disponíveis"""
    try:
        files = os.listdir("../data")
        return [f.replace(".json", "") for f in files if f.endswith(".json")]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para criar/atualizar estudo
@app.post("/study/")
async def create_study(study: StudyData):
    """Cria ou atualiza um estudo"""
    try:
        study_dict = study.dict(exclude_unset=True)
        os.makedirs("../data", exist_ok=True)
        
        # Adicionar timestamp
        study_dict["last_modified"] = datetime.now().isoformat()
        
        filename = f"../data/{study.Study_ID}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(study_dict, f, ensure_ascii=False, indent=2)
        
        return {
            "message": "Estudo salvo com sucesso",
            "study_id": study.Study_ID,
            "timestamp": study_dict["last_modified"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para obter um estudo
@app.get("/study/{study_id}")
async def get_study(study_id: str):
    """Obtém os dados de um estudo específico"""
    try:
        with open(f"../data/{study_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Estudo não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para deletar um estudo
@app.delete("/study/{study_id}")
async def delete_study(study_id: str):
    """Deleta um estudo específico"""
    try:
        filename = f"../data/{study_id}.json"
        os.remove(filename)
        return {"message": f"Estudo {study_id} deletado com sucesso"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Estudo não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para exportar todos os estudos para Excel
@app.get("/export/excel")
async def export_to_excel():
    """Exporta todos os estudos para Excel"""
    try:
        import pandas as pd
        
        # Ler todos os arquivos JSON
        studies = []
        for file in os.listdir("../data"):
            if file.endswith(".json"):
                with open(f"../data/{file}", "r", encoding="utf-8") as f:
                    studies.append(json.load(f))
        
        # Criar DataFrame
        df = pd.DataFrame(studies)
        
        # Criar pasta outputs se não existir
        os.makedirs("../outputs", exist_ok=True)
        
        # Salvar Excel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../outputs/studies_export_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        
        return {"message": f"Dados exportados para {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
