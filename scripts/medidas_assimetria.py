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
df['taxa_real'] = df['taxa_real'].clip(upper=100)

dados = df['taxa_real']

assimetria = dados.skew()
curtose = dados.kurtosis()

print(" MEDIDAS DE FORMA (TAXA DE TRANSPORTE RURAL AL)\n")

print(f"Assimetria (Skewness): {assimetria:.4f}")
print(f"Curtose (Kurtosis):    {curtose:.4f}\n")


plt.figure(figsize=(6, 8))

sns.boxplot(y=dados, color='mediumseagreen', width=0.4, linewidth=2)


plt.title('Boxplot: Dependência Real de Transporte (%)', fontsize=14, fontweight='bold')
plt.ylabel('Percentual de Alunos no Transporte (%)', fontsize=12)


plt.savefig('medidas_forma_boxplot.png', bbox_inches='tight')
