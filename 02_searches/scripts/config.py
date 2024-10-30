# -*- coding: utf-8 -*-

# Configurações para integração com EndNote
ENDNOTE_SETTINGS = {
    'export_path': r'C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis\02_searches\data\endnote_exports',
    'file_types': ['.xml', '.ris'],
    'default_encoding': 'utf-8'
}

# Campos expandidos para meta-análise
REFERENCE_FIELDS = [
    'authors',
    'year',
    'title',
    'journal',
    'abstract',
    'keywords',
    'doi',
    'type_of_study',      # RCT, observacional, etc.
    'intervention_type',   # Albendazol, Praziquantel, Combinado
    'sample_size',        # Número de participantes
    'follow_up_time',     # Tempo de seguimento
    'outcomes',           # Desfechos reportados
    'quality_score',      # Pontuação de qualidade
    'inclusion_status'    # Incluído, Excluído, Pendente
]

# Critérios de classificação PICO
PICO_CRITERIA = {
    'population': 'Pacientes adultos com neurocisticercose parenquimatosa confirmada',
    'intervention': ['Albendazol', 'Praziquantel', 'Terapia combinada'],
    'comparison': ['Placebo', 'Nenhum tratamento', 'Comparação entre regimes'],
    'outcomes': ['Mortalidade', 'Resolução completa das lesões', 'Redução de crises epilépticas']
}
