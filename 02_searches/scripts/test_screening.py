import pandas as pd

# Testar leitura do arquivo Scopus
def test_scopus_reading():
    try:
        # Tentar ler o arquivo
        df = pd.read_csv("02_searches/data/scopus.csv")
        
        # Verificar colunas necessárias
        required_columns = ['Title', 'Abstract', 'Authors', 'Year', 'DOI']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Faltam colunas: {missing_columns}")
        else:
            print("✅ Todas as colunas necessárias estão presentes")
            
        # Mostrar primeiras linhas
        print("\nPrimeiras linhas do DataFrame:")
        print(df[['Title', 'Year', 'Authors']].head(2))
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testando leitura do arquivo Scopus...")
    test_scopus_reading() 