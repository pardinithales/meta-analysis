import os
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

class ReferenceManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.data_dir = os.path.join(project_dir, '02_searches', 'data')
        self.output_dir = os.path.join(project_dir, '02_searches', 'outputs')
        
        # Criar diretórios necessários
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Log de atividades
        self.log_file = os.path.join(self.output_dir, 'reference_log.txt')
        
    def log_activity(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp}: {message}\n")
            
    def import_endnote_xml(self, xml_file):
        """
        Importa arquivo XML do EndNote
        """
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            references = []
            for record in root.findall('.//record'):
                ref = {
                    'authors': [],
                    'year': '',
                    'title': '',
                    'journal': '',
                    'keywords': []
                }
                
                # Extrair dados básicos
                authors = record.findall('.//author')
                ref['authors'] = [author.text for author in authors if author.text]
                
                year = record.find('.//year')
                ref['year'] = year.text if year is not None else ''
                
                title = record.find('.//title')
                ref['title'] = title.text if title is not None else ''
                
                journal = record.find('.//secondary-title')
                ref['journal'] = journal.text if journal is not None else ''
                
                keywords = record.findall('.//keyword')
                ref['keywords'] = [kw.text for kw in keywords if kw.text]
                
                references.append(ref)
            
            # Converter para DataFrame
            df = pd.DataFrame(references)
            
            # Salvar em CSV
            output_file = os.path.join(self.data_dir, 'imported_references.csv')
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            self.log_activity(f"Importados {len(references)} referências de {xml_file}")
            return df
            
        except Exception as e:
            self.log_activity(f"Erro ao importar {xml_file}: {str(e)}")
            raise
    
    def remove_duplicates(self, df, columns=['title']):
        """
        Remove duplicatas baseado em colunas específicas
        """
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=columns)
        removed_count = initial_count - len(df_clean)
        
        self.log_activity(f"Removidas {removed_count} duplicatas")
        return df_clean
    
    def generate_report(self):
        """
        Gera relatório de estatísticas
        """
        try:
            df = pd.read_csv(os.path.join(self.data_dir, 'imported_references.csv'))
            
            report = [
                "Relatório de Referências",
                "=" * 50,
                f"Total de referências: {len(df)}",
                f"Anos cobertos: {df['year'].min()} - {df['year'].max()}",
                f"Journals únicos: {df['journal'].nunique()}",
                "\nTop 5 Journals:",
                df['journal'].value_counts().head().to_string(),
                "\nDistribuição por ano:",
                df['year'].value_counts().sort_index().to_string()
            ]
            
            report_file = os.path.join(self.output_dir, 'reference_report.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report))
                
            self.log_activity("Relatório gerado com sucesso")
            
        except Exception as e:
            self.log_activity(f"Erro ao gerar relatório: {str(e)}")
            raise

def main():
    # Exemplo de uso
    project_dir = r"C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis"
    manager = ReferenceManager(project_dir)
    
    print("Reference Manager inicializado com sucesso!")
    print(f"Diretório do projeto: {project_dir}")
    print("Use as funções da classe ReferenceManager para gerenciar suas referências.")

if __name__ == "__main__":
    main()
