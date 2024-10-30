import pandas as pd
from datetime import datetime
from lilacs_helper import load_lilacs_data, save_progress, show_statistics

def screen_lilacs():
    """Realiza screening dos artigos do LILACS"""
    
    print("🔍 Iniciando screening LILACS...\n")
    
    # Carregar banco de dados usando o helper
    df = load_lilacs_data()
    
    # Encontrar artigos pendentes
    pending = df[df['Decisão'].isna()].copy()
    
    if len(pending) == 0:
        print("✅ Todos os artigos já foram revisados!")
        return
    
    print(f"📊 {len(pending)} artigos pendentes para revisar\n")
    show_statistics()
    
    # Iniciar screening
    i = 0
    while i < len(pending):
        idx = pending.index[i]
        row = pending.iloc[i]
        
        print(f"\n{'='*80}\n")
        print(f"Artigo {i+1} de {len(pending)}")
        print(f"Base: {row['Base']}\n")
        print(f"Título: {row['Title']}")
        print(f"Autores: {row['Authors']}")
        print(f"Fonte: {row['Source']}")
        print(f"Ano: {row['Publication year']}")
        print(f"Tipo: {row['Type']}")
        print(f"Idioma: {row['Language']}")
        
        while True:
            decisao = input("\nIncluir artigo? (s/n/p para pausar/v para voltar): ").lower()
            if decisao in ['s', 'n', 'p', 'v']:
                break
        
        if decisao == 'p':
            print("\n⏸️ Screening pausado. Progresso salvo.")
            save_progress(df)
            break
            
        if decisao == 'v':
            if i > 0:
                i -= 1
                continue
            else:
                print("⚠️ Não é possível voltar, este é o primeiro artigo.")
                continue
        
        df.at[idx, 'Decisão'] = 'Incluído' if decisao == 's' else 'Excluído'
        
        if decisao == 'n':
            motivo = input("Motivo da exclusão (v para voltar): ")
            if motivo.lower() == 'v':
                df.at[idx, 'Decisão'] = None
                continue
            df.at[idx, 'Motivo_Exclusão'] = motivo
        
        # Salvar progresso usando o helper
        save_progress(df)
        i += 1

if __name__ == "__main__":
    screen_lilacs() 