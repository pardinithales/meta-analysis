# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime

def log_pubmed_search():
    # Carregar planilha existente
    excel_path = r'C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis\02_searches\data\search_tracking.xlsx'
    
    print("=== Registro de Busca PubMed ===")
    print("\nString de busca para PubMed:")
    print("(neurocysticercosis OR \"Taenia solium\" OR \"brain cysticercosis\") AND (albendazole OR praziquantel OR antiparasitic OR treatment OR therapy)")
    
    # Coletar informações
    total_results = input("\nNúmero total de resultados encontrados: ")
    exported = input("Número de resultados exportados: ")
    notes = input("Observações adicionais: ")
    
    # Carregar o arquivo existente
    search_log = pd.read_excel(excel_path, sheet_name='Search_Log')
    
    # Adicionar nova linha
    new_row = {
        'Database': 'PubMed',
        'Date_of_Search': datetime.now().strftime('%Y-%m-%d'),
        'Search_String': '(neurocysticercosis OR "Taenia solium" OR "brain cysticercosis") AND (albendazole OR praziquantel OR antiparasitic OR treatment OR therapy)',
        'Total_Results': total_results,
        'Exported_Results': exported,
        'Notes': notes
    }
    
    # Adicionar à planilha
    search_log = pd.concat([search_log, pd.DataFrame([new_row])], ignore_index=True)
    
    # Salvar atualização
    with pd.ExcelWriter(excel_path, mode='a', if_sheet_exists='replace') as writer:
        search_log.to_excel(writer, sheet_name='Search_Log', index=False)
    
    print(f"\nBusca registrada com sucesso em: {excel_path}")
    print("\nPróximos passos:")
    print("1. Exporte os resultados do PubMed em formato XML")
    print("2. Salve o arquivo XML na pasta: \\02_searches\\data\\endnote_exports")
    print("3. Use o script xml_handler.py para processar os resultados")

if __name__ == "__main__":
    log_pubmed_search()
