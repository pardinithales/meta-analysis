import pandas as pd

def test_setup():
    print("Configuração de teste iniciada...")
    
    # Criar um DataFrame de exemplo
    data = {
        'title': ['Teste 1', 'Teste 2'],
        'authors': ['Autor A', 'Autor B'],
        'year': [2023, 2024]
    }
    
    df = pd.DataFrame(data)
    print("\nDataFrame de teste criado com sucesso:")
    print(df)
    
if __name__ == "__main__":
    test_setup()
