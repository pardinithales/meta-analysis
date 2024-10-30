import pandas as pd
from datetime import datetime

def continue_screening():
    """Continua o screening de onde parou"""
    
    print("🔍 Iniciando screening...\n")
    
    # Carregar banco de dados
    df = pd.read_excel("02_searches/data/screening_database.xlsx")
    
    # Encontrar artigos pendentes (sem decisão)
    pending = df[df['Decisão'].isna()].copy()
    
    if len(pending) == 0:
        print("✅ Todos os artigos já foram revisados!")
        return
    
    print(f"📊 {len(pending)} artigos pendentes para revisar\n")
    
    # Iniciar screening
    i = 0
    while i < len(pending):
        idx = pending.index[i]
        row = pending.iloc[i]
        
        print(f"\n{'='*80}\n")
        print(f"Artigo {i+1} de {len(pending)}")
        print(f"Base: {row['Base']}")
        print(f"\nTítulo: {row['Título']}")
        print(f"Autores: {row['Autores']}")
        print(f"Ano: {row['Ano']}")
        print(f"\nAbstract: {row['Abstract']}\n")
        
        # Solicitar decisão
        while True:
            decisao = input("\nIncluir artigo? (s/n/p para pausar): ").lower()
            if decisao in ['s', 'n', 'p']:
                break
        
        if decisao == 'p':
            print("\n⏸️ Screening pausado. Progresso salvo.")
            break
            
        df.at[idx, 'Decisão'] = 'Incluído' if decisao == 's' else 'Excluído'
        
        if decisao == 'n':
            motivo = input("Motivo da exclusão (v para voltar): ")
            if motivo.lower() == 'v':
                df.at[idx, 'Decisão'] = None
                continue
            df.at[idx, 'Motivo_Exclusão'] = motivo
        
        # Salvar progresso
        df.to_excel("02_searches/data/screening_database.xlsx", index=False)
        print("✅ Progresso salvo")
        
        i += 1

if __name__ == "__main__":
    continue_screening() 