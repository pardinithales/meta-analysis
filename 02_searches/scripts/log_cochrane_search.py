import pandas as pd
import os
from datetime import datetime

def log_cochrane_search():
    """Registra detalhes da busca na Cochrane Library"""
    
    # Detalhes da busca
    search_details = {
        'Database': 'Cochrane Library',
        'Date_of_Search': '2024-02-14',
        'Search_String': '''(neurocysticercosis OR "brain cysticercosis" OR 
                           "central nervous system cysticercosis" OR 
                           "cerebral cysticercosis" OR "CNS cysticercosis") 
                           AND (albendazole OR praziquantel OR 
                           "antiparasitic agents" OR anthelmintics) 
                           AND (human* OR patient*) 
                           NOT (animal* NOT human*)''',
        'Filters_Applied': '''- Database: Trials
                             - Date Range: 2004-2024
                             - Language: English, Spanish, Portuguese
                             - Search Fields: Title, Abstract, Keywords''',
        'Total_Results': 50,
        'Date_Range': '2004-2024',
        'Notes': 'Busca realizada na interface web da Cochrane Library'
    }
    
    # Carregar ou criar planilha de registro
    excel_path = r'C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis\02_searches\data\search_tracking.xlsx'
    
    try:
        # Tentar ler todas as abas existentes
        all_sheets = pd.read_excel(excel_path, sheet_name=None)
        search_log = all_sheets.get('Search_Log', pd.DataFrame(columns=[
            'Database', 'Date_of_Search', 'Search_String', 
            'Filters_Applied', 'Total_Results', 'Date_Range', 'Notes'
        ]))
    except FileNotFoundError:
        # Se arquivo não existe, criar novo DataFrame
        search_log = pd.DataFrame(columns=[
            'Database', 'Date_of_Search', 'Search_String', 
            'Filters_Applied', 'Total_Results', 'Date_Range', 'Notes'
        ])
        all_sheets = {'Search_Log': search_log}
    
    # Adicionar nova busca ao registro
    search_log = pd.concat([search_log, pd.DataFrame([search_details])], ignore_index=True)
    all_sheets['Search_Log'] = search_log
    
    # Salvar todas as abas
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print("\n=== Registro de Busca Cochrane Library ===")
    print("\nDetalhes salvos:")
    for key, value in search_details.items():
        print(f"\n{key}:")
        print(value)
    
    print(f"\nRegistro salvo em: {excel_path}")
    print("\nPróximos passos:")
    print("1. Verificar se todos os 50 resultados foram exportados corretamente")
    print("2. Processar os resultados usando process_cochrane_results.py")
    print("3. Iniciar o screening dos artigos")

if __name__ == "__main__":
    log_cochrane_search()