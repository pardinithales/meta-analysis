import pandas as pd
import os

def test_duplicates():
    """Testa duplicatas entre screening existente e Scopus"""
    
    print("🔍 Verificando duplicatas...\n")
    
    # Carregar dados do screening existente (PubMed)
    try:
        screening_df = pd.read_excel("02_searches/data/screening_database.xlsx")
        print(f"✅ Screening atual: {len(screening_df)} artigos carregados")
        screening_titles = set(screening_df['Título'].str.lower())
    except Exception as e:
        print(f"❌ Erro ao carregar screening database: {str(e)}")
        return
    
    # Carregar dados do Scopus
    try:
        scopus_df = pd.read_csv("02_searches/data/scopus.csv")
        print(f"✅ Scopus: {len(scopus_df)} artigos carregados")
        scopus_titles = set(scopus_df['Title'].str.lower())
    except Exception as e:
        print(f"❌ Erro ao carregar Scopus: {str(e)}")
        return
    
    # Encontrar duplicatas
    duplicates = screening_titles.intersection(scopus_titles)
    
    print(f"\n📊 Resultados:")
    print(f"- Screening atual: {len(screening_titles)} títulos únicos")
    print(f"- Scopus novos: {len(scopus_titles)} títulos")
    print(f"- Duplicatas encontradas: {len(duplicates)}")
    
    if len(duplicates) > 0:
        print("\n📝 Títulos duplicados:")
        for i, title in enumerate(duplicates, 1):
            print(f"{i}. {title}")

if __name__ == "__main__":
    test_duplicates() 