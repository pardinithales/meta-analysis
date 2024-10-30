# -*- coding: utf-8 -*-

# Lista de bases de dados e suas URLs
DATABASES = {
    'PubMed': 'https://pubmed.ncbi.nlm.nih.gov/',
    'Scopus': 'https://www.scopus.com/',
    'Web of Science': 'https://www.webofscience.com/',
    'LILACS': 'https://lilacs.bvsalud.org/',
    'Embase': 'https://www.embase.com/'
}

# Termos de busca estruturados
SEARCH_TERMS = {
    'Disease': [
        'neurocysticercosis',
        'neurocisticercose',
        'Taenia solium',
        'brain cysticercosis'
    ],
    'Treatment': [
        'albendazole',
        'praziquantel',
        'antiparasitic',
        'treatment',
        'therapy'
    ],
    'Study Type': [
        'randomized',
        'trial',
        'clinical trial',
        'controlled'
    ]
}

# Strings de busca pré-formatadas para cada base
SEARCH_STRINGS = {
    'PubMed': '(neurocysticercosis OR "Taenia solium" OR "brain cysticercosis") AND (albendazole OR praziquantel OR antiparasitic OR treatment OR therapy)',
    'Scopus': 'TITLE-ABS-KEY(neurocysticercosis OR "Taenia solium") AND (albendazole OR praziquantel)',
    'Web of Science': 'TS=(neurocysticercosis AND (albendazole OR praziquantel OR treatment))',
    'LILACS': 'neurocysticercosis [Words] and (albendazole OR praziquantel) [Words]',
    'Embase': 'neurocysticercosis:ti,ab,kw AND (albendazole:ti,ab,kw OR praziquantel:ti,ab,kw)'
}

# Critérios de inclusão simplificados
INCLUSION_CRITERIA = [
    '1. Estudo em humanos',
    '2. Neurocisticercose parenquimatosa',
    '3. Tratamento com albendazol e/ou praziquantel',
    '4. Relata desfechos de interesse (mortalidade/cura/crises)',
    '5. Artigo completo disponível'
]

# Checklist rápido para triagem
SCREENING_QUESTIONS = [
    'É um estudo em humanos?',
    'Aborda neurocisticercose parenquimatosa?',
    'Usa albendazol e/ou praziquantel?',
    'Reporta desfechos de interesse?',
    'Artigo completo disponível?'
]

def print_search_help():
    print("\nGuia Rápido de Busca Sistemática")
    print("=" * 50)
    
    print("\n1. Bases de Dados:")
    for db, url in DATABASES.items():
        print(f"   - {db}: {url}")
    
    print("\n2. Strings de Busca:")
    for db, string in SEARCH_STRINGS.items():
        print(f"\n{db}:")
        print(f"   {string}")
    
    print("\n3. Critérios de Inclusão:")
    for criterion in INCLUSION_CRITERIA:
        print(f"   {criterion}")

if __name__ == "__main__":
    print_search_help()
