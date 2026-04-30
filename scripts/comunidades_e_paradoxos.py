import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

colunas = [
    'CO_ENTIDADE', 'SG_UF', 'TP_LOCALIZACAO', 'TP_LOCALIZACAO_DIFERENCIADA', 'NO_MUNICIPIO',
    'QT_MAT_BAS', 'QT_MAT_EJA', 'QT_TRANSP_PUBLICO', 
    'IN_AGUA_FONTE_RIO', 'IN_AGUA_INEXISTENTE', 'IN_ESGOTO_INEXISTENTE', 
    'IN_INTERNET', 'IN_BIBLIOTECA', 'IN_ENERGIA_INEXISTENTE'
]

df_bruto = pd.read_csv('microdados_ed_basica_2023.csv', sep=';', encoding='latin1', usecols=colunas)

df = df_bruto[(df_bruto['SG_UF'] == 'AL') & (df_bruto['TP_LOCALIZACAO'] == 2)].copy()
df['QT_MAT_BAS'] = df['QT_MAT_BAS'].fillna(0)
df['QT_MAT_EJA'] = df['QT_MAT_EJA'].fillna(0)
df = df[df['QT_MAT_BAS'] > 0]

df['sem_saneamento'] = ((df['IN_ESGOTO_INEXISTENTE'] == 1) | (df['IN_AGUA_INEXISTENTE'] == 1) | (df['IN_AGUA_FONTE_RIO'] == 1)).astype(int)

df['paradoxo_tech'] = ((df['IN_INTERNET'] == 1) & (df['sem_saneamento'] == 1)).astype(int)
qtd_paradoxo = df['paradoxo_tech'].sum()
pct_paradoxo = (qtd_paradoxo / len(df)) * 100

print(f"\n--- O PARADOXO TECNOLÓGICO ---")
print(f"Escolas com Internet mas SEM Saneamento/Água: {qtd_paradoxo} ({pct_paradoxo:.1f}% da rede)")

df['pct_eja'] = (df['QT_MAT_EJA'] / df['QT_MAT_BAS']) * 100

mun_eja = df.groupby('NO_MUNICIPIO').agg({
    'QT_MAT_EJA': 'sum',
    'QT_MAT_BAS': 'sum',
    'CO_ENTIDADE': 'count'
})
mun_eja = mun_eja[mun_eja['CO_ENTIDADE'] >= 3] # Mínimo 3 escolas para ter média justa
mun_eja['taxa_eja_mun'] = (mun_eja['QT_MAT_EJA'] / mun_eja['QT_MAT_BAS']) * 100
top_eja = mun_eja.sort_values('taxa_eja_mun', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(y=top_eja.index, x=top_eja['taxa_eja_mun'], palette='viridis')
plt.title('Top 10 Municípios com Maior Carga de EJA no Campo\n(Indicador de Logística Noturna e Evasão Histórica)')
plt.xlabel('Proporção de Alunos do EJA (%)')
plt.ylabel('')
plt.savefig('tema4_peso_eja.png')


df_tradicional = df[df['TP_LOCALIZACAO_DIFERENCIADA'].isin([2.0, 3.0])].copy()
loc_map = {2.0: 'Terra Indígena', 3.0: 'Quilombola'}
df_tradicional['Comunidade'] = df_tradicional['TP_LOCALIZACAO_DIFERENCIADA'].map(loc_map)


comp_tradicional = df_tradicional.groupby('Comunidade').agg({
    'sem_saneamento': lambda x: (x.sum() / len(x)) * 100,
    'IN_INTERNET': lambda x: ((len(x) - x.sum()) / len(x)) * 100,
    'IN_BIBLIOTECA': lambda x: ((len(x) - x.sum()) / len(x)) * 100 
}).rename(columns={
    'sem_saneamento': '% Sem Saneamento',
    'IN_INTERNET': '% Sem Internet',
    'IN_BIBLIOTECA': '% Sem Biblioteca'
})

comp_tradicional.T.plot(kind='bar', figsize=(10,6), color=['#1f77b4', '#d62728'], width=0.7)
plt.title('Déficit Estrutural: Escolas Indígenas vs. Quilombolas (AL)')
plt.ylabel('Percentual de Escolas Afetadas (%)')
plt.xticks(rotation=0)
plt.legend(title='Tipo de Comunidade')
plt.grid(axis='y', alpha=0.3)
plt.savefig('tema5_comunidades_tradicionais.png')