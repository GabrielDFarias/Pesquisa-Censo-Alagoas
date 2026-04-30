# 📊 Diagnóstico Logístico e Estrutural da Educação Rural em Alagoas

Este repositório contém os scripts de análise exploratória e estatística descritiva baseados nos **Microdados do Censo Escolar da Educação Básica de 2023 (INEP)**. O foco central da pesquisa é investigar a vulnerabilidade, a infraestrutura e o nível de dependência de transporte público das escolas rurais no estado de Alagoas.

## 📌 Contexto da Pesquisa
No interior do Brasil, o acesso à educação está diretamente condicionado à infraestrutura de deslocamento. Este projeto utiliza Python e Estatística para provar matematicamente o "efeito funil" na educação do campo, evidenciando como a precarização estrutural (falta de água, saneamento e internet) e o esgotamento logístico geram evasão escolar, especialmente na transição para o Ensino Médio.

## 🚀 Principais Eixos de Análise
1. **O Colapso Logístico:** Comprovação estatística (distribuições bimodais, assimetria e curtose) de que a rede rural não possui um padrão homogêneo, sustentando-se fortemente em "Escolas Polo" superlotadas.
2. **O Funil Educacional:** Visualização da queda drástica de matrículas entre os Anos Iniciais do Ensino Fundamental e o Ensino Médio.
3. **Isolamento e Comunidades Tradicionais:** Cruzamento de dados estruturais comparando escolas rurais comuns, assentamentos, territórios quilombolas e terras indígenas.
4. **O Paradoxo Tecnológico:** Identificação de escolas que recebem equipamentos de internet via satélite, mas operam sem abastecimento de água potável ou esgotamento sanitário.

## 📁 Estrutura dos Arquivos
Os scripts foram divididos de forma cronológica, indo da matemática pura aos cruzamentos sociais complexos:

* **Estatística Matemática:**
  * `medidas_posicao.py`: Cálculo de Média, Mediana, Moda, Quartis e Percentis.
  * `medidas_dispersao.py`: Amplitude, Variância e Desvio Padrão.
  * `medidas_assimetria.py`: Assimetria, Curtose (excesso de Fisher) e geração de Boxplot.
* **Visualização de Dados e Diagnóstico:**
  * `panorama_geral_rede.py`: Histograma de frequências e Curva de Frequência Acumulada (Ogiva).
  * `mapeamento_geografico.py`: Dependência por tipo de comunidade, Score de Vulnerabilidade e Heatmap dos Top 10 municípios.
  * `funil_escolar_e_agua.py`: Gráficos da evasão no Ensino Médio e do déficit hídrico.
  * `perfil_demografico_e_infra.py`: Composição etária da rede e exclusão estrutural (biblioteca e internet).
  * `comunidades_e_paradoxos.py`: Peso logístico do EJA, Paradoxo Tecnológico e Raio-X Indígena x Quilombola.

## 🛠️ Tecnologias e Bibliotecas
* **Python 3**
* **Pandas:** Limpeza, filtragem, agrupamentos (groupby) e cálculos estatísticos.
* **NumPy:** Operações matemáticas vetoriais e cálculos de percentis.
* **Matplotlib & Seaborn:** Geração de gráficos, mapas de calor (heatmaps) e manipulação de paletas de cores.

## 📥 Como Reproduzir este Projeto

Devido ao tamanho limite de arquivos do GitHub e boas práticas de controle de versão, a base de dados original `.csv` **não** está inclusa neste repositório.

Para rodar os scripts localmente:
1. Clone este repositório: `git clone https://github.com/GabrielDFarias/Pesquisa-Censo-Alagoas.git`
2. Instale as dependências: `pip install pandas numpy matplotlib seaborn`
3. Baixe os Microdados do Censo Escolar 2023 no [portal de Dados Abertos do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados).
4. Extraia o arquivo de escolas (`microdados_ed_basica_2023.csv`) e coloque-o na mesma pasta dos scripts (ou ajuste o caminho do `pd.read_csv` nos arquivos).
5. Execute os scripts em ordem de preferência.

---
**Autor:** Gabriel Farias
*Análise com foco em políticas públicas e sociologia educacional computacional.*
