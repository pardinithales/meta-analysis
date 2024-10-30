import pandas as pd
from datetime import datetime
import os

def create_table1_template():
    """Cria template para Tabela 1 com estudos incluídos em neurocisticercose"""
    
    # Lista de estudos incluídos
    included_studies = [
        "Sharma 2007",
        "Sinh 2022",
        "Bhattarai 2022",
        "Thang 2022",
        "Arroyo 2019",
        "Carpio A",
        "Ibanez VLDF",
        "Garcia HH 2016 (Clin Infect Dis)",
        "Garcia HH 2014 (Lancet Infect Dis)",
        "Thapa K 2018",
        "Garcia HH 2014 (Epilepsia)",
        "Romo ML 2015",
        "Santhosh AP 2021",
        "Carpio A 2019",
        "Carpio A 2008",
        "Das K 2007",
        "Garcia HH 2004 (N Engl J Med)",
        "Thussu A 2008",
        "de Souza A 2010",
        "Singhi P 2004",
        "Khurana N 2012",
        "Singla M 2011",
        "Chaurasia RN 2010",
        "Prakash S 2006",
        "Kaur P 2010"
    ]
    
    # Criar DataFrame inicial com os estudos
    df = pd.DataFrame({
        'Study': included_studies,
        'Population': '',
        'Intervention': '',
        'Control': '',
        'Primary Outcomes': '',
        'Secondary Outcomes': ''
    })
    
    # Criar diretório de saída se não existir
    output_dir = '02_searches/outputs/tables'
    os.makedirs(output_dir, exist_ok=True)
    
    # Exportar para Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f'table1_neurocysticercosis_{timestamp}.xlsx')
    
    # Configurar o writer do Excel
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Table 1', index=False)
        
        # Obter o workbook e o worksheet
        workbook = writer.book
        worksheet = writer.sheets['Table 1']
        
        # Definir largura das colunas
        column_widths = {
            'Study': 25,
            'Population': 40,
            'Intervention': 30,
            'Control': 25,
            'Primary Outcomes': 35,
            'Secondary Outcomes': 35
        }
        
        for i, (col, width) in enumerate(column_widths.items()):
            worksheet.set_column(i, i, width)
        
        # Adicionar formatos
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'align': 'center',
            'border': 1,
            'bg_color': '#F2F2F2'
        })
        
        cell_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'border': 1
        })
        
        # Aplicar formato ao cabeçalho
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Aplicar formato às células com dados
        for row in range(len(df)):
            for col in range(len(df.columns)):
                worksheet.write(row + 1, col, df.iloc[row, col], cell_format)
    
    print(f"\nTemplate da Tabela 1 criado em: {filename}")
    return filename

if __name__ == "__main__":
    template_file = create_table1_template()
