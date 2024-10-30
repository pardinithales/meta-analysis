from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
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
