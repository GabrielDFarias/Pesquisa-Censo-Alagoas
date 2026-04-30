import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

colunas = [
    'SG_UF', 'TP_LOCALIZACAO', 
    'IN_AGUA_FONTE_RIO', 'IN_AGUA_INEXISTENTE', 'IN_AGUA_POTAVEL',
    'QT_MAT_FUND_AI', 'QT_MAT_FUND_AF', 'QT_MAT_MED'
]

df_bruto = pd.read_csv('microdados_ed_basica_2023.csv', sep=';', encoding='latin1', usecols=colunas)

df = df_bruto[(df_bruto['SG_UF'] == 'AL') & (df_bruto['TP_LOCALIZACAO'] == 2)].copy()

for col in ['QT_MAT_FUND_AI', 'QT_MAT_FUND_AF', 'QT_MAT_MED']:
    df[col] = df[col].fillna(0)

qtd_inexistente = df['IN_AGUA_INEXISTENTE'].sum()
qtd_rio_fonte = df['IN_AGUA_FONTE_RIO'].sum()
qtd_regular = len(df) - (qtd_inexistente + qtd_rio_fonte)

agua_df = pd.DataFrame({
    'Situação Hídrica': ['Sem Acesso à Água', 'Água de Rio / Fonte', 'Acesso Regular'],
    'Quantidade de Escolas': [qtd_inexistente, qtd_rio_fonte, qtd_regular]
})


plt.figure(figsize=(8, 6))
cores = ['#d62728', '#ff7f0e', '#1f77b4']
ax = sns.barplot(x='Situação Hídrica', y='Quantidade de Escolas', data=agua_df, palette=cores)

plt.title('Condição de Acesso à Água nas Escolas Rurais')
plt.ylabel('Número de Escolas')
plt.xlabel('')

for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.savefig('grafico_agua_escolas.png', bbox_inches='tight')


ensino_df = pd.DataFrame({
    'Nível de Ensino': ['Anos Iniciais\n(1º ao 5º Ano)', 'Anos Finais\n(6º ao 9º Ano)', 'Ensino Médio\n(1º ao 3º Ano)'],
    'Alunos Matriculados': [
        df['QT_MAT_FUND_AI'].sum(), 
        df['QT_MAT_FUND_AF'].sum(), 
        df['QT_MAT_MED'].sum()
    ]
})

plt.figure(figsize=(9, 6))
plt.plot(ensino_df['Nível de Ensino'], ensino_df['Alunos Matriculados'], 
         color='darkred', marker='o', markersize=12, linewidth=4)
plt.fill_between(ensino_df['Nível de Ensino'], ensino_df['Alunos Matriculados'], color='red', alpha=0.1)

plt.title('Queda de Matrículas até o Ensino Médio', fontsize=14)
plt.ylabel('Total de Alunos Matriculados')
plt.grid(axis='y', linestyle='--', alpha=0.5)

for i, valor in enumerate(ensino_df['Alunos Matriculados']):
    plt.text(i, valor + 2000, f'{int(valor):,}', ha='center', fontweight='bold', fontsize=12)

plt.savefig('grafico_queda_medio.png', bbox_inches='tight')
