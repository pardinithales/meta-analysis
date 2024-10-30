import pandas as pd

def update_screening_database():
    """Atualiza o banco de dados de screening com novos artigos do Scopus"""
    
    print("🔄 Atualizando banco de dados de screening...\n")
    
    # Carregar dados existentes
    screening_df = pd.read_excel("02_searches/data/screening_database.xlsx")
    screening_titles = set(screening_df['Título'].str.lower())
    
    # Carregar Scopus
    scopus_df = pd.read_csv("02_searches/data/scopus.csv")
    
    # Preparar novos dados do Scopus
    new_articles = []
    for _, row in scopus_df.iterrows():
        if row['Title'].lower() not in screening_titles:
            new_articles.append({
                'Título': row['Title'],
                'Abstract': row['Abstract'],
                'Autores': row['Authors'],
                'Ano': row['Year'],
                'DOI': row['DOI'],
                'Base': 'Scopus',
                'Decisão': None
            })
    
    # Adicionar novos artigos
    new_df = pd.DataFrame(new_articles)
    updated_df = pd.concat([screening_df, new_df], ignore_index=True)
    
    # Salvar arquivo atualizado
    updated_df.to_excel("02_searches/data/screening_database_updated.xlsx", index=False)
    
    print(f"✅ Adicionados {len(new_articles)} novos artigos")
    print(f"📊 Total de artigos no banco: {len(updated_df)}")

if __name__ == "__main__":
    update_screening_database() 