import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

novas_colunas = [
    'SG_UF', 'TP_LOCALIZACAO', 'NO_MUNICIPIO',
    'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND_AI', 'QT_MAT_FUND_AF', 'QT_MAT_MED', 'QT_MAT_EJA',
    'QT_TRANSP_PUBLICO', 'IN_AGUA_INEXISTENTE', 'IN_ENERGIA_INEXISTENTE', 'IN_ESGOTO_INEXISTENTE', 
    'IN_INTERNET', 'IN_BIBLIOTECA'
]

df_bruto = pd.read_csv('microdados_ed_basica_2023.csv', sep=';', encoding='latin1', usecols=novas_colunas)


df = df_bruto[(df_bruto['SG_UF'] == 'AL') & (df_bruto['TP_LOCALIZACAO'] == 2)].copy()
cols_num = ['QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND_AI', 'QT_MAT_FUND_AF', 'QT_MAT_MED', 'QT_MAT_EJA', 'QT_TRANSP_PUBLICO']
df[cols_num] = df[cols_num].fillna(0)
df = df[df['QT_MAT_BAS'] > 0].copy()


df['taxa_transporte_real'] = (df['QT_TRANSP_PUBLICO'] / df['QT_MAT_BAS']) * 100
df['taxa_transporte_real'] = df['taxa_transporte_real'].clip(upper=100)

total_alunos = df['QT_MAT_BAS'].sum()
comp_etaria = pd.DataFrame({
    'Etapa': ['Educação Infantil\n', 'Ensino Fundamental\n', 'Ensino Médio\n', 'EJA\n'],
    'Total': [
        df['QT_MAT_INF'].sum(),
        df['QT_MAT_FUND_AI'].sum() + df['QT_MAT_FUND_AF'].sum(),
        df['QT_MAT_MED'].sum(),
        df['QT_MAT_EJA'].sum()
    ]
})

plt.figure(figsize=(9, 7))
plt.pie(comp_etaria['Total'], labels=comp_etaria['Etapa'], autopct='%1.1f%%', 
        colors=sns.color_palette("Set2"), startangle=140, wedgeprops=dict(width=0.4, edgecolor='w'))
plt.title('Composição do Público Alvo', fontsize=14)
plt.savefig('tema1_composicao_etaria.png')

plt.figure(figsize=(10, 6))

sns.scatterplot(data=df, x='QT_MAT_BAS', y='taxa_transporte_real', alpha=0.5, color='darkmagenta')

sns.regplot(data=df, x='QT_MAT_BAS', y='taxa_transporte_real', scatter=False, color='red', line_kws={"linestyle": "--"})
plt.title('Tamanho da Escola vs. Dependência de Transporte', fontsize=14)
plt.xlabel('Total de Alunos Matriculados')
plt.ylabel('Dependência de Transporte (%)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.savefig('tema2_tamanho_escola.png')


infra = pd.DataFrame({
    'Déficit Estrutural': ['Sem Biblioteca / Sala de Leitura', 'Sem Internet', 'Sem Esgotamento Básico', 'Sem Energia Elétrica'],
    'Quantidade': [
        len(df) - df['IN_BIBLIOTECA'].sum(), 
        len(df) - df['IN_INTERNET'].sum(),   
        df['IN_ESGOTO_INEXISTENTE'].sum(),   
        df['IN_ENERGIA_INEXISTENTE'].sum()   
    ]
})
infra['Percentual (%)'] = (infra['Quantidade'] / len(df)) * 100

plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Percentual (%)', y='Déficit Estrutural', data=infra, palette='Reds_r')
plt.title('Déficit Estrutural Rural', fontsize=14)
plt.xlabel('Percentual da Rede Rural de Alagoas (%)')
plt.ylabel('')
for p in ax.patches:
    ax.annotate(f'{p.get_width():.1f}%', (p.get_width() + 1, p.get_y() + p.get_height()/2), 
                ha='left', va='center', fontweight='bold')
plt.xlim(0, 100)
plt.savefig('tema3_exclusao_estrutural.png')
