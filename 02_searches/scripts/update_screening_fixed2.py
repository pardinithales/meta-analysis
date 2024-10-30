import pandas as pd
from datetime import datetime

def update_screening_database():
    """Atualiza o banco de dados de screening mantendo todos os dados"""
    
    print("🔄 Atualizando banco de dados de screening...\n")
    
    # Carregar dados existentes
    screening_df = pd.read_excel("02_searches/data/screening_database.xlsx")
    screening_titles = set(screening_df['Título'].str.lower())
    
    # Adicionar coluna Base aos dados existentes
    screening_df['Base'] = 'PubMed'
    
    # Carregar Scopus
    scopus_df = pd.read_csv("02_searches/data/scopus.csv")
    
    # Preparar novos dados do Scopus
    new_articles = []
    for _, row in scopus_df.iterrows():
        if row['Title'].lower() not in screening_titles:
            new_articles.append({
                'PMID': None,
                'Título': row['Title'],
                'Autores': row['Authors'],
                'Referência Completa': f"{row['Authors']} ({row['Year']}). {row['Title']}. {row['Source title']}",
                'Primeiro Autor': row['Authors'].split(';')[0].strip(),
                'Journal/Book': row['Source title'],
                'Publication Year': row['Year'],
                'Create Date': datetime.now().strftime('%Y-%m-%d'),
                'PMCID': None,
                'NIHMS ID': None,
                'DOI': row['DOI'],
                'Decisão': None,
                'Motivo_Exclusão': None,
                'Observações': None,
                'Abstract': row['Abstract'],
                'Ano': row['Year'],
                'Base': 'Scopus'
            })
    
    # Adicionar novos artigos
    new_df = pd.DataFrame(new_articles)
    updated_df = pd.concat([screening_df, new_df], ignore_index=True)
    
    # Preencher valores ausentes
    updated_df['Ano'] = updated_df['Ano'].fillna(updated_df['Publication Year'])
    
    # Salvar arquivo atualizado
    updated_df.to_excel("02_searches/data/screening_database_updated.xlsx", index=False)
    
    print(f"✅ Adicionados {len(new_articles)} novos artigos")
    print(f"📊 Total de artigos no banco: {len(updated_df)}")

if __name__ == "__main__":
    update_screening_database() 