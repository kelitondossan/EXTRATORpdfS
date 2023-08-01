from flask import Flask, render_template
import os
from PyPDF2 import PdfReader
import re
import pymysql

app = Flask(__name__)

# Restante do código permanece igual

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    # Conectar ao banco de dados MySQL
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="faturas"
    )

    # Criar as tabelas
    with conn.cursor() as cur:
        # Tabela de Faturas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS faturas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_arquivo VARCHAR(100) NOT NULL,
                mes_referencia VARCHAR(10),
                valor_total DECIMAL(10, 2)
            )
        """)

        # Tabela de Valores Faturados
        cur.execute("""
            CREATE TABLE IF NOT EXISTS valores_faturados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fatura_id INT,
                tipo VARCHAR(50) NOT NULL,
                quantidade DECIMAL(10, 2),
                preco_unit DECIMAL(10, 2),
                valor DECIMAL(10, 2),
                FOREIGN KEY (fatura_id) REFERENCES faturas(id)
            )
        """)

        # Tabela de Histórico de Consumo
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historico_consumo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fatura_id INT,
                mes_ano VARCHAR(10),
                cons_kwh DECIMAL(10, 2),
                media_kwh_dia DECIMAL(10, 2),
                dias INT,
                FOREIGN KEY (fatura_id) REFERENCES faturas(id)
            )
        """)

    # Fechar a conexão com o banco de dados
    conn.close()

# Função para inserir os dados extraídos no banco de dados
def inserir_dados(faturas):
    # Conectar ao banco de dados MySQL
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="faturas"
    )

    with conn.cursor() as cur:
        for fatura in faturas:
            # Inserir dados na tabela de Faturas
            cur.execute("""
                INSERT INTO faturas (nome_arquivo, mes_referencia, valor_total)
                VALUES (%s, %s, %s)
            """, (fatura['nome_arquivo'], fatura['mes_referencia'], fatura['valor_total']))
            fatura_id = conn.insert_id()

            # Inserir dados na tabela de Valores Faturados
            for tipo, valores in fatura['valores_faturados'].items():
                cur.execute("""
                    INSERT INTO valores_faturados (fatura_id, tipo, quantidade, preco_unit, valor)
                    VALUES (%s, %s, %s, %s, %s)
                """, (fatura_id, tipo, valores['Quant.'], valores['Preço Unit'], valores['Valor (R$)']))

            # Inserir dados na tabela de Histórico de Consumo
            for historico in fatura['historico_consumo']:
                cur.execute("""
                    INSERT INTO historico_consumo (fatura_id, mes_ano, cons_kwh, media_kwh_dia, dias)
                    VALUES (%s, %s, %s, %s, %s)
                """, (fatura_id, historico['Mês/Ano'], historico['Cons. kWh'], historico['Média kWh/Dia'], historico['Dias']))

    # Commit e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()

# Para chamar as funções de criação de tabelas e inserção de dados, podemos adicionar o seguinte código no início do arquivo:

if __name__ == '__main__':
    # Cria as tabelas no banco de dados
    criar_tabelas()

    # Use o caminho absoluto para a pasta "Faturas"
    pasta_fatura = os.path.abspath("Faturas")  
    faturas = ler_faturas_pasta(pasta_fatura)

    # Insere os dados no banco de dados
    inserir_dados(faturas)

    app.run(debug=True)
