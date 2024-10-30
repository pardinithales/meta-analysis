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
        
        # Criar todos os widgets
        self.create_widgets()
        
        # Vincular atalhos de teclado
        self.bind_shortcuts()
        
    def create_widgets(self):
        # Frame principal com barra de rolagem
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas e Scrollbar com cor de fundo correta
        canvas = tk.Canvas(main_frame, bg=self.root.cget('bg'))  # Mesma cor do fundo
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        # Configurar rolagem
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Criar janela no canvas com largura adequada
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1150)  # Largura fixa
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack do canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar cores e estilos
        style = ttk.Style()
        style.configure('TFrame', background=self.root.cget('bg'))
        canvas.configure(highlightthickness=0)  # Remove a borda do canvas
        
        # Configurar grid para expandir
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Definir linha atual
        self.current_row = 0
        
        # 1. Informações do Estudo
        ttk.Label(scrollable_frame, text="Informações do Estudo", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Study_ID (Seleção do Estudo)
        ttk.Label(scrollable_frame, text="Study_ID:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.study_var = tk.StringVar()
        self.study_combo = ttk.Combobox(scrollable_frame, 
                                        textvariable=self.study_var,
                                        values=self.studies,
                                        width=40,
                                        state="readonly")
        self.study_combo.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.study_combo.bind('<<ComboboxSelected>>', self.on_study_select)
        self.current_row += 1
        
        # First_Author
        ttk.Label(scrollable_frame, text="First Author:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(scrollable_frame, textvariable=self.author_var, width=40)
        self.author_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Year
        ttk.Label(scrollable_frame, text="Year:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.year_var = tk.StringVar()
        self.year_entry = ttk.Entry(scrollable_frame, textvariable=self.year_var, width=40)
        self.year_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Country
        ttk.Label(scrollable_frame, text="Country:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.country_var = tk.StringVar()
        self.country_entry = ttk.Entry(scrollable_frame, textvariable=self.country_var, width=40)
        self.country_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Study Design
        ttk.Label(scrollable_frame, text="Study Design:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.design_var = tk.StringVar()
        self.design_combo = ttk.Combobox(scrollable_frame, textvariable=self.design_var, 
                                         values=["RCT", "Non-RCT", "Case-Control", "Cohort", "Cross-sectional"],
                                         width=37, state="readonly")
        self.design_combo.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Risk of Bias
        ttk.Label(scrollable_frame, text="Risk of Bias:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.risk_bias_var = tk.StringVar()
        self.risk_bias_combo = ttk.Combobox(scrollable_frame, textvariable=self.risk_bias_var, 
                                            values=["Low", "Moderate", "High", "Unclear"],
                                            width=37, state="readonly")
        self.risk_bias_combo.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row +=1
        
        # Diagnostic Criteria
        ttk.Label(scrollable_frame, text="Diagnostic Criteria:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.diagnostic_var = tk.StringVar()
        self.diagnostic_entry = ttk.Entry(scrollable_frame, textvariable=self.diagnostic_var, width=40)
        self.diagnostic_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row +=1
        
        # 2. População
        ttk.Label(scrollable_frame, text="População", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Total Sample Size
        ttk.Label(scrollable_frame, text="Total Sample Size:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.total_sample_var = tk.StringVar()
        self.total_sample_entry = ttk.Entry(scrollable_frame, textvariable=self.total_sample_var, width=40)
        self.total_sample_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Treatment Group N
        ttk.Label(scrollable_frame, text="Treatment Group N:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.treatment_n_var = tk.StringVar()
        self.treatment_n_entry = ttk.Entry(scrollable_frame, textvariable=self.treatment_n_var, width=40)
        self.treatment_n_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Control Group N
        ttk.Label(scrollable_frame, text="Control Group N:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.control_n_var = tk.StringVar()
        self.control_n_entry = ttk.Entry(scrollable_frame, textvariable=self.control_n_var, width=40)
        self.control_n_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Age Mean ± SD
        ttk.Label(scrollable_frame, text="Age Mean ± SD:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.age_mean_sd_var = tk.StringVar()
        self.age_mean_sd_entry = ttk.Entry(scrollable_frame, textvariable=self.age_mean_sd_var, width=40)
        self.age_mean_sd_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Male Percentage
        ttk.Label(scrollable_frame, text="Male Percentage (%):").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.male_perc_var = tk.StringVar()
        self.male_perc_entry = ttk.Entry(scrollable_frame, textvariable=self.male_perc_var, width=40)
        self.male_perc_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Female Percentage
        ttk.Label(scrollable_frame, text="Female Percentage (%):").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.female_perc_var = tk.StringVar()
        self.female_perc_entry = ttk.Entry(scrollable_frame, textvariable=self.female_perc_var, width=40)
        self.female_perc_entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # 3. Características Clínicas
        ttk.Label(scrollable_frame, text="Características Clínicas", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Criar campos para cada característica clínica
        self.create_clinical_fields(scrollable_frame)
        
        # 4. Detalhes do Tratamento
        ttk.Label(scrollable_frame, text="Detalhes do Tratamento", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Criar campos para detalhes do tratamento
        self.create_treatment_fields(scrollable_frame)
        
        # 5. Follow-up e Resultados
        ttk.Label(scrollable_frame, text="Follow-up e Resultados", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Criar campos para follow-up e resultados
        self.create_followup_fields(scrollable_frame)
        
        # 6. Parâmetros Laboratoriais
        ttk.Label(scrollable_frame, text="Parâmetros Laboratoriais", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Criar campos para parâmetros laboratoriais
        self.create_laboratory_fields(scrollable_frame)
        
        # 7. Eventos Adversos
        ttk.Label(scrollable_frame, text="Eventos Adversos", font=('Helvetica', 16, 'bold')).grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=10)
        self.current_row += 1
        
        # Criar campos para eventos adversos
        self.create_adverse_events_fields(scrollable_frame)
        
        # 8. Notas
        ttk.Label(scrollable_frame, text="Comentários:").grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
        self.comments_text = tk.Text(scrollable_frame, height=4, width=50)
        self.comments_text.grid(row=self.current_row, column=1, sticky='ew', pady=2)
        self.current_row += 1
        
        # Botões de Ação
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=self.current_row, column=0, columnspan=2, sticky=tk.E, pady=20)
        
        self.save_button = ttk.Button(button_frame, text="Salvar Entrada (Ctrl+Enter)", command=self.save_entry)
        self.save_button.grid(row=0, column=0, padx=5)
        
        self.export_button = ttk.Button(button_frame, text="Exportar para Excel (Ctrl+Shift+Enter)", command=self.export_to_excel)
        self.export_button.grid(row=0, column=1, padx=5)
        
    def create_clinical_fields(self, frame):
        # Lista de campos clínicos
        clinical_fields = [
            ('Single Lesion N:', 'single_lesion_n_var'),
            ('Multiple Lesions N:', 'multiple_lesions_n_var'),
            ('Lesions Mean Number:', 'lesions_mean_number_var'),
            ('Parenchymal Location %:', 'parenchymal_location_perc_var'),
            ('Extraparenchymal %:', 'extraparenchymal_perc_var'),
            ('Active Cysts %:', 'active_cysts_perc_var'),
            ('Calcified Lesions %:', 'calcified_lesions_perc_var'),
            ('Focal Seizures %:', 'focal_seizures_perc_var'),
            ('Generalized Seizures %:', 'generalized_seizures_perc_var'),
            ('Headache %:', 'headache_perc_var'),
            ('Other Symptoms:', 'other_symptoms_var')
        ]
        
        for label_text, var_name in clinical_fields:
            ttk.Label(frame, text=label_text).grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
            setattr(self, var_name, tk.StringVar())
            entry = ttk.Entry(frame, textvariable=getattr(self, var_name), width=40)
            entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
            self.current_row += 1
    
    def create_treatment_fields(self, frame):
        # Lista de campos de tratamento
        treatment_fields = [
            ('Treatment Type:', 'treatment_type_var', ['Albendazole', 'Praziquantel', 'Combined', 'Placebo']),
            ('Albendazole Dose:', 'albendazole_dose_var'),
            ('Praziquantel Dose:', 'praziquantel_dose_var'),
            ('Treatment Duration (Days):', 'treatment_duration_var'),
            ('Number of Cycles:', 'number_of_cycles_var'),
            ('Cycle Interval (Days):', 'cycle_interval_var'),
            ('Corticosteroid Type:', 'corticosteroid_type_var'),
            ('Corticosteroid Dose:', 'corticosteroid_dose_var'),
            ('Corticosteroid Duration:', 'corticosteroid_duration_var'),
            ('Antiepileptic Drug:', 'antiepileptic_drug_var'),
            ('AED Dose:', 'aed_dose_var')
        ]
        
        for item in treatment_fields:
            label_text = item[0]
            var_name = item[1]
            ttk.Label(frame, text=label_text).grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
            setattr(self, var_name, tk.StringVar())
            if len(item) == 3:
                # Combobox
                entry = ttk.Combobox(frame, textvariable=getattr(self, var_name), 
                                     values=item[2], width=37, state="readonly")
            else:
                # Entry
                entry = ttk.Entry(frame, textvariable=getattr(self, var_name), width=40)
            entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
            self.current_row += 1
    
    def create_followup_fields(self, frame):
        # Lista de campos de follow-up
        followup_fields = [
            ('Follow-up Duration (Months):', 'followup_duration_var'),
            ('Lost to Follow-up N:', 'lost_to_followup_n_var'),
            ('Imaging Schedule:', 'imaging_schedule_var'),
            ('Complete Resolution %:', 'complete_resolution_perc_var'),
            ('Partial Resolution %:', 'partial_resolution_perc_var'),
            ('No Change %:', 'no_change_perc_var'),
            ('Calcification Rate %:', 'calcification_rate_perc_var'),
            ('Seizure Free %:', 'seizure_free_perc_var'),
            ('Seizure Reduction %:', 'seizure_reduction_perc_var')
        ]
        
        for label_text, var_name in followup_fields:
            ttk.Label(frame, text=label_text).grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
            setattr(self, var_name, tk.StringVar())
            entry = ttk.Entry(frame, textvariable=getattr(self, var_name), width=40)
            entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
            self.current_row += 1
    
    def create_laboratory_fields(self, frame):
        # Lista de campos laboratoriais
        lab_fields = [
            ('EITB Positive %:', 'eitb_positive_perc_var'),
            ('ELISA Positive %:', 'elisa_positive_perc_var'),
            ('CSF Analysis:', 'csf_analysis_var'),
            ('Elevated Liver Enzymes %:', 'elevated_liver_enzymes_perc_var')
        ]
        
        for label_text, var_name in lab_fields:
            ttk.Label(frame, text=label_text).grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
            setattr(self, var_name, tk.StringVar())
            entry = ttk.Entry(frame, textvariable=getattr(self, var_name), width=40)
            entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
            self.current_row += 1
    
    def create_adverse_events_fields(self, frame):
        # Lista de campos de eventos adversos
        ae_fields = [
            ('Total AE N:', 'total_ae_n_var'),
            ('Headache AE %:', 'headache_ae_perc_var'),
            ('Seizures AE %:', 'seizures_ae_perc_var'),
            ('Gastrointestinal AE %:', 'gastrointestinal_ae_perc_var'),
            ('Other AE:', 'other_ae_var')
        ]
        
        for label_text, var_name in ae_fields:
            ttk.Label(frame, text=label_text).grid(row=self.current_row, column=0, sticky=tk.W, pady=2)
            setattr(self, var_name, tk.StringVar())
            entry = ttk.Entry(frame, textvariable=getattr(self, var_name), width=40)
            entry.grid(row=self.current_row, column=1, sticky='ew', pady=2)
            self.current_row += 1
    
    def save_entry(self):
        """Salva a entrada atual"""
        # Verificar se o Study_ID está selecionado
        study_id = self.study_var.get()
        if not study_id:
            messagebox.showerror("Erro", "Por favor, selecione o Study_ID.")
            return
        
        # Coletar todos os dados
        entry = {
            'Study_ID': study_id,
            'First_Author': self.author_var.get(),
            'Year': self.year_var.get(),
            'Country': self.country_var.get(),
            'Study_Design': self.design_var.get(),
            'Risk_of_Bias': self.risk_bias_var.get(),
            'Diagnostic_Criteria': self.diagnostic_var.get(),
            'Total_Sample_Size': self.total_sample_var.get(),
            'Treatment_Group_N': self.treatment_n_var.get(),
            'Control_Group_N': self.control_n_var.get(),
            'Age_Mean_SD': self.age_mean_sd_var.get(),
            'Male_Percentage': self.male_perc_var.get(),
            'Female_Percentage': self.female_perc_var.get(),
            'Single_Lesion_N': self.single_lesion_n_var.get(),
            'Multiple_Lesions_N': self.multiple_lesions_n_var.get(),
            'Lesions_Mean_Number': self.lesions_mean_number_var.get(),
            'Parenchymal_Location_%': self.parenchymal_location_perc_var.get(),
            'Extraparenchymal_%': self.extraparenchymal_perc_var.get(),
            'Active_Cysts_%': self.active_cysts_perc_var.get(),
            'Calcified_Lesions_%': self.calcified_lesions_perc_var.get(),
            'Focal_Seizures_%': self.focal_seizures_perc_var.get(),
            'Generalized_Seizures_%': self.generalized_seizures_perc_var.get(),
            'Headache_%': self.headache_perc_var.get(),
            'Other_Symptoms': self.other_symptoms_var.get(),
            'Treatment_Type': self.treatment_type_var.get(),
            'Albendazole_Dose': self.albendazole_dose_var.get(),
            'Praziquantel_Dose': self.praziquantel_dose_var.get(),
            'Treatment_Duration_Days': self.treatment_duration_var.get(),
            'Number_of_Cycles': self.number_of_cycles_var.get(),
            'Cycle_Interval_Days': self.cycle_interval_var.get(),
            'Corticosteroid_Type': self.corticosteroid_type_var.get(),
            'Corticosteroid_Dose': self.corticosteroid_dose_var.get(),
            'Corticosteroid_Duration': self.corticosteroid_duration_var.get(),
            'Antiepileptic_Drug': self.antiepileptic_drug_var.get(),
            'AED_Dose': self.aed_dose_var.get(),
            'Follow_up_Duration_Months': self.followup_duration_var.get(),
            'Lost_to_Follow_up_N': self.lost_to_followup_n_var.get(),
            'Imaging_Schedule': self.imaging_schedule_var.get(),
            'Complete_Resolution_%': self.complete_resolution_perc_var.get(),
            'Partial_Resolution_%': self.partial_resolution_perc_var.get(),
            'No_Change_%': self.no_change_perc_var.get(),
            'Calcification_Rate_%': self.calcification_rate_perc_var.get(),
            'Seizure_Free_%': self.seizure_free_perc_var.get(),
            'Seizure_Reduction_%': self.seizure_reduction_perc_var.get(),
            'EITB_Positive_%': self.eitb_positive_perc_var.get(),
            'ELISA_Positive_%': self.elisa_positive_perc_var.get(),
            'CSF_Analysis': self.csf_analysis_var.get(),
            'Elevated_Liver_Enzymes_%': self.elevated_liver_enzymes_perc_var.get(),
            'Total_AE_N': self.total_ae_n_var.get(),
            'Headache_AE_%': self.headache_ae_perc_var.get(),
            'Seizures_AE_%': self.seizures_ae_perc_var.get(),
            'Gastrointestinal_AE_%': self.gastrointestinal_ae_perc_var.get(),
            'Other_AE': self.other_ae_var.get(),
            'Comments': self.comments_text.get("1.0", tk.END).strip()
        }
        
        # Atualizar ou adicionar entrada
        for i, d in enumerate(self.data):
            if d['Study_ID'] == study_id:
                self.data[i] = entry
                break
        else:
            self.data.append(entry)
        
        # Mostrar mensagem de sucesso
        self.root.lift()  # Traz a janela para frente
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!", parent=self.root)
        self.clear_form()
        
    def clear_form(self):
        """Limpa todos os campos do formulário"""
        # Limpar variáveis
        self.study_var.set('')
        self.author_var.set('')
        self.year_var.set('')
        self.country_var.set('')
        self.design_var.set('')
        self.risk_bias_var.set('')
        self.diagnostic_var.set('')
        self.total_sample_var.set('')
        self.treatment_n_var.set('')
        self.control_n_var.set('')
        self.age_mean_sd_var.set('')
        self.male_perc_var.set('')
        self.female_perc_var.set('')
        self.single_lesion_n_var.set('')
        self.multiple_lesions_n_var.set('')
        self.lesions_mean_number_var.set('')
        self.parenchymal_location_perc_var.set('')
        self.extraparenchymal_perc_var.set('')
        self.active_cysts_perc_var.set('')
        self.calcified_lesions_perc_var.set('')
        self.focal_seizures_perc_var.set('')
        self.generalized_seizures_perc_var.set('')
        self.headache_perc_var.set('')
        self.other_symptoms_var.set('')
        self.treatment_type_var.set('')
        self.albendazole_dose_var.set('')
        self.praziquantel_dose_var.set('')
        self.treatment_duration_var.set('')
        self.number_of_cycles_var.set('')
        self.cycle_interval_var.set('')
        self.corticosteroid_type_var.set('')
        self.corticosteroid_dose_var.set('')
        self.corticosteroid_duration_var.set('')
        self.antiepileptic_drug_var.set('')
        self.aed_dose_var.set('')
        self.followup_duration_var.set('')
        self.lost_to_followup_n_var.set('')
        self.imaging_schedule_var.set('')
        self.complete_resolution_perc_var.set('')
        self.partial_resolution_perc_var.set('')
        self.no_change_perc_var.set('')
        self.calcification_rate_perc_var.set('')
        self.seizure_free_perc_var.set('')
        self.seizure_reduction_perc_var.set('')
        self.eitb_positive_perc_var.set('')
        self.elisa_positive_perc_var.set('')
        self.csf_analysis_var.set('')
        self.elevated_liver_enzymes_perc_var.set('')
        self.total_ae_n_var.set('')
        self.headache_ae_perc_var.set('')
        self.seizures_ae_perc_var.set('')
        self.gastrointestinal_ae_perc_var.set('')
        self.other_ae_var.set('')
        self.comments_text.delete("1.0", tk.END)
        
        # Focar novamente no Combobox de Estudo
        self.study_combo.focus_set()
        
    def export_to_excel(self):
        """Exporta os dados para Excel"""
        if not self.data:
            self.root.lift()
            messagebox.showerror("Erro", "Nenhum dado para exportar.", parent=self.root)
            return
        
        # Definir colunas
        columns = [
            # Study Information
            'Study_ID',
            'First_Author',
            'Year',
            'Country',
            'Study_Design',
            'Risk_of_Bias',
            'Diagnostic_Criteria',
            
            # Population
            'Total_Sample_Size',
            'Treatment_Group_N',
            'Control_Group_N',
            'Age_Mean_SD',
            'Male_Percentage',
            'Female_Percentage',
            
            # Clinical Features
            'Single_Lesion_N',
            'Multiple_Lesions_N',
            'Lesions_Mean_Number',
            'Parenchymal_Location_%',
            'Extraparenchymal_%',
            'Active_Cysts_%',
            'Calcified_Lesions_%',
            'Focal_Seizures_%',
            'Generalized_Seizures_%',
            'Headache_%',
            'Other_Symptoms',
            
            # Treatment Details
            'Treatment_Type',
            'Albendazole_Dose',
            'Praziquantel_Dose',
            'Treatment_Duration_Days',
            'Number_of_Cycles',
            'Cycle_Interval_Days',
            'Corticosteroid_Type',
            'Corticosteroid_Dose',
            'Corticosteroid_Duration',
            'Antiepileptic_Drug',
            'AED_Dose',
            
            # Follow-up & Outcomes
            'Follow_up_Duration_Months',
            'Lost_to_Follow_up_N',
            'Imaging_Schedule',
            'Complete_Resolution_%',
            'Partial_Resolution_%',
            'No_Change_%',
            'Calcification_Rate_%',
            'Seizure_Free_%',
            'Seizure_Reduction_%',
            
            # Laboratory Parameters
            'EITB_Positive_%',
            'ELISA_Positive_%',
            'CSF_Analysis',
            'Elevated_Liver_Enzymes_%',
            
            # Adverse Events
            'Total_AE_N',
            'Headache_AE_%',
            'Seizures_AE_%',
            'Gastrointestinal_AE_%',
            'Other_AE',
            
            # Notes
            'Comments'
        ]
        
        df = pd.DataFrame(self.data, columns=columns)
        
        # Criar diretório se não existir
        output_dir = os.path.join('outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        # Exportar para Excel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f'data_extraction_{timestamp}.xlsx')
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data_Extraction', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Data_Extraction']
            
            # Formatos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D9E1F2',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1
            })
            
            # Formatar cabeçalhos
            for col_num, value in enumerate(columns):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 20)
            
            # Adicionar validação de dados
            # Study Design
            worksheet.data_validation('E2:E1000', {
                'validate': 'list',
                'source': ['RCT', 'Non-RCT', 'Case-Control', 'Cohort', 'Cross-sectional']
            })
            
            # Risk of Bias
            worksheet.data_validation('F2:F1000', {
                'validate': 'list',
                'source': ['Low', 'Moderate', 'High', 'Unclear']
            })
            
            # Treatment Type
            worksheet.data_validation('W2:W1000', {
                'validate': 'list',
                'source': ['Albendazole', 'Praziquantel', 'Combined', 'Placebo']
            })
        
        self.root.lift()
        messagebox.showinfo("Sucesso", f"Dados exportados para {filename}", parent=self.root)
        
    def on_study_select(self, event=None):
        """Manipula a seleção de um estudo"""
        selected_study = self.study_var.get()
        
        # Procurar dados existentes para este estudo
        existing_data = None
        for entry in self.data:
            if entry['Study_ID'] == selected_study:
                existing_data = entry
                break
        
        if existing_data:
            # Preencher o formulário com os dados existentes
            self.load_study_data(existing_data)
        else:
            # Limpar o formulário para novo estudo
            self.clear_form()
            self.study_var.set(selected_study)  # Manter o estudo selecionado
    
    def load_study_data(self, data):
        """Carrega os dados do estudo no formulário"""
        self.author_var.set(data.get('First_Author', ''))
        self.year_var.set(data.get('Year', ''))
        self.country_var.set(data.get('Country', ''))
        self.design_var.set(data.get('Study_Design', ''))
        self.risk_bias_var.set(data.get('Risk_of_Bias', ''))
        self.diagnostic_var.set(data.get('Diagnostic_Criteria', ''))
        self.total_sample_var.set(data.get('Total_Sample_Size', ''))
        self.treatment_n_var.set(data.get('Treatment_Group_N', ''))
        self.control_n_var.set(data.get('Control_Group_N', ''))
        self.age_mean_sd_var.set(data.get('Age_Mean_SD', ''))
        self.male_perc_var.set(data.get('Male_Percentage', ''))
        self.female_perc_var.set(data.get('Female_Percentage', ''))
        self.single_lesion_n_var.set(data.get('Single_Lesion_N', ''))
        self.multiple_lesions_n_var.set(data.get('Multiple_Lesions_N', ''))
        self.lesions_mean_number_var.set(data.get('Lesions_Mean_Number', ''))
        self.parenchymal_location_perc_var.set(data.get('Parenchymal_Location_%', ''))
        self.extraparenchymal_perc_var.set(data.get('Extraparenchymal_%', ''))
        self.active_cysts_perc_var.set(data.get('Active_Cysts_%', ''))
        self.calcified_lesions_perc_var.set(data.get('Calcified_Lesions_%', ''))
        self.focal_seizures_perc_var.set(data.get('Focal_Seizures_%', ''))
        self.generalized_seizures_perc_var.set(data.get('Generalized_Seizures_%', ''))
        self.headache_perc_var.set(data.get('Headache_%', ''))
        self.other_symptoms_var.set(data.get('Other_Symptoms', ''))
        self.treatment_type_var.set(data.get('Treatment_Type', ''))
        self.albendazole_dose_var.set(data.get('Albendazole_Dose', ''))
        self.praziquantel_dose_var.set(data.get('Praziquantel_Dose', ''))
        self.treatment_duration_var.set(data.get('Treatment_Duration_Days', ''))
        self.number_of_cycles_var.set(data.get('Number_of_Cycles', ''))
        self.cycle_interval_var.set(data.get('Cycle_Interval_Days', ''))
        self.corticosteroid_type_var.set(data.get('Corticosteroid_Type', ''))
        self.corticosteroid_dose_var.set(data.get('Corticosteroid_Dose', ''))
        self.corticosteroid_duration_var.set(data.get('Corticosteroid_Duration', ''))
        self.antiepileptic_drug_var.set(data.get('Antiepileptic_Drug', ''))
        self.aed_dose_var.set(data.get('AED_Dose', ''))
        self.followup_duration_var.set(data.get('Follow_up_Duration_Months', ''))
        self.lost_to_followup_n_var.set(data.get('Lost_to_Follow_up_N', ''))
        self.imaging_schedule_var.set(data.get('Imaging_Schedule', ''))
        self.complete_resolution_perc_var.set(data.get('Complete_Resolution_%', ''))
        self.partial_resolution_perc_var.set(data.get('Partial_Resolution_%', ''))
        self.no_change_perc_var.set(data.get('No_Change_%', ''))
        self.calcification_rate_perc_var.set(data.get('Calcification_Rate_%', ''))
        self.seizure_free_perc_var.set(data.get('Seizure_Free_%', ''))
        self.seizure_reduction_perc_var.set(data.get('Seizure_Reduction_%', ''))
        self.eitb_positive_perc_var.set(data.get('EITB_Positive_%', ''))
        self.elisa_positive_perc_var.set(data.get('ELISA_Positive_%', ''))
        self.csf_analysis_var.set(data.get('CSF_Analysis', ''))
        self.elevated_liver_enzymes_perc_var.set(data.get('Elevated_Liver_Enzymes_%', ''))
        self.total_ae_n_var.set(data.get('Total_AE_N', ''))
        self.headache_ae_perc_var.set(data.get('Headache_AE_%', ''))
        self.seizures_ae_perc_var.set(data.get('Seizures_AE_%', ''))
        self.gastrointestinal_ae_perc_var.set(data.get('Gastrointestinal_AE_%', ''))
        self.other_ae_var.set(data.get('Other_AE', ''))
        self.comments_text.delete("1.0", tk.END)
        self.comments_text.insert(tk.END, data.get('Comments', ''))
    
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
    
    @staticmethod
    def main():
        root = tk.Tk()
        app = StudyEntryForm(root)
        root.mainloop()

if __name__ == "__main__":
    StudyEntryForm.main()
