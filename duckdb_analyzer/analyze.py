import duckdb
import os

minio_endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
minio_access_key = os.getenv("MINIO_ROOT_USER", "minioadmin")
minio_secret_key = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
bucket_name = "bronze"
file_path = f"s3://{bucket_name}/user_purchases_optimized.parquet"

print(f"Iniciando análise com DuckDB no arquivo: {file_path}")

try:
    con = duckdb.connect(database=':memory:')

    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")

    con.execute(f"SET s3_endpoint = '{minio_endpoint.split('//')[1]}';")
    con.execute(f"SET s3_url_style = 'path';")
    con.execute(f"SET s3_access_key_id = '{minio_access_key}';")
    con.execute(f"SET s3_secret_access_key = '{minio_secret_key}';")

    con.execute("SET s3_use_ssl = false;")

    print("\n--- 1. Contagem de Linhas ---")
    row_count = con.execute(f"SELECT COUNT(*) FROM '{file_path}';").fetchone()[0]
    print(f"O arquivo contém {row_count:,} linhas.")

    print("\n--- 2. Validação de Tipos (Schema) ---")
    schema = con.execute(f"DESCRIBE SELECT * FROM '{file_path}';").df()
    print(schema)

    print("\n--- 3. Estatísticas Descritivas ---")
    stats = con.execute(f"SUMMARIZE SELECT * FROM '{file_path}';").df()
    print(stats)
    
    print("\n--- 4. Exemplo de Agregação: Preço médio por categoria ---")
    avg_price_by_category = con.execute(f"""
        SELECT category, AVG(price) as average_price
        FROM '{file_path}'
        GROUP BY category
        ORDER BY average_price DESC;
    """).df()
    print(avg_price_by_category)


except Exception as e:
    print(f'ERRO: O erro "{e}" ocorreu durante a análise.')

finally:
    if 'con' in locals():
        con.close()
    print("\nAnálise finalizada.")