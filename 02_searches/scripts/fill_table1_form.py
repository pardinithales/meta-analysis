import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox

class StudyEntryForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulário de Entrada de Estudos")
        self.root.geometry("1200x800")
        
        # Lista de estudos
        self.studies = [
            "Sharma 2007",
            "Sinh 2022",
            "Bhattarai 2022",
            "Thang 2022",
            "Arroyo 2019",
            "Carpio A",
            "Ibanez VLDF",
            "Garcia HH 2016 (Clin Infect Dis)",
            "Garcia HH 2014 (Lancet Infect Dis)",
            "Thapa K 2018",
            "Garcia HH 2014 (Epilepsia)",
            "Romo ML 2015",
            "Santhosh AP 2021",
            "Carpio A 2019",
            "Carpio A 2008",
            "Das K 2007",
            "Garcia HH 2004 (N Engl J Med)",
            "Thussu A 2008",
            "de Souza A 2010",
            "Singhi P 2004",
            "Khurana N 2012",
            "Singla M 2011",
            "Chaurasia RN 2010",
            "Prakash S 2006",
            "Kaur P 2010"
        ]
        
        # Dados coletados
        self.data = []
        
        # Abreviações
        self.abbreviations = {}
        
        # Inicializar listas de grupos
        self.treatment_groups = []
        self.control_groups = []
        
        # Criar todos os widgets
        self.create_widgets()
        
        # Vincular atalhos de teclado
        self.bind_shortcuts()
        
    def create_widgets(self):
        # Frame principal com barra de rolagem
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar grid para expandir
        scrollable_frame.columnconfigure(1, weight=1)
        
        # 1. Estudo Selecionado
        ttk.Label(scrollable_frame, text="Estudo:").grid(row=0, column=0, sticky=tk.W, pady=2)
        study_frame = ttk.Frame(scrollable_frame)
        study_frame.grid(row=0, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Autor
        ttk.Label(study_frame, text="Autor:").grid(row=0, column=0, padx=5)
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(study_frame, textvariable=self.author_var, width=20)
        self.author_entry.grid(row=0, column=1, padx=5)
        
        # Ano
        ttk.Label(study_frame, text="Ano:").grid(row=0, column=2, padx=5)
        self.year_var = tk.StringVar()
        self.year_entry = ttk.Entry(study_frame, textvariable=self.year_var, width=10)
        self.year_entry.grid(row=0, column=3, padx=5)
        
        # Design do Estudo
        ttk.Label(study_frame, text="Design:").grid(row=0, column=4, padx=5)
        self.design_var = tk.StringVar()
        self.design_combo = ttk.Combobox(study_frame, textvariable=self.design_var, 
                                       values=["RCT", "Non-RCT"], width=10)
        self.design_combo.grid(row=0, column=5, padx=5)
        
        # Número de Pacientes por Grupo
        patient_frame = ttk.Frame(scrollable_frame)
        patient_frame.grid(row=1, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Frame para grupos de tratamento
        ttk.Label(scrollable_frame, text="Tratamentos:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.treatment_frame = ttk.Frame(scrollable_frame)
        self.treatment_frame.grid(row=1, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Botão para adicionar novo grupo de tratamento
        add_treatment_btn = ttk.Button(self.treatment_frame, text="Adicionar Grupo de Tratamento", 
                                     command=self.add_treatment_group)
        add_treatment_btn.grid(row=0, column=0, pady=5, sticky='w')
        
        # Total de tratamentos
        treatment_total_frame = ttk.Frame(self.treatment_frame)
        treatment_total_frame.grid(row=999, column=0, sticky='ew', pady=5)
        ttk.Label(treatment_total_frame, text="N Total Tratamentos:").grid(row=0, column=0, padx=5)
        self.total_treatment_n_var = tk.StringVar()
        self.total_treatment_entry = ttk.Entry(treatment_total_frame, 
                                             textvariable=self.total_treatment_n_var, 
                                             width=10, state='readonly')
        self.total_treatment_entry.grid(row=0, column=1, padx=5)
        
        # Frame para grupos controle
        ttk.Label(scrollable_frame, text="Controles:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.control_frame = ttk.Frame(scrollable_frame)
        self.control_frame.grid(row=2, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Botão para adicionar novo controle
        add_control_btn = ttk.Button(self.control_frame, text="Adicionar Grupo Controle", 
                                    command=self.add_control_group)
        add_control_btn.grid(row=0, column=0, pady=5, sticky='w')
        
        # Total de controles
        control_total_frame = ttk.Frame(self.control_frame)
        control_total_frame.grid(row=999, column=0, sticky='ew', pady=5)
        ttk.Label(control_total_frame, text="N Total Controles:").grid(row=0, column=0, padx=5)
        self.total_control_n_var = tk.StringVar()
        self.total_control_entry = ttk.Entry(control_total_frame, 
                                           textvariable=self.total_control_n_var, 
                                           width=10, state='readonly')
        self.total_control_entry.grid(row=0, column=1, padx=5)
        
        # Abreviações (apenas uma vez, após os controles)
        ttk.Label(scrollable_frame, text="Abreviações:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.abbreviation_text = tk.Text(scrollable_frame, height=3, width=50)
        self.abbreviation_text.grid(row=3, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Inicializar com um grupo de cada
        self.add_treatment_group()
        self.add_control_group()
        
        # 4. Intervenção - Campos Dinâmicos
        ttk.Label(scrollable_frame, text="Intervenção:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.int_frame = ttk.Frame(scrollable_frame)
        self.int_frame.grid(row=4, column=1, columnspan=2, sticky='nsew', padx=5, pady=5)
        
        # Lista para campos de intervenção
        self.int_fields = []
        
        # Botão para adicionar intervenção
        add_button = ttk.Button(self.int_frame, text="Adicionar Campo de Intervenção", 
                               command=self.add_int_field)
        add_button.grid(row=0, column=0, pady=5, sticky='w')
        
        # 5. Controle - Campos Dinâmicos
        ttk.Label(scrollable_frame, text="Controle:").grid(row=5, column=0, sticky=tk.NW, pady=2)
        self.add_control_field(scrollable_frame)
        
        # 6. Desenho do Estudo
        ttk.Label(scrollable_frame, text="Desenho do Estudo:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.study_design_var = tk.StringVar()
        self.study_design_combo = ttk.Combobox(scrollable_frame, textvariable=self.study_design_var, state="readonly")
        self.study_design_combo['values'] = ["RCT", "Cohort", "Case-Control", "Observacional", "Outros"]
        self.study_design_combo.grid(row=6, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.study_design_combo.set("RCT")  # Definir como padrão
        
        # 7. Follow-Up
        ttk.Label(scrollable_frame, text="Follow-Up:").grid(row=7, column=0, sticky=tk.W, pady=2)
        followup_frame = ttk.Frame(scrollable_frame)
        followup_frame.grid(row=7, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        self.followup_number_var = tk.StringVar()
        self.followup_number_entry = ttk.Entry(followup_frame, textvariable=self.followup_number_var, width=10)
        self.followup_number_entry.grid(row=0, column=0, padx=5)
        
        self.followup_unit_var = tk.StringVar()
        self.followup_unit_combo = ttk.Combobox(followup_frame, textvariable=self.followup_unit_var, state="readonly", width=10)
        self.followup_unit_combo['values'] = ["Meses", "Anos"]
        self.followup_unit_combo.grid(row=0, column=1, padx=5)
        self.followup_unit_combo.set("Meses")
        
        self.followup_symbol_var = tk.StringVar()
        self.followup_symbol_combo = ttk.Combobox(followup_frame, textvariable=self.followup_symbol_var, state="readonly", width=5)
        self.followup_symbol_combo['values'] = ["±", "="]
        self.followup_symbol_combo.grid(row=0, column=2, padx=5)
        self.followup_symbol_combo.set("±")
        
        # 8. Número de Pacientes
        ttk.Label(scrollable_frame, text="Número de Pacientes:").grid(row=8, column=0, sticky=tk.NW, pady=2)
        self.add_patient_numbers_field(scrollable_frame)
        
        # 9. Dados Epidemiológicos
        ttk.Label(scrollable_frame, text="Dados Epidemiológicos:").grid(row=9, column=0, sticky=tk.NW, pady=2)
        self.add_epidemiological_field(scrollable_frame)
        
        # 10. Idade
        ttk.Label(scrollable_frame, text="Idade:").grid(row=10, column=0, sticky=tk.NW, pady=2)
        self.add_age_field(scrollable_frame)
        
        # 11. Botões de Ação
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=11, column=1, columnspan=2, sticky=tk.E, pady=20)
        
        self.save_button = ttk.Button(button_frame, text="Salvar Entrada (Ctrl+Enter)", command=self.save_entry)
        self.save_button.grid(row=0, column=0, padx=5)
        
        self.export_button = ttk.Button(button_frame, text="Exportar para Excel (Ctrl+Shift+Enter)", command=self.export_to_excel)
        self.export_button.grid(row=0, column=1, padx=5)
        
        # Inicializar com um campo de intervenção
        self.add_int_field()
        
        # Frame para grupos controle (separando abreviações)
        control_label_frame = ttk.Frame(scrollable_frame)
        control_label_frame.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(control_label_frame, text="Controles:").pack(anchor='w')
        ttk.Label(control_label_frame, text="Abreviações:").pack(anchor='w')
        
        self.control_frame = ttk.Frame(scrollable_frame)
        self.control_frame.grid(row=2, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Lista para armazenar os grupos controle
        self.control_groups = []
        
        # Botão para adicionar novo controle
        add_control_btn = ttk.Button(self.control_frame, text="Adicionar Grupo Controle", 
                                    command=self.add_control_group)
        add_control_btn.grid(row=0, column=0, pady=5, sticky='w')
        
        # Inicializar com um grupo controle
        self.add_control_group()
        
    def add_population_field(self, parent_frame):
        """Adiciona campos dinâmicos para População"""
        self.pop_frame = ttk.Frame(parent_frame)
        self.pop_frame.grid(row=1, column=1, columnspan=2, sticky='ew', pady=2)
        
        add_button = ttk.Button(self.pop_frame, text="Adicionar Campo de População", command=self.add_pop_field)
        add_button.grid(row=0, column=0, pady=5, sticky='w')
        
        self.pop_fields = []
        self.add_pop_field()
        
    def add_pop_field(self):
        """Adiciona um novo campo de População com bindings para Tab e Delete"""
        idx = len(self.pop_fields) + 1
        entry = ttk.Entry(self.pop_frame, width=50)
        entry.grid(row=idx, column=0, padx=5, pady=2, sticky='ew')
        self.pop_fields.append(entry)
        
        # Vincular eventos
        entry.bind("<Tab>", lambda e: self.handle_population_tab(e, entry))
        entry.bind("<Delete>", lambda e: self.handle_population_delete(e, entry))
        entry.bind("<BackSpace>", lambda e: self.handle_population_delete(e, entry))
        
    def handle_population_tab(self, event, current_entry):
        """Gerencia Tab nos campos de população"""
        current_text = current_entry.get().strip()
        if current_text and current_entry == self.pop_fields[-1]:
            self.add_pop_field()
            self.pop_fields[-1].focus_set()
            return "break"
        return None
        
    def handle_population_delete(self, event, current_entry):
        """Gerencia Delete/Backspace nos campos de população"""
        if not current_entry.get().strip() and len(self.pop_fields) > 1:
            # Encontrar o índice do campo atual
            idx = self.pop_fields.index(current_entry)
            
            # Remover o campo
            current_entry.grid_remove()
            self.pop_fields.remove(current_entry)
            
            # Focar no campo anterior se existir
            if idx > 0:
                self.pop_fields[idx-1].focus_set()
            return "break"
        return None
        
    def add_int_field(self):
        """Adiciona novo campo de intervenção com número de pacientes"""
        idx = len(self.int_fields)
        frame = ttk.Frame(self.int_frame)
        frame.grid(row=idx+1, column=0, sticky='ew', pady=2)
        
        # Campo de intervenção
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=0, column=0, padx=5)
        
        # Adicionar trace para atualizar campos dependentes
        entry.bind('<KeyRelease>', lambda e: self.on_intervention_change(e))
        
        # Número de pacientes
        ttk.Label(frame, text="Pacientes:").grid(row=0, column=1, padx=5)
        num_entry = ttk.Entry(frame, width=10)
        num_entry.grid(row=0, column=2, padx=5)
        
        # Porcentagem
        ttk.Label(frame, text="%:").grid(row=0, column=3, padx=5)
        perc_entry = ttk.Entry(frame, width=10)
        perc_entry.grid(row=0, column=4, padx=5)
        
        # Botão remover
        remove_btn = ttk.Button(frame, text="X", width=3,
                    command=lambda: self.remove_field(frame, self.int_fields))
        remove_btn.grid(row=0, column=5, padx=5)
        
        # Adicionar à lista
        field_dict = {
            'frame': frame,
            'intervention': entry,
            'patients': num_entry,
            'percentage': perc_entry,
            'remove_button': remove_btn
        }
        self.int_fields.append(field_dict)
        
        # Vincular eventos
        entry.bind("<Tab>", lambda e: self.handle_intervention_tab(e, field_dict))
        num_entry.bind("<Tab>", lambda e: self.handle_intervention_tab(e, field_dict))
        perc_entry.bind("<Tab>", lambda e: self.handle_intervention_tab(e, field_dict))
        
        entry.bind("<Delete>", lambda e: self.handle_intervention_delete(e, field_dict))
        entry.bind("<BackSpace>", lambda e: self.handle_intervention_delete(e, field_dict))
        
        # Atualizar campos dependentes
        self.update_patient_numbers_fields()
        self.update_age_fields()
        self.update_epidemiological_fields()
        
        return entry
        
    def handle_intervention_tab(self, event, field_dict):
        """Gerencia Tab nos campos de intervenção"""
        # Identificar qual campo disparou o evento
        widget = event.widget
        
        # Se for o campo de porcentagem e tiver conteúdo
        if (widget == field_dict['percentage'] and 
            field_dict['percentage'].get().strip() and 
            field_dict == self.int_fields[-1]):
            # Adicionar novo campo de intervenção
            new_entry = self.add_int_field()
            new_entry.focus_set()
            return "break"
        return None
        
    def handle_intervention_delete(self, event, field_dict):
        """Gerencia Delete/Backspace nos campos de intervenção"""
        if (not field_dict['intervention'].get().strip() and 
            len(self.int_fields) > 1):
            # Encontrar o índice do campo atual
            idx = self.int_fields.index(field_dict)
            
            # Remover o campo
            field_dict['frame'].grid_remove()
            self.int_fields.remove(field_dict)
            
            # Focar no campo anterior se existir
            if idx > 0:
                self.int_fields[idx-1]['intervention'].focus_set()
                
            # Atualizar campos dependentes
            self.update_patient_numbers_fields()
            self.update_age_fields()
            self.update_epidemiological_fields()
            return "break"
        return None
        
    def remove_field(self, frame, field_list):
        """Remove um campo específico"""
        frame.destroy()
        for idx, field in enumerate(field_list):
            if field['frame'] == frame:
                field_list.pop(idx)
                break
        # Atualizar campos dependentes
        self.update_patient_numbers_fields()
        self.update_age_fields()
        self.update_epidemiological_fields()
        
    def on_intervention_change(self, event=None):
        """Atualiza campos dependentes quando a intervenção muda"""
        self.update_patient_numbers_fields()
        self.update_age_fields()
        self.update_epidemiological_fields()
        
    def add_control_field(self, parent_frame):
        """Adiciona campos dinâmicos para Controle"""
        self.control_frame = ttk.Frame(parent_frame)
        self.control_frame.grid(row=5, column=1, columnspan=2, sticky='ew', pady=2)
        
        add_button = ttk.Button(self.control_frame, text="Adicionar Campo de Controle", 
                               command=self.add_control_field_entry)
        add_button.grid(row=0, column=0, pady=5, sticky='w')
        
        self.control_fields = []
        self.add_control_field_entry()
        
    def add_control_field_entry(self):
        """Adiciona um novo campo de Controle"""
        idx = len(self.control_fields) + 1
        entry = ttk.Entry(self.control_frame, width=50)
        entry.grid(row=idx, column=0, padx=5, pady=2, sticky='ew')
        self.control_fields.append(entry)
        
        # Vincular eventos
        entry.bind("<Tab>", lambda e: self.handle_control_tab(e, entry))
        entry.bind("<Delete>", lambda e: self.handle_control_delete(e, entry))
        entry.bind("<BackSpace>", lambda e: self.handle_control_delete(e, entry))
        
    def handle_control_tab(self, event, current_entry):
        """Gerencia Tab nos campos de controle"""
        current_text = current_entry.get().strip()
        if current_text and current_entry == self.control_fields[-1]:
            self.add_control_field_entry()
            self.control_fields[-1].focus_set()
            return "break"
        return None
        
    def handle_control_delete(self, event, current_entry):
        """Gerencia Delete/Backspace nos campos de controle"""
        if not current_entry.get().strip() and len(self.control_fields) > 1:
            # Encontrar o índice do campo atual
            idx = self.control_fields.index(current_entry)
            
            # Remover o campo
            current_entry.grid_remove()
            self.control_fields.remove(current_entry)
            
            # Focar no campo anterior se existir
            if idx > 0:
                self.control_fields[idx-1].focus_set()
            return "break"
        return None
        
    def add_patient_numbers_field(self, parent_frame):
        """Adiciona campos para Número de Pacientes"""
        self.patients_frame = ttk.Frame(parent_frame)
        self.patients_frame.grid(row=8, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Labels para Intervenção
        ttk.Label(self.patients_frame, text="Grupo").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(self.patients_frame, text="Número de Pacientes").grid(row=0, column=1, padx=5, pady=2)
        
        self.patient_entries = []
        self.update_patient_numbers_fields()
        
    def update_patient_numbers_fields(self):
        """Atualiza os campos de Número de Pacientes com base nas Intervenções"""
        # Limpar campos existentes
        for widget in self.patients_frame.winfo_children():
            widget.destroy()
        
        # Recriar labels de cabeçalho
        ttk.Label(self.patients_frame, text="Grupo").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(self.patients_frame, text="Número de Pacientes").grid(row=0, column=1, padx=5, pady=2)
        
        self.patient_entries = []
        for i, intervention_dict in enumerate(self.int_fields):
            group = intervention_dict['intervention'].get().strip() if intervention_dict['intervention'].get().strip() else f"Intervenção {i+1}"
            ttk.Label(self.patients_frame, text=group).grid(row=i+1, column=0, padx=5, pady=2)
            
            patient_entry = ttk.Entry(self.patients_frame, width=20)
            patient_entry.grid(row=i+1, column=1, padx=5, pady=2, sticky='ew')
            patient_entry.insert(0, "0")
            
            self.patient_entries.append(patient_entry)
        
    def add_epidemiological_field(self, parent_frame):
        """Adiciona campos para Dados Epidemiológicos"""
        self.epi_frame = ttk.Frame(parent_frame)
        self.epi_frame.grid(row=9, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Label para Female Sex
        ttk.Label(self.epi_frame, text="Sexo Feminino:").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Subdivisão por Intervenção
        self.epi_entries = {}
        for i, intervention_dict in enumerate(self.int_fields):
            inter_text = intervention_dict['intervention'].get().strip() if intervention_dict['intervention'].get().strip() else f"Intervenção {i+1}"
            ttk.Label(self.epi_frame, text=inter_text).grid(row=0, column=i+1, padx=5, pady=2)
            
            # Entrada para cada intervenção
            entry = ttk.Entry(self.epi_frame, width=20)
            entry.grid(row=1, column=i+1, padx=5, pady=2, sticky='ew')
            entry.insert(0, "0 (0.0%)")
            self.epi_entries[inter_text] = entry
        
    def update_epidemiological_fields(self):
        """Atualiza os campos de Dados Epidemiológicos com base nas Intervenções"""
        # Limpar entradas existentes
        for widget in self.epi_frame.winfo_children():
            widget.destroy()
        
        # Label para Female Sex
        ttk.Label(self.epi_frame, text="Sexo Feminino:").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Atualizar labels e entradas
        self.epi_entries = {}
        for i, intervention_dict in enumerate(self.int_fields):
            inter_text = intervention_dict['intervention'].get().strip() if intervention_dict['intervention'].get().strip() else f"Intervenção {i+1}"
            ttk.Label(self.epi_frame, text=inter_text).grid(row=0, column=i+1, padx=5, pady=2)
            
            entry = ttk.Entry(self.epi_frame, width=20)
            entry.grid(row=1, column=i+1, padx=5, pady=2, sticky='ew')
            entry.insert(0, "0 (0.0%)")
            self.epi_entries[inter_text] = entry
        
    def add_age_field(self, parent_frame):
        """Adiciona campos para Idade"""
        self.age_frame = ttk.Frame(parent_frame)
        self.age_frame.grid(row=10, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Labels para Intervenção
        ttk.Label(self.age_frame, text="Grupo").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(self.age_frame, text="Idade").grid(row=0, column=1, padx=5, pady=2)
        
        self.age_entries = []
        self.update_age_fields()
        
    def update_age_fields(self):
        """Atualiza os campos de Idade com base nas Intervenções"""
        # Limpar campos existentes
        for widget in self.age_frame.winfo_children():
            widget.destroy()
        
        # Recriar labels de cabeçalho
        ttk.Label(self.age_frame, text="Grupo").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(self.age_frame, text="Idade").grid(row=0, column=1, padx=5, pady=2)
        
        self.age_entries = []
        for i, intervention_dict in enumerate(self.int_fields):
            group = intervention_dict['intervention'].get().strip() if intervention_dict['intervention'].get().strip() else f"Intervenção {i+1}"
            ttk.Label(self.age_frame, text=group).grid(row=i+1, column=0, padx=5, pady=2)
            
            age_entry = ttk.Entry(self.age_frame, width=30)
            age_entry.grid(row=i+1, column=1, padx=5, pady=2, sticky='ew')
            age_entry.insert(0, "0.0 ± 0.0")
            
            self.age_entries.append(age_entry)
        
    def save_entry(self):
        """Salva a entrada atual nos dados coletados"""
        study = self.study_var.get()
        if not study:
            messagebox.showerror("Erro", "Por favor, selecione um estudo.")
            return
        
        # População
        population_entries = [field.get().strip() for field in self.pop_fields if field.get().strip()]
        if not population_entries:
            messagebox.showerror("Erro", "Por favor, insira pelo menos uma característica de população.")
            return
        population = ", ".join(population_entries)
        
        # Documentação de Abreviações
        abbreviations = self.abbreviation_text.get("1.0", tk.END).strip()
        
        # Intervenção
        intervention_entries = [field['intervention'].get().strip() for field in self.int_fields if field['intervention'].get().strip()]
        if not intervention_entries:
            messagebox.showerror("Erro", "Por favor, insira pelo menos uma intervenção.")
            return
        intervention = ", ".join(intervention_entries)
        
        # Controle
        control_entries = [field.get().strip() for field in self.control_fields if field.get().strip()]
        if not control_entries:
            messagebox.showerror("Erro", "Por favor, insira pelo menos um controle.")
            return
        control = ", ".join(control_entries)
        
        # Desenho do Estudo
        study_design = self.study_design_var.get()
        
        # Follow-Up
        followup_number = self.followup_number_var.get().strip()
        followup_unit = self.followup_unit_var.get().strip()
        followup_symbol = self.followup_symbol_var.get().strip()
        if not followup_number.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um número válido para Follow-Up.")
            return
        followup = f"{followup_number} {followup_unit} {followup_symbol}"
        
        # Número de Pacientes
        patient_numbers = {}
        for idx, entry in enumerate(self.patient_entries):
            num = entry.get().strip()
            if num:
                patient_numbers[f"{intervention_entries[idx]}"] = num
        
        # Dados Epidemiológicos
        epidemiological_data = {}
        for key, entry in self.epi_entries.items():
            epidemiological_data[key] = entry.get().strip()
        
        # Idade
        age_data = {}
        for idx, entry in enumerate(self.age_entries):
            age = entry.get().strip()
            group = intervention_entries[idx] if idx < len(intervention_entries) else f"Grupo {idx+1}"
            age_data[group] = age
        
        # Construir o dicionário de entrada
        entry = {
            'Study': study,
            'Population': population,
            'Abbreviations': abbreviations,
            'Intervention': intervention,
            'Control': control,
            'Study Design': study_design,
            'Follow-Up': followup
        }
        
        # Adicionar Número de Pacientes
        for key, value in patient_numbers.items():
            entry[f'Número de Pacientes - {key}'] = value
        
        # Adicionar Dados Epidemiológicos
        for key, value in epidemiological_data.items():
            entry[f'Dados Epidemiológicos - {key}'] = value
        
        # Adicionar Idade
        for key, value in age_data.items():
            entry[f'Idade - {key}'] = value
        
        # Atualizar ou adicionar entrada
        for i, d in enumerate(self.data):
            if d['Study'] == study:
                self.data[i] = entry
                break
        else:
            self.data.append(entry)
        
        messagebox.showinfo("Sucesso", f"Entrada salva para {study}")
        self.clear_form()
        
    def clear_form(self):
        """Limpa todos os campos do formulário"""
        self.study_var.set('')
        for field in self.pop_fields:
            field.delete(0, tk.END)
        self.abbreviation_text.delete("1.0", tk.END)
        for field in self.int_fields:
            field['intervention'].delete(0, tk.END)
            field['patients'].delete(0, tk.END)
            field['percentage'].delete(0, tk.END)
        for field in self.control_fields:
            field.delete(0, tk.END)
        self.study_design_combo.set("RCT")
        self.followup_number_var.set('')
        self.followup_unit_combo.set("Meses")
        self.followup_symbol_combo.set("±")
        
        # Limpar Número de Pacientes
        for entry in self.patient_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        
        # Limpar Dados Epidemiológicos
        for entry in self.epi_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0 (0.0%)")
        
        # Limpar Idade
        for entry in self.age_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0.0 ± 0.0")
        
        # Focar novamente no Combobox de Estudo
        self.study_combo.focus_set()
        
    def export_to_excel(self):
        """Exporta os dados coletados para um arquivo Excel"""
        if not self.data:
            messagebox.showerror("Erro", "Nenhum dado para exportar.")
            return
        
        df = pd.DataFrame(self.data)
        
        # Criar diretório se não existir
        output_dir = os.path.join('02_searches', 'outputs', 'tables')
        os.makedirs(output_dir, exist_ok=True)
        
        # Exportar para Excel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f'table1_neurocysticercosis_{timestamp}.xlsx')
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Tabela 1', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Tabela 1']
            
            # Formatos
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'align': 'center',
                'border': 1,
                'bg_color': '#F2F2F2'
            })
            
            cell_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'top',
                'border': 1
            })
            
            # Larguras das colunas
            for i, column in enumerate(df.columns):
                max_length = max(df[column].astype(str).map(len).max(), len(column)) + 2
                worksheet.set_column(i, i, max_length)
                worksheet.write(0, i, column, header_format)
            
            # Aplicar formato às células
            for row in range(1, len(df)+1):
                for col in range(len(df.columns)):
                    worksheet.write(row, col, df.iloc[row-1, col], cell_format)
        
        messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
        
    def bind_shortcuts(self):
        """Vincula atalhos de teclado ao aplicativo"""
        # Salvar Entrada com Ctrl+Enter
        self.root.bind('<Control-Return>', lambda event: self.save_entry())
        # Exportar com Ctrl+Shift+Enter
        self.root.bind('<Control-Shift-Return>', lambda event: self.export_to_excel())
        # Salvar com Ctrl+S
        self.root.bind('<Control-s>', lambda event: self.save_entry())
        self.root.bind('<Control-S>', lambda event: self.save_entry())
        # Exportar com Ctrl+E
        self.root.bind('<Control-e>', lambda event: self.export_to_excel())
        self.root.bind('<Control-E>', lambda event: self.export_to_excel())
        
    def validate_entry(self, entry, field_type):
        """Valida entrada do usuário e mostra mensagem de erro apropriada"""
        value = entry.get().strip()
        
        if field_type == "population":
            if not value:
                messagebox.showwarning("Aviso", "Campo de população não pode estar vazio")
                return False
            if len(value) < 3:
                messagebox.showwarning("Aviso", "Descrição da população deve ter pelo menos 3 caracteres")
                return False
                
        elif field_type == "intervention":
            if not value:
                messagebox.showwarning("Aviso", "Campo de intervenção não pode estar vazio")
                return False
            if len(value) < 3:
                messagebox.showwarning("Aviso", "Descrição da intervenção deve ter pelo menos 3 caracteres")
                return False
                
        elif field_type == "patients":
            try:
                num = int(value)
                if num < 0:
                    messagebox.showwarning("Aviso", "Número de pacientes não pode ser negativo")
                    return False
            except ValueError:
                messagebox.showwarning("Aviso", "Número de pacientes deve ser um número inteiro")
                return False
                
        elif field_type == "percentage":
            try:
                num = float(value.replace('%', ''))
                if not 0 <= num <= 100:
                    messagebox.showwarning("Aviso", "Porcentagem deve estar entre 0 e 100")
                    return False
            except ValueError:
                messagebox.showwarning("Aviso", "Formato inválido para porcentagem. Use: XX.X%")
                return False
                
        elif field_type == "age":
            if "±" in value:  # Formato média ± DP
                try:
                    mean, sd = value.split("±")
                    float(mean.strip())
                    float(sd.strip())
                except ValueError:
                    messagebox.showwarning("Aviso", "Formato inválido para idade. Use: XX.X ± XX.X")
                    return False
            else:  # Formato mediana (IQR)
                if not value.strip().startswith("(") or not value.strip().endswith(")"):
                    messagebox.showwarning("Aviso", "Formato inválido para idade. Use: XX.X (XX.X-XX.X)")
                    return False
        
        return True
        
    def add_treatment_group(self):
        """Adiciona um novo grupo de tratamento"""
        idx = len(self.treatment_groups) + 1
        frame = ttk.Frame(self.treatment_frame)
        frame.grid(row=idx, column=0, sticky='ew', pady=2)
        
        # Nome do grupo
        ttk.Label(frame, text=f"Grupo {idx}:").grid(row=0, column=0, padx=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=name_var, width=20)
        name_entry.grid(row=0, column=1, padx=5)
        
        # Número de pacientes
        ttk.Label(frame, text="N:").grid(row=0, column=2, padx=5)
        n_var = tk.StringVar()
        n_entry = ttk.Entry(frame, textvariable=n_var, width=10)
        n_entry.grid(row=0, column=3, padx=5)
        
        # Adicionar à lista de grupos
        group_dict = {
            'frame': frame,
            'name': name_var,
            'name_entry': name_entry,
            'n': n_var,
            'n_entry': n_entry
        }
        self.treatment_groups.append(group_dict)
        
        # Vincular eventos
        n_entry.bind("<Tab>", lambda e: self.handle_treatment_tab(e, group_dict))
        name_entry.bind("<Delete>", lambda e: self.handle_treatment_delete(e, group_dict))
        name_entry.bind("<BackSpace>", lambda e: self.handle_treatment_delete(e, group_dict))
        
        # Vincular atualização do total
        n_var.trace('w', self.update_total_n)

    def handle_treatment_tab(self, event, current_group):
        """Gerencia Tab nos campos de tratamento"""
        if (current_group['n_entry'] == event.widget and 
            current_group['n'].get().strip() and 
            current_group == self.treatment_groups[-1]):
            # Se for o último campo do último grupo e tiver conteúdo
            self.add_treatment_group()
            self.treatment_groups[-1]['name_entry'].focus_set()
            return "break"
        return None

    def handle_treatment_delete(self, event, current_group):
        """Gerencia Delete/Backspace nos campos de tratamento"""
        if (not current_group['name'].get().strip() and 
            len(self.treatment_groups) > 1):
            # Se o campo de nome estiver vazio e houver mais de um grupo
            idx = self.treatment_groups.index(current_group)
            current_group['frame'].destroy()
            self.treatment_groups.remove(current_group)
            
            # Focar no grupo anterior se existir
            if idx > 0:
                self.treatment_groups[idx-1]['name_entry'].focus_set()
            
            self.update_total_n()
            return "break"
        return None

    def update_total_n(self, *args):
        """Atualiza o número total de pacientes"""
        total = 0
        for group in self.treatment_groups:
            try:
                n = int(group['n'].get() or 0)
                total += n
            except ValueError:
                pass
        self.total_n_var.set(str(total))

    def add_control_group(self):
        """Adiciona um novo grupo controle"""
        idx = len(self.control_groups) + 1
        frame = ttk.Frame(self.control_frame)
        frame.grid(row=idx, column=0, sticky='ew', pady=2)
        
        # Nome do controle
        ttk.Label(frame, text=f"Controle {idx}:").grid(row=0, column=0, padx=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, padx=5)
        
        # Número de pacientes
        ttk.Label(frame, text="N:").grid(row=0, column=2, padx=5)
        n_var = tk.StringVar()
        n_entry = ttk.Entry(frame, textvariable=n_var, width=10)
        n_entry.grid(row=0, column=3, padx=5)
        
        # Adicionar ao dicionário
        control_dict = {
            'frame': frame,
            'name': name_var,
            'name_entry': name_entry,
            'n': n_var,
            'n_entry': n_entry
        }
        self.control_groups.append(control_dict)
        
        # Vincular eventos
        n_entry.bind("<Tab>", lambda e: self.handle_control_tab(e, control_dict))
        name_entry.bind("<BackSpace>", lambda e: self.handle_control_delete(e, control_dict))
        
        # Vincular atualização do total
        n_var.trace('w', self.update_total_n)

    def handle_control_tab(self, event, current_group):
        """Gerencia Tab nos campos de controle"""
        if (current_group['n_entry'] == event.widget and 
            current_group['n'].get().strip() and 
            current_group == self.control_groups[-1]):
            # Se for o último campo do último grupo e tiver conteúdo
            self.add_control_group()
            self.control_groups[-1]['name_entry'].focus_set()
            return "break"  # Importante para interromper o comportamento padrão do Tab
        return None

    def handle_control_delete(self, event, current_group):
        """Gerencia Delete/Backspace nos campos de controle"""
        if (not current_group['name'].get().strip() and 
            len(self.control_groups) > 1 and
            current_group['name_entry'] == event.widget):  # Verifica se o evento veio do campo nome
            # Se o campo de nome estiver vazio e houver mais de um grupo
            idx = self.control_groups.index(current_group)
            current_group['frame'].destroy()
            self.control_groups.remove(current_group)
            
            # Focar no grupo anterior se existir
            if idx > 0:
                self.control_groups[idx-1]['name_entry'].focus_set()
            
            self.update_total_n()
            return "break"  # Importante para interromper o comportamento padrão do Backspace
        return None

    def update_total_n(self, *args):
        """Atualiza os números totais de pacientes"""
        # Total tratamentos
        total_treatment = 0
        for group in self.treatment_groups:
            try:
                n = int(group['n'].get() or 0)
                total_treatment += n
            except ValueError:
                pass
        self.total_treatment_n_var.set(str(total_treatment))
        
        # Total controles
        total_control = 0
        for group in self.control_groups:
            try:
                n = int(group['n'].get() or 0)
                total_control += n
            except ValueError:
                pass
        self.total_control_n_var.set(str(total_control))

    @staticmethod
    def main():
        root = tk.Tk()
        app = StudyEntryForm(root)
        root.mainloop()

if __name__ == "__main__":
    StudyEntryForm.main()
