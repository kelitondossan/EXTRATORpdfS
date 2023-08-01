from leitor_faturas import ler_faturas_pasta

# Pasta onde estão os arquivos PDF das faturas
pasta_fatura = "caminho/para/pasta/Fatura"

faturas = ler_faturas_pasta(pasta_fatura)

# Exemplo de como acessar as informações das faturas lidas
for fatura in faturas:
    print("Nome do arquivo:", fatura["nome_arquivo"])
    print("Número de páginas:", fatura["num_paginas"])
    print("Texto extraído do PDF:")
    print(fatura["texto"])
    print("----------------------")
