from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime
import pandas as pd

app = FastAPI()

class StudyData(BaseModel):
    Study_ID: Optional[str] = None
    First_Author: Optional[str] = None
    Year: Optional[str] = None
    Country: Optional[str] = None
    Study_Design: Optional[str] = None
    Risk_of_Bias: Optional[str] = None
    Diagnostic_Criteria: Optional[str] = None
    Total_Sample_Size: Optional[str] = None
    Treatment_Group_N: Optional[str] = None
    Control_Group_N: Optional[str] = None
    Age_Mean_SD: Optional[str] = None
    Male_Percentage: Optional[str] = None
    Female_Percentage: Optional[str] = None
    Other_Demographics: Optional[str] = None
    Headache_Percentage: Optional[str] = None
    Focal_Seizures_Percentage: Optional[str] = None
    Other_Symptoms: Optional[str] = None
    Treatment_Type: Optional[str] = None
    Albendazole_Dose: Optional[str] = None
    Treatment_Duration_Days: Optional[str] = None
    Number_of_Cycles: Optional[str] = None
    Cycle_Interval_Days: Optional[str] = None
    Praziquantel_Dose: Optional[str] = None
    Corticosteroid_Type: Optional[str] = None
    Antiepileptic_Drug: Optional[str] = None
    Follow_up_Duration_Months: Optional[str] = None
    Imaging_Schedule: Optional[str] = None
    Complete_Resolution_Percentage: Optional[str] = None
    Partial_Resolution_Percentage: Optional[str] = None
    No_Change_Percentage: Optional[str] = None
    Seizure_Reduction_Percentage: Optional[str] = None
    Elevated_Liver_Enzymes_Percentage: Optional[str] = None
    Other_AE: Optional[str] = None
    Comments: Optional[str] = None

# Conferir se o POST está certo
@app.post("/study")
async def create_study(study: Dict[str, Any]):
    """Cria um novo estudo"""
    try:
        # Verificar se tem Study_ID
        if "Study_ID" not in study:
            raise HTTPException(status_code=400, detail="Study_ID é obrigatório")
        
        study_id = study["Study_ID"]
        filename = f"../data/{study_id}.json"
        
        # Verificar se já existe
        if os.path.exists(filename):
            raise HTTPException(status_code=400, detail="Estudo já existe")
        
        # Adicionar timestamp
        study["last_modified"] = datetime.now().isoformat()
        
        # Salvar arquivo
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(study, f, ensure_ascii=False, indent=2)
        
        return {
            "message": "Estudo criado com sucesso",
            "study_id": study_id,
            "timestamp": study["last_modified"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export")
async def export_to_excel():
    """Exporta todos os estudos para Excel"""
    try:
        print("Iniciando exportação...")
        os.makedirs("../outputs", exist_ok=True)
        print(f"Diretório atual: {os.getcwd()}")
        
        studies = []
        data_dir = "../data"
        print(f"Lendo arquivos de: {os.path.abspath(data_dir)}")
        
        for file in os.listdir(data_dir):
            if file.endswith(".json"):
                print(f"Processando: {file}")
                with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
                    studies.append(json.load(f))
        
        print(f"Total de estudos: {len(studies)}")
        df = pd.DataFrame(studies)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("../outputs", f"studies_export_{timestamp}.xlsx")
        print(f"Salvando em: {filename}")
        
        df.to_excel(filename, index=False)
        print("Excel criado com sucesso")
        
        return FileResponse(
            path=filename,
            filename=f"studies_export_{timestamp}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/studies/")
async def list_studies():
    try:
        files = os.listdir("../data")
        return [f.replace(".json", "") for f in files if f.endswith(".json")]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/study/{study_id}")
async def get_study(study_id: str):
    try:
        with open(f"../data/{study_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Estudo não encontrado")

@app.put("/study/{study_id}")
async def update_study(study_id: str, study: Dict[str, Any]):
    """Atualiza um estudo existente"""
    try:
        # Verificar se o estudo existe
        filename = f"../data/{study_id}.json"
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Estudo não encontrado")
        
        # Adicionar timestamp
        study["last_modified"] = datetime.now().isoformat()
        
        # Se estiver mudando o Study_ID
        new_study_id = study.get("Study_ID")
        if new_study_id and new_study_id != study_id:
            new_filename = f"../data/{new_study_id}.json"
            
            # Primeiro salvar o novo arquivo
            with open(new_filename, "w", encoding="utf-8") as f:
                json.dump(study, f, ensure_ascii=False, indent=2)
            
            # Verificar se o novo arquivo foi criado
            if not os.path.exists(new_filename):
                raise HTTPException(status_code=500, detail="Falha ao criar novo arquivo")
            
            # Remover arquivo antigo
            if os.path.exists(filename):
                os.remove(filename)
            
            # Verificar se o arquivo antigo foi removido
            if os.path.exists(filename):
                raise HTTPException(status_code=500, detail="Falha ao remover arquivo antigo")
            
            # Verificar se o novo arquivo ainda existe
            if not os.path.exists(new_filename):
                raise HTTPException(status_code=500, detail="Novo arquivo não encontrado após criação")
            
            return {
                "message": "Estudo atualizado com sucesso",
                "study_id": new_study_id,
                "old_id": study_id,
                "timestamp": study["last_modified"]
            }
        
        # Se não estiver mudando o ID
        else:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(study, f, ensure_ascii=False, indent=2)
            
            # Verificar se o arquivo foi salvo
            if not os.path.exists(filename):
                raise HTTPException(status_code=500, detail="Falha ao salvar arquivo")
            
            return {
                "message": "Estudo atualizado com sucesso",
                "study_id": study_id,
                "timestamp": study["last_modified"]
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/study/{study_id}")
async def delete_study(study_id: str):
    """Deleta um estudo existente"""
    try:
        filename = f"../data/{study_id}.json"
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Estudo não encontrado")
        
        os.remove(filename)
        
        return {
            "message": "Estudo deletado com sucesso",
            "study_id": study_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
