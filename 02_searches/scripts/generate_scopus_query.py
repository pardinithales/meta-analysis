def generate_scopus_query():
    # Termos principais
    disease_terms = '(neurocysticercosis OR "Taenia solium" OR "brain cysticercosis")'
    treatment_terms = '(albendazole OR praziquantel OR antiparasitic OR treatment OR therapy)'
    
    # Construir query básica
    base_query = f'TITLE-ABS-KEY({disease_terms}) AND TITLE-ABS-KEY({treatment_terms})'
    
    # Query completa com filtros
    # Nota: filtros são aplicados na interface, não na string
    
    print("\n=== Query Scopus ===")
    print("\nQuery para copiar:")
    print(base_query)
    print("\nFiltros para aplicar na interface:")
    print("1. Document type: Article OR Review")
    print("2. Language: English OR Spanish OR Portuguese")
    print("3. Year: All years")
    print("\nInstruções:")
    print("1. Acesse: https://www.scopus.com/")
    print("2. Clique em 'Advanced'")
    print("3. Cole a query no campo de busca")
    print("4. Aplique os filtros manualmente")
    print("5. Exporte os resultados em formato CSV")
    print("6. Salve como: 02_searches/data/scopus_results.csv")

if __name__ == "__main__":
    generate_scopus_query()
