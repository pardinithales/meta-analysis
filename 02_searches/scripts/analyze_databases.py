import
pandas
as
pd
import
os
"Analisa banco da Cochrane"
try:
try:
df
=
pd.read_csv
02_searches/data/screening_cochrane.csv
except:
df
=
pd.read_excel
02_searches/data/screening_database.xlsx
print
\n=== Análise Banco Cochrane ===
print
\nColunas disponíveis:
print
\nPrimeiras 5 linhas:
return
df
except
Exception
as
e:
return
None
if
__name__
==
__main__
:
