def generate_bvs_query():
    """Gera query simplificada para BVS/LILACS"""
    
    # Termos principais sem campos específicos
    disease_terms = (
        '(neurocysticercosis OR neurocisticercose OR '
        '"taenia solium")'
    )
    
    # Termos de tratamento
    treatment_terms = (
        '(albendazole OR albendazol OR praziquantel)'
    )
    
    # Query básica
    basic_query = f"{disease_terms} AND {treatment_terms}"
    
    print("\n=== Query BVS/LILACS (Simplificada) ===")
    print("\nQuery para copiar:")
    print(basic_query)
    
    print("\nInstruções:")
    print("1. Acesse: https://bvsalud.org/")
    print("2. Cole a query")
    print("3. Aplique os filtros:")
    print("   - Base de dados: LILACS")
    print("   - Tipo de estudo: Ensaio Clínico")
    print("   - Idioma: Português, Espanhol, Inglês")

if __name__ == "__main__":
    generate_bvs_query() 