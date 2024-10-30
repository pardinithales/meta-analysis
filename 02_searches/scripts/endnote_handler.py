import os
from config import ENDNOTE_SETTINGS, REFERENCE_FIELDS
import pandas as pd

def check_endnote_exports():
    """Verifica se o diretório de exportação do EndNote existe e está acessível"""
    export_path = ENDNOTE_SETTINGS['export_path']
    if os.path.exists(export_path):
        print(f"Diretório de exportação encontrado: {export_path}")
        return True
    else:
        print(f"ERRO: Diretório não encontrado: {export_path}")
        return False

def test_endnote_setup():
    """Testa a configuração básica do EndNote"""
    print("Iniciando teste de configuração do EndNote...")
    
    # Verifica diretório
    if check_endnote_exports():
        print("✓ Verificação de diretório OK")
    
    # Verifica configurações
    print("\nConfigurações carregadas:")
    for key, value in ENDNOTE_SETTINGS.items():
        print(f"  {key}: {value}")
    
    print("\nCampos de referência definidos:")
    for field in REFERENCE_FIELDS:
        print(f"  - {field}")

if __name__ == "__main__":
    test_endnote_setup()
