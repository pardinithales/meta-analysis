# -*- coding: utf-8 -*-
import re
from typing import Dict, List, Optional

class ReferenceClassifier:
    def __init__(self):
        # Padrões para identificar tipos de estudo
        self.study_patterns = {
            'RCT': [r'randomized', r'randomised', r'random\w*\s+allocat\w*', r'double blind', r'placebo\s+controlled'],
            'Observacional': [r'cohort', r'observational', r'case[\s-]control', r'retrospective', r'prospective'],
            'Revisão': [r'systematic\s+review', r'meta[\s-]analysis', r'literature review']
        }
        
        # Padrões para intervenções
        self.intervention_patterns = {
            'Albendazol': [r'albendazole', r'albendazol'],
            'Praziquantel': [r'praziquantel', r'PZQ'],
            'Terapia Combinada': [r'combin\w+\s+therap\w*', r'albendazole\s+and\s+praziquantel']
        }
        
        # Padrões para desfechos
        self.outcome_patterns = {
            'Mortalidade': [r'mortality', r'death', r'survival'],
            'Resolução de Lesões': [r'lesion\s+resolution', r'complete\s+cure', r'radiological\s+improvement'],
            'Crises Epilépticas': [r'seizure', r'epilep\w+', r'convulsion']
        }

    def classify_study_type(self, text: str) -> str:
        """Classifica o tipo de estudo baseado no texto"""
        text = text.lower()
        for study_type, patterns in self.study_patterns.items():
            if any(re.search(pattern, text) for pattern in patterns):
                return study_type
        return 'Não classificado'

    def identify_intervention(self, text: str) -> str:
        """Identifica o tipo de intervenção"""
        text = text.lower()
        interventions = []
        for intervention, patterns in self.intervention_patterns.items():
            if any(re.search(pattern, text) for pattern in patterns):
                interventions.append(intervention)
        return '; '.join(interventions) if interventions else 'Não classificado'

    def extract_sample_size(self, text: str) -> str:
        """Extrai possível tamanho da amostra"""
        patterns = [
            r'n\s*=\s*(\d+)',
            r'(\d+)\s+patients',
            r'(\d+)\s+participants',
            r'sample\s+size\s+of\s+(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        return 'Não informado'

    def identify_outcomes(self, text: str) -> str:
        """Identifica desfechos mencionados"""
        text = text.lower()
        outcomes = []
        for outcome, patterns in self.outcome_patterns.items():
            if any(re.search(pattern, text) for pattern in patterns):
                outcomes.append(outcome)
        return '; '.join(outcomes) if outcomes else 'Não classificado'

    def classify_reference(self, reference: Dict) -> Dict:
        """Classifica uma referência completa"""
        # Combina título e abstract para análise
        text_to_analyze = f"{reference['title']} {reference['abstract']}"
        
        # Atualiza a classificação
        reference['type_of_study'] = self.classify_study_type(text_to_analyze)
        reference['intervention_type'] = self.identify_intervention(text_to_analyze)
        reference['sample_size'] = self.extract_sample_size(text_to_analyze)
        reference['outcomes'] = self.identify_outcomes(text_to_analyze)
        
        return reference
