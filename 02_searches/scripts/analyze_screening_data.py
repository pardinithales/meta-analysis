import pandas as pd
import os

def analyze_screening_data():
    """Analisa ambos os bancos de screening"""
    
    print("\n=== Análise dos Bancos de Screening ===")
    
    # Análise Cochrane
    try:
        cochrane_df = pd.read_excel("02_searches/data/screening_database.xlsx")
        print("\nCOCHRANE:")
        print(f"Total de registros: {len(cochrane_df)}")
        
        # Análise das decisões
        if 'Decisão' in cochrane_df.columns:
            decisao_counts = cochrane_df['Decisão'].value_counts()
            print("\nStatus das decisões Cochrane:")
            print(decisao_counts)
        
        # Análise dos motivos de exclusão
        if 'Motivo_Exclusão' in cochrane_df.columns:
            motivos_counts = cochrane_df['Motivo_Exclusão'].value_counts()
            print("\nMotivos de exclusão Cochrane:")
            print(motivos_counts)
            
    except Exception as e:
        print(f"Erro ao ler arquivo Cochrane: {e}")
    
    # Análise LILACS
    try:
        lilacs_df = pd.read_excel("02_searches/data/lilacs_screening.xlsx")
        print("\nLILACS:")
        print(f"Total de registros: {len(lilacs_df)}")
        
        # Análise das decisões
        if 'Decisão' in lilacs_df.columns:
            decisao_counts = lilacs_df['Decisão'].value_counts()
            print("\nStatus das decisões LILACS:")
            print(decisao_counts)
        
        # Análise dos motivos de exclusão
        if 'Motivo_Exclusão' in lilacs_df.columns:
            motivos_counts = lilacs_df['Motivo_Exclusão'].value_counts()
            print("\nMotivos de exclusão LILACS:")
            print(motivos_counts)
            
    except Exception as e:
        print(f"Erro ao ler arquivo LILACS: {e}")

if __name__ == "__main__":
    analyze_screening_data()