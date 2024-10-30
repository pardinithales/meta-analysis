def generate_cochrane_query():
    """Gera query otimizada para Cochrane Library"""
    
    # Termos MeSH e sinônimos para neurocisticercose
    disease_terms = (
        '(neurocysticercosis OR "brain cysticercosis" OR '
        '"central nervous system cysticercosis" OR '
        '"cerebral cysticercosis" OR "CNS cysticercosis")'
    )
    
    # Termos MeSH para tratamento
    treatment_terms = (
        '(albendazole OR praziquantel OR '
        '"antiparasitic agents" OR anthelmintics)'
    )
    
    # Filtros adicionais
    filters = (
        'AND (human* OR patient*) '
        'NOT (animal* NOT human*)'
    )
    
    # Query completa
    query = f"{disease_terms} AND {treatment_terms} {filters}"
    
    print("\n=== Query Cochrane Library ===")
    print("\nQuery para copiar:")
    print(query)
    
    print("\nInstruções:")
    print("1. Acesse: https://www.cochranelibrary.com/")
    print("2. Clique em 'Advanced search'")
    print("3. Cole a query na caixa de busca")
    print("4. Aplique os filtros:")
    print("   - Trials")
    print("   - Custom Range: All years")
    print("   - Language: English, Spanish, Portuguese")
    print("5. Exporte os resultados em formato CSV")
    print("6. Salve como: 02_searches/data/cochrane_results.csv")
    
    print("\nObservações:")
    print("- A query usa termos MeSH e sinônimos comuns")
    print("- Inclui filtro para estudos em humanos")
    print("- Exclui estudos puramente animais")

if __name__ == "__main__":
    generate_cochrane_query()
