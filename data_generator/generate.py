# order_id: ID sequencial do pedido.
# user_id: ID inteiro do usuário.
# product_id: ID inteiro do produto.
# product_name: Nome fictício do produto (Faker).
# category: Categoria aleatória do produto.
# price: Preço unitário (float).
# quantity: Quantidade comprada (int).
# order_date: Data/hora da compra (datetime no formato AAAA-MM-DD HH:MM:SS).
# status: Status do pedido ('completed', 'shipped', 'cancelled').

import polars as pl
from faker import Faker
import pyarrow.parquet as pq
import random
import os

fake = Faker()
Faker.seed(42)
random.seed(42)

STATUS_OPTIONS = ["completed", "shipped", "cancelled"]

REAL_PRODUCTS_BY_CATEGORY = {
    "Eletrônicos": [
        "Smartphone Galaxy S25", "Notebook UltraBook i7", "Smart TV 4K 55 Polegadas",
        "Fone de Ouvido Bluetooth TWS", "Monitor Gamer Curvo 27 pol", "Carregador Portátil 20000mAh"
    ],
    "Livros": [
        "O Senhor dos Anéis: A Sociedade do Anel", "A Culpa é das Estrelas", "O Guia do Mochileiro das Galáxias",
        "Sapiens: Uma Breve História da Humanidade", "Duna", "O Poder do Hábito"
    ],
    "Roupas": [
        "Camiseta de Algodão Básica", "Calça Jeans Slim Fit", "Jaqueta Corta-Vento Impermeável",
        "Vestido Floral de Verão", "Tênis de Corrida Performance", "Moletom com Capuz"
    ],
    "Alimentos": [
        "Café Gourmet Grãos 1kg", "Azeite de Oliva Extra Virgem 500ml", "Barra de Proteína Sabor Chocolate",
        "Arroz Integral Orgânico 1kg", "Molho de Tomate Artesanal", "Vinho Tinto Cabernet Sauvignon"
    ],
    "Móveis": [
        "Cadeira de Escritório Ergonômica", "Mesa de Jantar 4 Lugares", "Sofá Retrátil 3 Lugares",
        "Estante para Livros 5 Prateleiras", "Guarda-Roupa Casal com Espelho"
    ],
    "Brinquedos": [
        "Blocos de Montar - Castelo Medieval", "Quebra-Cabeça 1000 Peças - Paisagem", "Carro de Controle Remoto 4x4",
        "Boneca Articulada com Acessórios", "Jogo de Tabuleiro - Conquista Espacial"
    ],
    "Beleza": [
        "Protetor Solar FPS 50", "Creme Hidratante Facial Noturno", "Shampoo para Cabelos Cacheados",
        "Perfume Masculino Amadeirado", "Kit de Maquiagem Essencial"
    ]
}
CATEGORIES = list(REAL_PRODUCTS_BY_CATEGORY.keys())

def generate_data(start_id: int, batch_size: int) -> pl.DataFrame:
    products = []
    categories = []

    for _ in range(batch_size):
        selected_category = random.choice(CATEGORIES)
        selected_product = random.choice(REAL_PRODUCTS_BY_CATEGORY[selected_category])
        products.append(selected_product)
        categories.append(selected_category)

    data = {
        # "order_id": range(start_id, start_id + batch_size),
        # "user_id": [random.randint(1, 10_000_000) for _ in range(batch_size)],
        # "product_id": [random.randint(1, 1_000_000) for _ in range(batch_size)],
        "product_name": products,
        # "category": categories,
        "price": [round(random.uniform(5, 1000), 2) for _ in range(batch_size)],
        # "quantity": [random.randint(1, 10) for _ in range(batch_size)],
        "order_date": [fake.date_time_between(start_date='-2y', end_date='now') for _ in range(batch_size)],
        # "status": [random.choice(STATUS_OPTIONS) for _ in range(batch_size)],
    }
    return pl.DataFrame(data, schema={
            # "order_id": pl.UInt64,
            # "user_id": pl.UInt32,
            # "product_id": pl.UInt32,
            "product_name": pl.String,
            # "category": pl.Categorical,
            "price": pl.Float32,
            # "quantity": pl.UInt8,
            "order_date": pl.Datetime,
            # "status": pl.Categorical
        })
