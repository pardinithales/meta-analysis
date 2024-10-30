import pandas as pd
import os
from datetime import datetime

# Caminhos dos arquivos
PUBMED_FILE = "02_searches/data/pubmed_results.csv"
SCOPUS_FILE = "02_searches/data/scopus.csv"
SCREENING_FILE = "02_searches/data/screening_database.xlsx"
HISTORY_FILE = "02_searches/data/screening_history.xlsx"

def load_scopus_data():
    """Carrega dados do Scopus"""
    df = pd.read_csv(SCOPUS_FILE)
    return pd.DataFrame({
        'Título': df['Title'],
        'Abstract': df['Abstract'],
        'Autores': df['Authors'],
        'Ano': df['Year'],
        'DOI': df['DOI'],
        'Base': 'Scopus',
        'Decisão': None
    })

def load_all_data():
    """Carrega e combina dados do PubMed e Scopus"""
    # Carregar dados existentes ou criar novo
    if os.path.exists(SCREENING_FILE):
        return pd.read_excel(SCREENING_FILE)
    
    # Combinar dados das duas bases
    pubmed_df = pd.read_csv(PUBMED_FILE)  # manter formato anterior
    scopus_df = load_scopus_data()
    
    # Combinar e remover duplicatas
    df = pd.concat([pubmed_df, scopus_df], ignore_index=True)
    df = df.drop_duplicates(subset=['Título'], keep='first')
    
    return df

def save_history(article, decision):
    """Salva histórico de decisões"""
    history = {
        'Data': datetime.now(),
        'Título': article['Título'],
        'Base': article['Base'],
        'Decisão': decision
    }
    
    if os.path.exists(HISTORY_FILE):
        history_df = pd.read_excel(HISTORY_FILE)
        history_df = history_df.append(history, ignore_index=True)
    else:
        history_df = pd.DataFrame([history])
    
    history_df.to_excel(HISTORY_FILE, index=False)

def show_statistics():
    """Mostra estatísticas do screening"""
    if os.path.exists(SCREENING_FILE):
        df = pd.read_excel(SCREENING_FILE)
        print("\nEstatísticas do Screening:")
        print(f"Total de artigos: {len(df)}")
        print("\nPor base de dados:")
        print(df['Base'].value_counts())
        print("\nPor decisão:")
        print(df['Decisão'].value_counts())