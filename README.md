# Meta-análise: Neurocisticercose

## Rastreamento de Artigos (PRISMA)

### Estrutura do Projeto

### Como Atualizar os Números PRISMA

1. **Ver Estatísticas Atuais**

powershell
Navegar até a pasta do projeto
cd "C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis"
Ver estatísticas
python "02_searches\scripts\track_selection_numbers.py"

Selecione opção 1
powershell
Navegar até a pasta do projeto
cd "C:\Users\fagun\OneDrive\Desktop\meta-analysis_neurocisticercosis"
Adicionar nova etapa
python "02_searches\scripts\track_selection_numbers.py"

2. **Adicionar nova etapa**

Selecione opção 2
Siga as instruções para adicionar:
- Nome da etapa (ex: "Após screening de títulos")
- Número de artigos
- Observação


python "02_searches\scripts\track_selection_numbers.py"
Opção: 2
Etapa: "Após screening de títulos"
Número: [número de artigos restantes]
Observação: "Excluídos X artigos após leitura de títulos"
powershell
python "02_searches\scripts\track_selection_numbers.py"

Opção: 2
Etapa: "Após screening de resumos"
Número: [número de artigos restantes]
Observação: "Excluídos X artigos após leitura de resumos"
powershell
python "02_searches\scripts\track_selection_numbers.py"
Opção: 2
Etapa: "Após leitura completa"
Número: [número de artigos incluídos]
Observação: "Excluídos X artigos após leitura completa"

### Notas Importantes

1. Execute o script sempre da pasta raiz do projeto
2. Mantenha o arquivo `screening_database.xlsx` atualizado
3. Cada etapa será registrada com data automática
4. Os números são cumulativos e serão usados para o fluxograma PRISMA