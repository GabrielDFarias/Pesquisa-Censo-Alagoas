import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

colunas_interesse = [
    'CO_ENTIDADE', 'NO_MUNICIPIO', 'SG_UF', 'TP_LOCALIZACAO', 'TP_LOCALIZACAO_DIFERENCIADA',
    'IN_AGUA_FONTE_RIO', 'IN_AGUA_INEXISTENTE', 'QT_TRANSP_PUBLICO', 
    'QT_MAT_BAS',     
    'QT_MAT_INF',     
    'QT_MAT_FUND_AI',  
    'QT_MAT_FUND_AF',  
    'QT_MAT_MED',      
    'QT_MAT_EJA'
]

df_bruto = pd.read_csv('microdados_ed_basica_2023.csv', sep=';', encoding='latin1', usecols=colunas_interesse)

df = df_bruto[(df_bruto['SG_UF'] == 'AL') & (df_bruto['TP_LOCALIZACAO'] == 2)].copy()

cols_mat = ['QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND_AI', 'QT_MAT_FUND_AF', 'QT_MAT_MED', 'QT_MAT_EJA', 'QT_TRANSP_PUBLICO']
df[cols_mat] = df[cols_mat].fillna(0)

df = df[df['QT_MAT_BAS'] > 0].copy()

df['taxa_transporte_real'] = (df['QT_TRANSP_PUBLICO'] / df['QT_MAT_BAS']) * 100
df['taxa_transporte_real'] = df['taxa_transporte_real'].clip(upper=100) # Normaliza em 100%

loc_map = {0.0: 'Rural Comum', 1.0: 'Assentamento', 2.0: 'Terra Indígena', 3.0: 'Quilombola'}
df['Tipo_Area'] = df['TP_LOCALIZACAO_DIFERENCIADA'].map(loc_map)

plt.figure(figsize=(10,5))
sns.barplot(x='Tipo_Area', y='taxa_transporte_real', data=df, errorbar=None, palette='Reds_r')
plt.title('Dependência de Transporte por Tipo de Comunidade')
plt.ylabel('Dependência Média (%)')
plt.xlabel('')
plt.grid(axis='y', alpha=0.3)
plt.savefig('1_localizacao_todo.png')


ensino_df = pd.DataFrame({
    'Nível de Ensino': ['Ed. Infantil', 'Fund. Iniciais', 'Fund. Finais', 'Ensino Médio', 'EJA'],
    'Total Matrículas': [
        df['QT_MAT_INF'].sum(), 
        df['QT_MAT_FUND_AI'].sum(), 
        df['QT_MAT_FUND_AF'].sum(), 
        df['QT_MAT_MED'].sum(),
        df['QT_MAT_EJA'].sum()
    ]
})

plt.figure(figsize=(10,6))
ax = sns.barplot(x='Nível de Ensino', y='Total Matrículas', data=ensino_df, palette='magma')
plt.title('Distribuição Total de Alunos no Campo')
for p in ax.patches:
    ax.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontweight='bold')
plt.ylim(0, df['QT_MAT_FUND_AI'].sum() * 1.2)
plt.savefig('2_niveis_ensino_todo.png')

df['escola_sem_agua'] = df['IN_AGUA_FONTE_RIO'] + df['IN_AGUA_INEXISTENTE']

mun_group = df.groupby('NO_MUNICIPIO').agg({
    'taxa_transporte_real': 'mean',
    'escola_sem_agua': 'sum',
    'QT_MAT_FUND_AF': 'sum',
    'QT_MAT_MED': 'sum',
    'CO_ENTIDADE': 'count'
})

mun_group = mun_group[mun_group['CO_ENTIDADE'] >= 3].copy()

mun_group['pct_agua_precaria'] = (mun_group['escola_sem_agua'] / mun_group['CO_ENTIDADE']) * 100

mun_group['deficit_medio'] = 100 - ((mun_group['QT_MAT_MED'] / mun_group['QT_MAT_FUND_AF'].replace(0, np.nan)) * 100).fillna(0).clip(upper=100)

mun_group['score_precariedade'] = mun_group['taxa_transporte_real'] + mun_group['pct_agua_precaria'] + mun_group['deficit_medio']

top_10 = mun_group.sort_values('score_precariedade', ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(y=top_10.index, x=top_10['score_precariedade'], palette='inferno')
plt.title('Top 10 Municípios mais Vulneráveis (Transporte Geral + Água + Queda pro Ensino Médio)')
plt.xlabel('Score de Vulnerabilidade')
plt.ylabel('')
plt.savefig('3_top10_municipios_todo.png')

heat_data = mun_group.sort_values('score_precariedade', ascending=False).head(15)
heat_matrix = pd.DataFrame({
    'Dep. Transporte Geral (%)': heat_data['taxa_transporte_real'],
    'Falta de Água (%)': heat_data['pct_agua_precaria'],
    'Queda pro Ensino Médio (%)': heat_data['deficit_medio']
})

plt.figure(figsize=(10, 8))
sns.heatmap(heat_matrix, annot=True, cmap='YlOrRd', fmt=".1f", linewidths=.5)
plt.title('Heatmap de Precariedade Sistêmica')
plt.ylabel('Município')
plt.savefig('4_heatmap_todo.png')