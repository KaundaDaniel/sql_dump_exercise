# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta



# ===================== CONFIGURAÇÕES =====================

NUM_CLIENTES = 120
NUM_CATEGORIAS = 12
NUM_PRODUTOS = 150
NUM_PEDIDOS = 350
MAX_ITENS_POR_PEDIDO = 6
OUTPUT_FILE = "dados.sql"

random.seed(42)

def sql_escape(value):
    return str(value).replace("'", "''")

# ===================== LISTAS COM ACENTOS =====================
nomes_angolanos = ["João", "Maria", "António", "Ana", "José", "Francisca", "Pedro", "Isabel",
                   "Carlos", "Luísa", "Miguel", "Sofia", "André", "Clara", "Paulo", "Raquel"]

apelidos_angolanos = ["Da Silva", "Dos Santos", "Francisco", "Manuel", "Oliveira", "Neto",
                      "Chivela", "Mendes", "Tomas", "Gomes", "Pereira", "António", "Kassongo"]

cidades_angola = ["Luanda", "Lobito", "Huambo", "Benguela", "Lubango", "Cabinda", "Malanje",
                  "Saurimo", "Ondjiva", "Dundo", "Sumbe", "Cuito", "N'dalatando"]

estados = ["LU", "BE", "HS", "CA", "NA", "ML", "BO", "CU", "HU"]

categorias_lista = [
    ("Eletrônicos", "Televisores, smartphones e acessórios"),
    ("Roupas", "Vestuário masculino, feminino e infantil"),
    ("Calçados", "Sapatos, botas e chinelos"),
    ("Alimentos", "Mercearia e produtos frescos"),
    ("Bebidas", "Refrigerantes, sumos e águas"),
    ("Casa", "Utensílios domésticos e decoração"),
    ("Móveis", "Mobiliário para casa e escritório"),
    ("Beleza", "Cosméticos e cuidados pessoais"),
    ("Esportes", "Equipamentos desportivos"),
    ("Informática", "Computadores e periféricos"),
    ("Jogos", "Consolas e jogos"),
    ("Automotivo", "Acessórios para veículos")
]

produtos_base = ["Camiseta", "Calça Jeans", "Tênis", "Smartphone", "Televisor", "Fone Bluetooth",
                 "Arroz", "Óleo", "Refrigerante", "Sofá", "Cadeira", "Notebook", "Mouse", "Panela",
                 "Liquidificador", "Bola de Futebol", "Perfume", "Relógio"]

# ===================== FUNÇÕES =====================
def random_date(start_year=2023, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).date()

# ===================== GERAÇÃO =====================
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    def w(line=""):
        f.write(line + "\n")

    w(f"-- Script gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    w("-- Encoding: UTF-8\n")

    # 1. CATEGORIAS
    w("-- ==================== CATEGORIAS ====================")
    w("INSERT INTO categorias (id, nome, descricao) VALUES")
    for i in range(1, NUM_CATEGORIAS + 1):
        nome, desc = categorias_lista[i-1] if i <= len(categorias_lista) else (f"Categoria {i}", "")
        comma = ',' if i < NUM_CATEGORIAS else ';'
        w(f"({i}, '{sql_escape(nome)}', '{sql_escape(desc)}'){comma}")

    # 2. CLIENTES
    w("\n-- ==================== CLIENTES ====================")
    w("INSERT INTO clientes (id, nome, email, cidade, estado, data_cadastro, ativo) VALUES")
    for i in range(1, NUM_CLIENTES + 1):
        nome = f"{random.choice(nomes_angolanos)} {random.choice(apelidos_angolanos)}"
        email = f"cliente{i}@example.com"
        cidade = random.choice(cidades_angola)
        estado = random.choice(estados)
        data = random_date(2023, 2025)
        ativo = random.choice([True, True, False])
        comma = ',' if i < NUM_CLIENTES else ';'
        w(f"({i}, '{sql_escape(nome)}', '{email}', '{sql_escape(cidade)}', '{estado}', '{data}', {ativo}){comma}")

    # 3. PRODUTOS
    w("\n-- ==================== PRODUTOS ====================")
    w("INSERT INTO produtos (id, nome, preco, categoria_id, estoque) VALUES")
    for i in range(1, NUM_PRODUTOS + 1):
        nome_prod = f"{random.choice(produtos_base)} Modelo {i}"
        preco = round(random.uniform(250, 12500), 2)
        cat_id = random.randint(1, NUM_CATEGORIAS)
        estoque = random.randint(5, 250)
        comma = ',' if i < NUM_PRODUTOS else ';'
        w(f"({i}, '{sql_escape(nome_prod)}', {preco}, {cat_id}, {estoque}){comma}")

    # 4. PEDIDOS
    w("\n-- ==================== PEDIDOS ====================")
    w("INSERT INTO pedidos (id, cliente_id, data_pedido, status, total) VALUES")

    itens_para_imprimir = []
    item_id = 1

    for pedido_id in range(1, NUM_PEDIDOS + 1):
        cliente_id = random.randint(1, NUM_CLIENTES)
        data_pedido = random_date(2024, 2026)
        status = random.choice(['Concluído', 'Processando', 'Enviado', 'Cancelado'])

        num_itens = random.randint(1, MAX_ITENS_POR_PEDIDO)
        total_pedido = 0.0

        for _ in range(num_itens):
            produto_id = random.randint(1, NUM_PRODUTOS)
            quantidade = random.randint(1, 10)
            preco_unitario = round(random.uniform(250, 8500), 2)
            total_pedido += quantidade * preco_unitario
            itens_para_imprimir.append(f"({item_id}, {pedido_id}, {produto_id}, {quantidade}, {preco_unitario})")
            item_id += 1

        comma = ',' if pedido_id < NUM_PEDIDOS else ';'
        w(f"({pedido_id}, {cliente_id}, '{data_pedido}', '{status}', {round(total_pedido, 2)}){comma}")

    # 5. ITENS_PEDIDO
    w("\n-- ==================== ITENS_PEDIDO ====================")
    w("INSERT INTO itens_pedido (id, pedido_id, produto_id, quantidade, preco_unitario) VALUES")
    for i, linha in enumerate(itens_para_imprimir):
        comma = ',' if i < len(itens_para_imprimir) - 1 else ';'
        w(linha + comma)

    w(f"\n-- Total de pedidos: {NUM_PEDIDOS}")
    w(f"-- Total de itens: {item_id-1}")
    w("-- Script finalizado com sucesso!")

print(f"Ficheiro '{OUTPUT_FILE}' gerado com sucesso (UTF-8).")
