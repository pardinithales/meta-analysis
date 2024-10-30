# -*- coding: utf-8 -*-
import os
from config import ENDNOTE_SETTINGS, REFERENCE_FIELDS, PICO_CRITERIA
import pandas as pd
import xml.etree.ElementTree as ET

def process_reference_details(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        processed_data = []
        
        print(f"\nProcessando arquivo: {os.path.basename(xml_file)}")
        for record in root.findall('.//record'):
            reference = {
                'authors': '',
                'year': '',
                'title': '',
                'journal': '',
                'abstract': '',
                'keywords': '',
                'doi': '',
                'type_of_study': 'Não classificado',
                'intervention_type': 'Não classificado',
                'sample_size': 'Não informado',
                'follow_up_time': 'Não informado',
                'outcomes': 'Não classificado',
                'quality_score': 'Não avaliado',
                'inclusion_status': 'Pendente'
            }
            
            # Dados básicos
            authors = record.findall('.//authors/author')
            reference['authors'] = [author.text for author in authors if author.text]
            
            title = record.find('.//titles/title')
            reference['title'] = title.text if title is not None else ''
            
            year = record.find('.//dates/year')
            reference['year'] = year.text if year is not None else ''
            
            journal = record.find('.//periodical/full-title')
            reference['journal'] = journal.text if journal is not None else ''
            
            keywords = record.findall('.//keywords/keyword')
            reference['keywords'] = [kw.text for kw in keywords if kw.text]
            
            abstract = record.find('.//abstract')
            reference['abstract'] = abstract.text if abstract is not None else ''
            
            doi = record.find('.//electronic-resource-num')
            reference['doi'] = doi.text if doi is not None else ''
            
            processed_data.append(reference)
        
        df = pd.DataFrame(processed_data)
        return df
        
    except Exception as e:
        print(f"Erro ao processar arquivo: {str(e)}")
        return None

def save_processed_data(df, filename="processed_references.csv"):
    try:
        output_path = os.path.join(ENDNOTE_SETTINGS['export_path'], '..', filename)
        
        # Converter listas para strings
        for col in ['authors', 'keywords']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: '; '.join(x) if isinstance(x, list) else x)
        
        # Salvar CSV
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\nDados salvos com sucesso em: {output_path}")
        
        print("\nResumo dos dados:")
        print(f"Total de referências: {len(df)}")
        print(f"Colunas salvas: {', '.join(df.columns)}")
        
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {str(e)}")
        return False

def test_xml_handler():
    print("Teste do processador XML do EndNote")
    print("=================================")
    
    export_dir = ENDNOTE_SETTINGS['export_path']
    print(f"Verificando diretório: {export_dir}")
    
    if os.path.exists(export_dir):
        print("✓ Diretório encontrado")
        xml_files = [f for f in os.listdir(export_dir) if f.endswith('.xml')]
        print(f"\nArquivos XML encontrados: {len(xml_files)}")
        for xml_file in xml_files:
            print(f"  - {xml_file}")
    else:
        print("× Diretório não encontrado")

if __name__ == "__main__":
    test_xml_handler()
    print("\nTestando processamento de referências...")
    
    export_dir = ENDNOTE_SETTINGS['export_path']
    for file in os.listdir(export_dir):
        if file.endswith('.xml'):
            full_path = os.path.join(export_dir, file)
            df = process_reference_details(full_path)
            if df is not None:
                print("\nDados extraídos:")
                print(df)
                save_processed_data(df)
