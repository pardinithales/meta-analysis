import pandas as pd
import os
from datetime import datetime

# Caminhos dos arquivos
LILACS_RESULTS = "02_searches/data/lilacs_results.csv"
LILACS_SCREENING = "02_searches/data/lilacs_screening.xlsx"

def load_lilacs_data():
    """Carrega dados do LILACS"""
    if not os.path.exists(LILACS_SCREENING):
        print("\n🔍 Depuração do carregamento de dados:")
        
        # 1. Ler CSV com parâmetros específicos
        df = pd.read_csv(LILACS_RESULTS, 
                        encoding='utf-8',
                        quoting=1,
                        skipinitialspace=True)
        
        print("\n1. Colunas do DataFrame:")
        print(df.columns.tolist())
        
        print("\n2. Primeira linha do CSV:")
        primeira_linha = df.iloc[0]
        for col in ['ID', 'Title', 'Authors', 'Source']:
            print(f"{col}: {primeira_linha[col]}")
        
        # Completar função temporariamente
        screening_df = pd.DataFrame({
            'Title': df['ID'].str.replace(r'^"?biblio-\d+",?"?', '', regex=True)  # Remove ID
                               .str.split('/').str[0].str.strip(),  # Pega apenas a parte em inglês
            'Authors': df['Title'],
            'Source': df['Source'].str.split(';').str[0].str.strip(),
            'Publication year': pd.to_numeric(df['Publication year'], errors='coerce'),
            'Type': df['Type'],
            'Language': df['Language'],
            'Abstract': df['Abstract'],
            'Base': 'LILACS',
            'Decisão': None,
            'Motivo_Exclusão': None
        })
        
        screening_df.to_excel(LILACS_SCREENING, index=False)
        return screening_df
    
    return pd.read_excel(LILACS_SCREENING)

def save_progress(df):
    """Salva o progresso do screening"""
    df.to_excel(LILACS_SCREENING, index=False)
    print("✅ Progresso salvo")

def show_statistics():
    """Mostra estatísticas do screening LILACS"""
    if os.path.exists(LILACS_SCREENING):
        df = pd.read_excel(LILACS_SCREENING)
        total = len(df)
        pending = df['Decisão'].isna().sum()
        included = (df['Decisão'] == 'Incluído').sum()
        excluded = (df['Decisão'] == 'Excluído').sum()
        
        print("\n📊 Estatísticas do Screening LILACS:")
        print(f"Total de artigos: {total}")
        print(f"Pendentes: {pending}")
        print(f"Incluídos: {included}")
        print(f"Excluídos: {excluded}")
