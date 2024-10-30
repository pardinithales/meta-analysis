import pandas as pd
import os
from datetime import datetime

def process_lilacs_results():
    """Processa os resultados exportados do LILACS"""
    
    # Definir caminhos
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LILACS_FILE = os.path.join(BASE_DIR, "02_searches", "data", "lilacs_results.csv")
    
    print("Processando resultados do LILACS...")
    
    # Ler arquivo
    df = pd.read_csv(LILACS_FILE)
    
    # Adicionar colunas para screening
    df['Decisão'] = None
    df['Motivo_Exclusão'] = None
    df['Base'] = 'LILACS'
    df['Data_Screening'] = datetime.now().strftime('%Y-%m-%d')
    
    # Salvar versão processada
    output_file = os.path.join(BASE_DIR, "02_searches", "data", "lilacs_screening.xlsx")
    df.to_excel(output_file, index=False)
    
    print(f"\nProcessamento concluído!")
    print(f"Total de referências: {len(df)}")
    print(f"Arquivo salvo em: {output_file}")
    
    return df

if __name__ == "__main__":
    df = process_lilacs_results() 