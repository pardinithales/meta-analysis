import requests
import json
from typing import Dict, Any

def get_study(study_id: str) -> Dict[Any, Any]:
    """
    Obtém os dados de um estudo existente
    
    Args:
        study_id: ID do estudo a ser obtido
        
    Returns:
        Dicionário com os dados do estudo
    """
    try:
        response = requests.get(f"http://localhost:8000/study/{study_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter estudo: {response.text}")
            return None
    except Exception as e:
        print(f"Erro: {str(e)}")
        return None

def edit_study(study_id: str, updated_data: Dict[Any, Any]) -> None:
    """
    Edita um estudo existente
    
    Args:
        study_id: ID do estudo a ser editado
        updated_data: Dicionário com os dados atualizados
    """
    try:
        # Enviar requisição PUT
        response = requests.put(
            url=f"http://localhost:8000/study/{study_id}",
            json=updated_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Verificar resposta
        if response.status_code == 200:
            print(f"Estudo {study_id} atualizado com sucesso!")
            print(f"Timestamp: {response.json()['timestamp']}")
        else:
            print(f"Erro ao atualizar estudo: {response.text}")
            
    except Exception as e:
        print(f"Erro na edição: {str(e)}")

# Exemplo de uso
if __name__ == "__main__":
    # ID do estudo a ser editado
    study_id = "Garcia2024"
    
    # Obter dados atuais
    current_data = get_study(study_id)
    if current_data:
        # Fazer alterações necessárias
        current_data["Risk_of_Bias"] = "Medium"
        current_data["Comments"] = "Atualizado: risco de viés reavaliado"
        
        # Enviar atualizações
        edit_study(study_id, current_data) 