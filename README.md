# Produtividade Setorial no Brasil: Uma Análise Comparativa Pré e Pós-Pandemia

https://doi.org/10.5281/zenodo.19131400

Este repositório contém os dados e códigos de replicação para o *Working Paper* [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6423439].

## Resumo do Projeto
A pesquisa analisa a evolução da produtividade do trabalho no Brasil, segmentada por grandes setores (Indústria, Comércio, Serviços e Agronegócio). O objetivo principal é comparar a trajetória histórica e projetada da produtividade com os resultados efetivamente realizados após o choque da pandemia de COVID-19.

## Fontes de Dados
Os dados brutos foram extraídos do Instituto Brasileiro de Geografia e Estatística (IBGE) - Contas Nacionais Trimestrais:
* **Tabela 6612:** Valores encadeados a preços de 1995 (Valor Adicionado por setor).
* **Tabela 6465:** Pessoas de 14 anos ou mais de idade, ocupadas na semana de referência (PNAD).

## Estrutura do Repositório
* `data/raw/`: Contém os microdados originais extraídos do IBGE.
* `data/processed/`: Contém as séries históricas calculadas, projeções (2020-2025) e as matrizes de comparação pré/pós pandemia.
* `scripts/`: Contém os scripts em Python utilizados para limpeza, fusão das bases e cálculo da produtividade (VA/PO).

## Como Replicar
Para replicar os resultados e tabelas apresentadas no artigo:

1. Clone este repositório: `git clone https://github.com/SeuUsuario/meu-projeto-produtividade.git`
2. Certifique-se de ter o Python 3.8+ instalado, juntamente com a biblioteca `pandas`.
3. Execute o script principal:
   ```bash
   python scripts/01_analise_produtividade.py
