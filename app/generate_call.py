from data_generator.generate import generate_data
import os
import pyarrow.parquet as pq

# TOTAL_ROWS = 1_000_000_000
# BATCH_SIZE = 1_000_000
TOTAL_ROWS = 10_000_000
BATCH_SIZE = 2_500_000
OUTPUT_FILE = "/data/user_purchases_optimized.parquet"
STATUS_OPTIONS = ["completed", "shipped", "cancelled"]

def generate_call():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"Arquivo antigo '{OUTPUT_FILE}' removido.")
    num_batches = TOTAL_ROWS // BATCH_SIZE
    print(f"Iniciando a geração de {TOTAL_ROWS:,} linhas em {num_batches} lotes de {BATCH_SIZE:,}...")
    writer = None
    try:
        for i in range(num_batches):
            print(f"Gerando e escrevendo lote {i + 1}/{num_batches}...")
            start_id = i * BATCH_SIZE
            df_batch = generate_data(start_id=start_id, batch_size=BATCH_SIZE)
            arrow_table = df_batch.to_arrow()
            if writer is None:
                writer = pq.ParquetWriter(OUTPUT_FILE, arrow_table.schema, compression='snappy')
            writer.write_table(arrow_table)

    finally:
        if writer:
            writer.close()
            print(f"\nArquivo '{OUTPUT_FILE}' gerado com sucesso!")
        else:
            print("\nNenhum dado foi gerado.")