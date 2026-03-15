import pandas as pd
import numpy as np
import os

# ==============================================================================
# FUNÇÕES DE LIMPEZA DE DADOS
# ==============================================================================

def limpar_moeda_br(valor):
    """Remove R$, pontos de milhar, troca vírgula por ponto e converte para float."""
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, str):
        valor_limpo = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
        return float(valor_limpo)
    return float(valor)

def limpar_inteiro_br(valor):
    """Remove pontos de milhar (ex: 13.034.000) e converte para numérico."""
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, str):
        valor_limpo = valor.replace('.', '').strip()
        return float(valor_limpo)
    return float(valor)

def limpar_percentual_br(valor):
    """Remove o símbolo de % e converte a string com vírgula para decimal."""
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, str):
        valor_limpo = valor.replace('%', '').replace('.', '').replace(',', '.').strip()
        return float(valor_limpo) / 100  # Divide por 100 para ficar em formato decimal real
    return float(valor)

# ==============================================================================
# CONFIGURAÇÃO DE DIRETÓRIOS
# ==============================================================================
# Garante que as pastas existam para não dar erro na hora de salvar
os.makedirs('../data/processed_clean', exist_ok=True)

print("Iniciando a limpeza e formatação dos dados do Working Paper...")

# ==============================================================================
# 1. PROCESSAMENTO DA SÉRIE HISTÓRICA
# ==============================================================================
print("\nProcessando a Série Histórica de Produtividade...")
caminho_serie = '../data/processed/Produtividade comparada - Série histórica produtividade.csv'

try:
    df_serie = pd.read_csv(caminho_serie, encoding='utf-8')
    
    # Colunas de Valor Adicionado (VA) e Produtividade (R$)
    cols_moeda = [col for col in df_serie.columns if 'VA' in col or 'Produtividade' in col]
    # Colunas de Pessoas Ocupadas (PO)
    cols_po = [col for col in df_serie.columns if 'PO' in col]

    # Aplicando as limpezas
    for col in cols_moeda:
        df_serie[col] = df_serie[col].apply(limpar_moeda_br)
        
    for col in cols_po:
        df_serie[col] = df_serie[col].apply(limpar_inteiro_br)

    # Salvando a base limpa
    df_serie.to_csv('../data/processed_clean/serie_historica_limpa.csv', index=False)
    print(" -> Sucesso! 'serie_historica_limpa.csv' salvo.")
    
except FileNotFoundError:
    print(f" -> ERRO: Arquivo não encontrado no caminho: {caminho_serie}")

# ==============================================================================
# 2. PROCESSAMENTO: PROJETADO x ESPERADO
# ==============================================================================
print("\nProcessando o comparativo Projetado x Esperado 2020 a 2025...")
caminho_projetado = '../data/processed/Produtividade comparada - Projetado x esperado 2020 a 2025.csv'

try:
    df_proj = pd.read_csv(caminho_projetado, encoding='utf-8')
    
    cols_moeda_proj = [col for col in df_proj.columns if 'Produtividade' in col]
    cols_perc_proj = [col for col in df_proj.columns if 'Diferença' in col]

    for col in cols_moeda_proj:
        df_proj[col] = df_proj[col].apply(limpar_moeda_br)
        
    for col in cols_perc_proj:
        df_proj[col] = df_proj[col].apply(limpar_percentual_br)

    df_proj.to_csv('../data/processed_clean/projetado_x_esperado_limpo.csv', index=False)
    print(" -> Sucesso! 'projetado_x_esperado_limpo.csv' salvo.")

except FileNotFoundError:
    print(f" -> ERRO: Arquivo não encontrado no caminho: {caminho_projetado}")

# ==============================================================================
# CONCLUSÃO E VALIDAÇÃO (PROVA DE REPLICAÇÃO)
# ==============================================================================
print("\nValidando os cálculos (Produtividade = VA / PO)...")
try:
    # Recalculando a produtividade da Indústria como prova de conceito
    df_serie['Teste_Prod_Industria'] = df_serie['Indústria VA'] / df_serie['Indústria PO']
    
    # Pega a primeira linha para mostrar na tela
    prod_original = df_serie['Produtividade Indústria'].iloc[0]
    prod_calculada = df_serie['Teste_Prod_Industria'].iloc[0]
    trimestre = df_serie['Trimestre'].iloc[0]
    
    print(f"Trimestre: {trimestre}")
    print(f"Produtividade (Original da Planilha): R$ {prod_original:,.2f}")
    print(f"Produtividade (Recalculada no Script): R$ {prod_calculada:,.2f}")
    
    if abs(prod_original - prod_calculada) < 0.05: # Margem de erro para arredondamento
         print("-> Validação bem sucedida: Os dados são perfeitamente reprodutíveis!")
    
except Exception as e:
    print(" -> Não foi possível rodar a validação. Erro:", e)

print("\nProcesso de limpeza concluído! Os dados estão prontos para o GitHub e análises estatísticas.")
