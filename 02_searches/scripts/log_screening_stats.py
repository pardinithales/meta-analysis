def show_cochrane_stats():
    """Mostra estatísticas do screening da Cochrane"""
    print("\n=== Estatísticas do Screening Cochrane ===")
    print(f"Total de artigos encontrados: 24")
    print("\nResultados do screening:")
    print("- Incluídos: 2")
    print("- Excluídos: 22")
    print("\nMotivos de exclusão:")
    print("- Estudos em andamento/protocolos: 6")
    print("- Estudos observacionais sem comparador: 3")
    print("- População pediátrica: 2")
    print("- Outras condições/intervenções: 11")

if __name__ == "__main__":
    show_cochrane_stats() 