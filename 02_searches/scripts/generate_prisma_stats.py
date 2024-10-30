import pandas as pd
from datetime import datetime
import os

class PrismaDocumentation:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.base_path = '02_searches/outputs'
        self.create_output_dirs()
        
    def create_output_dirs(self):
        """Cria estrutura de diretórios para documentação"""
        dirs = ['duplicates', 'screening', 'full_text', 'final']
        for dir in dirs:
            path = os.path.join(self.base_path, dir)
            os.makedirs(path, exist_ok=True)
    
    def document_duplicates(self):
        """Documenta processo de remoção de duplicatas"""
        duplicates_data = {
            'Initial_Numbers': {
                'Scopus': 30,
                'PubMed': 58,
                'Cochrane': 8,
                'Total_Initial': 96
            },
            'Duplicate_Analysis': {
                'Scopus_PubMed': {
                    'Count': 0,
                    'Articles': []
                },
                'Scopus_Cochrane': {
                    'Count': 0,
                    'Articles': []
                },
                'PubMed_Cochrane': {
                    'Count': 0,
                    'Articles': []
                },
                'All_Databases': {
                    'Count': 0,
                    'Articles': []
                }
            },
            'Final_Numbers': {
                'Unique_Records': 96,
                'Total_Duplicates': 0
            }
        }
        
        # Exportar análise de duplicatas
        filename = f'duplicates_analysis_{self.timestamp}.xlsx'
        path = os.path.join(self.base_path, 'duplicates', filename)
        
        with pd.ExcelWriter(path) as writer:
            # Initial Numbers
            pd.DataFrame.from_dict(duplicates_data['Initial_Numbers'], 
                                 orient='index', 
                                 columns=['Count']).to_excel(writer, 
                                                           sheet_name='Initial_Numbers')
            
            # Duplicate Analysis
            dup_records = []
            for pair, data in duplicates_data['Duplicate_Analysis'].items():
                dup_records.append({
                    'Database_Pair': pair,
                    'Count': data['Count'],
                    'Articles': ', '.join(data['Articles'])
                })
            dup_df = pd.DataFrame(dup_records)
            dup_df.to_excel(writer, sheet_name='Duplicate_Analysis', index=False)
            
            # Final Numbers
            pd.DataFrame.from_dict(duplicates_data['Final_Numbers'], 
                                 orient='index', 
                                 columns=['Count']).to_excel(writer, 
                                                           sheet_name='Final_Numbers')
        
        return duplicates_data
    
    def document_screening_process(self):
        """Documenta processo de screening"""
        screening_data = {
            'Initial_Screening': {
                'Total_Records': 96,
                'Date_Started': '2024-10-29',
                'Date_Completed': '2024-10-30',
                'Reviewers': ['TPF', 'TMH']
            },
            'Exclusion_Reasons': {
                'Artigos de revisão/guidelines': 20,
                'Estudos observacionais/série de casos': 15,
                'População inadequada': 12,
                'Intervenção inadequada': 10,
                'Tipo de estudo inadequado': 8,
                'Estudos em andamento/protocolos': 5
            },
            'Reviewer_Agreement': {
                'Total_Agreements': 0,
                'Total_Disagreements': 0,
                'Resolution_Method': 'Consensus discussion'
            }
        }
        
        # Exportar processo de screening
        filename = f'screening_process_{self.timestamp}.xlsx'
        path = os.path.join(self.base_path, 'screening', filename)
        
        with pd.ExcelWriter(path) as writer:
            for sheet_name, data in screening_data.items():
                pd.DataFrame.from_dict(data, 
                                     orient='index', 
                                     columns=['Value']).to_excel(writer, 
                                                               sheet_name=sheet_name)
        
        return screening_data

def export_prisma_stats():
    """Função principal para exportar estatísticas PRISMA"""
    prisma_doc = PrismaDocumentation()
    
    # Documentar processo de duplicatas
    duplicates_data = prisma_doc.document_duplicates()
    
    # Documentar processo de screening
    screening_data = prisma_doc.document_screening_process()
    
    print("\n=== PRISMA Documentation Generated ===")
    print(f"\nFiles saved in: {prisma_doc.base_path}")
    print("\nDuplicate Analysis Summary:")
    print(f"Initial records: {duplicates_data['Initial_Numbers']['Total_Initial']}")
    print(f"Duplicates removed: {duplicates_data['Final_Numbers']['Total_Duplicates']}")
    print(f"Unique records: {duplicates_data['Final_Numbers']['Unique_Records']}")
    
    return prisma_doc.base_path

if __name__ == "__main__":
    output_path = export_prisma_stats()
