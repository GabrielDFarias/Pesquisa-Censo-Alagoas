import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


colunas = ['SG_UF', 'TP_LOCALIZACAO', 'QT_MAT_BAS', 'QT_TRANSP_PUBLICO']
df_bruto = pd.read_csv('microdados_ed_basica_2023.csv', sep=';', encoding='latin1', usecols=colunas)

df = df_bruto[(df_bruto['SG_UF'] == 'AL') & (df_bruto['TP_LOCALIZACAO'] == 2)].copy()
df['QT_MAT_BAS'] = df['QT_MAT_BAS'].fillna(0)
df['QT_TRANSP_PUBLICO'] = df['QT_TRANSP_PUBLICO'].fillna(0)

df = df[df['QT_MAT_BAS'] > 0].copy()

df['taxa_real'] = (df['QT_TRANSP_PUBLICO'] / df['QT_MAT_BAS']) * 100
df['taxa_real'] = df['taxa_real'].clip(upper=100) # Limite seguro de 100%

dados = df['taxa_real']

estatisticas = {
    'Média': dados.mean(),
    'Mediana': dados.median(),
    'Moda': dados.mode()[0],
    'Q1 (25%)': dados.quantile(0.25),
    'Q3 (75%)': dados.quantile(0.75),
    'Desvio Padrão': dados.std(),
    'Assimetria': dados.skew()
}
sns.set_theme(style="whitegrid")

# 1. Boxplot Vertical
plt.figure(figsize=(6, 8))
sns.boxplot(y=dados, color='mediumseagreen', width=0.4, linewidth=2)
plt.title('Dependência de Transporte (%)')
plt.ylabel('Percentual de Alunos no Transporte (%)')
plt.savefig('geral_1_boxplot_real.png', bbox_inches='tight')

plt.figure(figsize=(10, 6))
sns.histplot(dados, bins=20, color='dodgerblue', kde=False, edgecolor='black')
plt.title('Distribuição Geral')
plt.xlabel('Taxa de Dependência de Transporte (%)')
plt.ylabel('Número de Escolas')
plt.savefig('geral_2_histograma_real.png', bbox_inches='tight')

sorted_data = np.sort(dados)
yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)

plt.figure(figsize=(10, 6))
plt.plot(sorted_data, yvals, color='darkorange', linewidth=3)
plt.fill_between(sorted_data, yvals, color='orange', alpha=0.2)
plt.axhline(0.5, color='gray', linestyle='--', label=f'Mediana ({estatisticas["Mediana"]:.1f}%)')
plt.axvline(estatisticas["Mediana"], color='gray', linestyle='--')
plt.title('Quantas escolas dependem de transporte?')
plt.xlabel('Taxa de Dependência (%)')
plt.ylabel('Proporção Acumulada da Rede (0 a 1.0)')
plt.legend()
plt.savefig('geral_3_ogiva_real.png', bbox_inches='tight')

