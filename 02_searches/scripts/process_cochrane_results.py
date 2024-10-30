import pandas as pd
from datetime import datetime

def process_cochrane_results():
    """Processa resultados da Cochrane e adiciona ao banco de screening"""
    
    print("🔄 Processando resultados da Cochrane...\n")
    
    # Carregar banco existente
    try:
        screening_df = pd.read_excel("02_searches/data/screening_database.xlsx")
        screening_titles = set(screening_df['Título'].str.lower())
        print(f"📊 Banco atual: {len(screening_df)} artigos")
    except FileNotFoundError:
        screening_df = pd.DataFrame()
        screening_titles = set()
        print("❗ Banco de dados não encontrado, será criado um novo")
    
    # Carregar resultados da Cochrane
    cochrane_df = pd.read_csv("02_searches/data/screening_cochrane.csv")
    print(f"📥 Resultados Cochrane: {len(cochrane_df)} artigos")
    
    # Preparar novos artigos
    new_articles = []
    for _, row in cochrane_df.iterrows():
        if row['Title'].lower() not in screening_titles:
            new_articles.append({
                'Título': row['Title'],
                'Autores': row['Author(s)'],
                'Abstract': row['Abstract'],
                'Ano': row['Year'],
                'DOI': row['DOI'],
                'Base': 'Cochrane',
                'Decisão': None,
                'Motivo_Exclusão': None,
                'Journal': row['Source'],
                'PMID': row['PubMed ID'].replace('PUBMED ', '') if pd.notna(row['PubMed ID']) else None,
                'Keywords': row['Keywords']
            })
    
    # Adicionar novos artigos
    if new_articles:
        new_df = pd.DataFrame(new_articles)
        updated_df = pd.concat([screening_df, new_df], ignore_index=True)
        updated_df.to_excel("02_searches/data/screening_database.xlsx", index=False)
        print(f"\n✅ Adicionados {len(new_articles)} novos artigos")
        print(f"📊 Total no banco: {len(updated_df)} artigos")
    else:
        print("\n✅ Nenhum novo artigo para adicionar")
    
    return len(new_articles)

if __name__ == "__main__":
    process_cochrane_results() 