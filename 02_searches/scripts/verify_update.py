import pandas as pd

def verify_database():
    """Verifica o conteúdo do banco de dados atualizado"""
    
    print("🔍 Verificando banco de dados atualizado...\n")
    
    # Carregar arquivo atualizado
    df = pd.read_excel("02_searches/data/screening_database_updated.xlsx")
    
    # Estatísticas
    print("📊 Estatísticas:")
    print(f"- Total de artigos: {len(df)}")
    print(f"- Artigos por base:")
    print(df['Base'].value_counts())
    print(f"\n- Artigos por ano:")
    print(df['Ano'].value_counts().sort_index())
    
    # Verificar dados ausentes
    print("\n🔍 Verificando dados ausentes:")
    print(df.isnull().sum())

if __name__ == "__main__":
    verify_database() 