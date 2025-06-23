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


fake = Faker()
Faker.seed(42)
random.seed(42)

# Parâmetros (AJUSTADOS PARA TESTE)
# TOTAL_ROWS = 1_000_000_000
# BATCH_SIZE = 1_000_000
TOTAL_ROWS = 10_000
BATCH_SIZE = 2_500
OUTPUT_FILE = "user_purchases.parquet"
CATEGORIES = ["Eletrônicos", "Livros", "Roupas", "Alimentos", "Móveis", "Brinquedos", "Beleza"]
STATUS_OPTIONS = ["completed", "shipped", "cancelled"]

def generate_batch(start_id: int, batch_size: int) -> pl.DataFrame:
    data = {
        "order_id": list(range(start_id, start_id + batch_size)),
        "user_id": [random.randint(1, 10_000_000) for _ in range(batch_size)],
        "product_id": [random.randint(1, 1_000_000) for _ in range(batch_size)],
        "product_name": [fake.word().capitalize() for _ in range(batch_size)],
        "category": [random.choice(CATEGORIES) for _ in range(batch_size)],
        "price": [round(random.uniform(5, 1000), 2) for _ in range(batch_size)],
        "quantity": [random.randint(1, 10) for _ in range(batch_size)],
        # --- MUDANÇA AQUI ---
        # Formatamos a data para uma string legível usando strftime
        "order_date": [fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') for _ in range(batch_size)],
        "status": [random.choice(STATUS_OPTIONS) for _ in range(batch_size)],
    }
    return pl.DataFrame(data)

def generate_data(output_path: str):
    print("Gerando o primeiro lote para definir o schema...")
    first_batch = generate_batch(0, BATCH_SIZE)

    arrow_schema = first_batch.to_arrow().schema

    writer = None
    try:
        writer = pq.ParquetWriter(output_path, arrow_schema, compression="snappy")

        # 2. Escreve o primeiro lote
        writer.write_table(first_batch.to_arrow())
        print(f"Lote inicial (0 a {BATCH_SIZE - 1}) salvo.")

        # 3. Itera sobre os lotes restantes e os escreve
        for i in range(BATCH_SIZE, TOTAL_ROWS, BATCH_SIZE):
            print(f"Gerando e salvando linhas {i} até {i + BATCH_SIZE - 1}...")
            batch = generate_batch(i, BATCH_SIZE)
            writer.write_table(batch.to_arrow())

        print(f"Arquivo {output_path} gerado com sucesso com {TOTAL_ROWS} linhas.")
    finally:
        if writer:
            writer.close()
        print("Processo concluído.")
