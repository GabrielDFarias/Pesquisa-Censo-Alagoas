import pandas as pd
import numpy as np

colunas = ['SG_UF', 'TP_LOCALIZACAO', 'QT_MAT_BAS', 'QT_TRANSP_PUBLICO']
df_bruto = pd.read_csv('microdados_ed_basica_2023.csv', sep=';', encoding='latin1', usecols=colunas)

df = df_bruto[(df_bruto['SG_UF'] == 'AL') & (df_bruto['TP_LOCALIZACAO'] == 2)].copy()
df['QT_MAT_BAS'] = df['QT_MAT_BAS'].fillna(0)
df['QT_TRANSP_PUBLICO'] = df['QT_TRANSP_PUBLICO'].fillna(0)
df = df[df['QT_MAT_BAS'] > 0].copy()

df['taxa_real'] = (df['QT_TRANSP_PUBLICO'] / df['QT_MAT_BAS']) * 100
df['taxa_real'] = df['taxa_real'].clip(upper=100)

dados = df['taxa_real']

amplitude = dados.max() - dados.min()

variancia = dados.var()
desvio_padrao = dados.std()

q1 = dados.quantile(0.25)
q3 = dados.quantile(0.75)
iqr = q3 - q1

print(" MEDIDAS DE DISPERSÃO (TAXA DE TRANSPORTE RURAL AL)\n")
print(f"Amplitude:                    {amplitude:.2f}%")
print(f"Variância:                    {variancia:.2f}")
print(f"Desvio Padrão:                {desvio_padrao:.2f}%")
print(f"Distância Interquartil (IQR): {iqr:.2f}%\n")
