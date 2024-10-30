import pandas as pd
import os
from datetime import datetime

# Definir caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACKING_FILE = os.path.join(BASE_DIR, "02_searches", "data", "prisma_numbers.xlsx")
SCREENING_FILE = os.path.join(BASE_DIR, "02_searches", "data", "screening_database.xlsx")

def update_prisma_numbers(etapa, numero, observacao):
    """
    Atualiza os números do PRISMA com nova etapa
    """
    if os.path.exists(TRACKING_FILE):
        # Ler dados existentes
        df = pd.read_excel(TRACKING_FILE, sheet_name='Números PRISMA')
        
        # Adicionar nova linha
        nova_linha = pd.DataFrame({
            'Etapa': [etapa],
            'Número': [numero],
            'Data': [datetime.now().strftime('%Y-%m-%d')],
            'Observações': [observacao]
        })
        
        df = pd.concat([df, nova_linha], ignore_index=True)
    else:
        print("Arquivo de tracking não encontrado!")
        return
    
    # Salvar atualização
    with pd.ExcelWriter(TRACKING_FILE) as writer:
        df.to_excel(writer, sheet_name='Números PRISMA', index=False)
        
        # Manter aba de notas
        if 'Notas' in pd.ExcelFile(TRACKING_FILE).sheet_names:
            notas = pd.read_excel(TRACKING_FILE, sheet_name='Notas')
            notas.to_excel(writer, sheet_name='Notas', index=False)
    
    return df

def get_screening_status():
    """
    Lê o arquivo de screening e retorna estatísticas atuais
    """
    if os.path.exists(SCREENING_FILE):
        df = pd.read_excel(SCREENING_FILE)
        stats = {
            'Total': len(df),
            'Incluídos': len(df[df['Decisão'] == 'Incluir']),
            'Excluídos': len(df[df['Decisão'] == 'Excluir']),
            'Pendentes': len(df[df['Decisão'].isna()])
        }
        return stats
    return None

if __name__ == "__main__":
    print("=== Sistema de Tracking PRISMA ===")
    print("\n1. Ver estatísticas atuais")
    print("2. Adicionar nova etapa")
    opcao = input("\nEscolha uma opção (1 ou 2): ")
    
    if opcao == "1":
        stats = get_screening_status()
        if stats:
            print("\nEstatísticas do Screening:")
            for k, v in stats.items():
                print(f"{k}: {v}")
    
    elif opcao == "2":
        etapa = input("Nome da etapa: ")
        numero = int(input("Número de artigos: "))
        obs = input("Observação: ")
        df = update_prisma_numbers(etapa, numero, obs)
        print("\nNúmeros atualizados!")
        print(df)
