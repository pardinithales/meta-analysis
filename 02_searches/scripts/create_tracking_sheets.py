# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime

def create_search_spreadsheet():
    # Diretório de dados
    data_dir = r'C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis\02_searches\data'
    
    # Criar DataFrame para registro de buscas
    search_log = pd.DataFrame(columns=[
        'Database',
        'Date_of_Search',
        'Search_String',
        'Total_Results',
        'Exported_Results',
        'Notes'
    ])
    
    # Criar DataFrame para screening inicial
    screening_log = pd.DataFrame(columns=[
        'Title',
        'Authors',
        'Year',
        'Database',
        'Human_Study',
        'Parenchymal_NCC',
        'Treatment_Type',
        'Reports_Outcomes',
        'Full_Text',
        'Include',
        'Notes'
    ])
    
    # Criar arquivo Excel com múltiplas abas
    with pd.ExcelWriter(os.path.join(data_dir, 'search_tracking.xlsx')) as writer:
        search_log.to_excel(writer, sheet_name='Search_Log', index=False)
        screening_log.to_excel(writer, sheet_name='Screening_Log', index=False)

    print(f"Planilha de registro criada em: {os.path.join(data_dir, 'search_tracking.xlsx')}")
    print("\nAbas criadas:")
    print("1. Search_Log - Para registrar as buscas em cada base")
    print("2. Screening_Log - Para registrar o screening inicial dos artigos")

if __name__ == "__main__":
    create_search_spreadsheet()
