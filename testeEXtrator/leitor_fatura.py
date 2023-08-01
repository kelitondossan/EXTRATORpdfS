import os
import PyPDF2

def ler_faturas_pasta(pasta):
    faturas = []

    # Verificar se a pasta existe
    if not os.path.exists(pasta):
        print(f"A pasta {pasta} não existe.")
        return faturas

    # Percorrer os arquivos na pasta
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)

        # Verificar se o arquivo é PDF
        if arquivo.lower().endswith(".pdf"):
            with open(caminho_arquivo, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)

                # Extrair informações do PDF
                num_paginas = pdf_reader.numPages
                texto = ""

                for pagina in range(num_paginas):
                    page = pdf_reader.getPage(pagina)
                    texto += page.extractText()

                faturas.append({
                    "nome_arquivo": arquivo,
                    "num_paginas": num_paginas,
                    "texto": texto
                })

    return faturas
