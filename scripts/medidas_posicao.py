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

media = dados.mean()
mediana = dados.median()
moda = dados.mode()[0]

q1 = dados.quantile(0.25)
q2 = dados.quantile(0.50)
q3 = dados.quantile(0.75)

p10 = dados.quantile(0.10)
p90 = dados.quantile(0.90) 
p99 = dados.quantile(0.99)

print(" MEDIDAS DE POSIÇÃO (TAXA DE TRANSPORTE RURAL AL)\n")
print(f"Média:   {media:.2f}%")
print(f"Mediana: {mediana:.2f}%")
print(f"Moda:    {moda:.2f}%\n")

print(" QUARTIS\n")
print(f"Q1 (25% das escolas têm até): {q1:.2f}%")
print(f"Q2 (50% das escolas têm até): {q2:.2f}% (Mediana)")
print(f"Q3 (75% das escolas têm até): {q3:.2f}%\n")


print(" PERCENTIS ESPECÍFICOS (PONTOS DE CORTE)\n")

print(f"Percentil 10 (10% menos dependentes têm até): {p10:.2f}%")
print(f"Percentil 90 (As 10% mais dependentes passam de): {p90:.2f}%")
print(f"Percentil 99 (O 1% mais extremo passa de):       {p99:.2f}%\n")
