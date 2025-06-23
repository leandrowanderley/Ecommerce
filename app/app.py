from data_generator.generate import generate_data
import os

def main():
    output_dir = "/data" 
    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, "user_purchases.parquet")

    print(f"Iniciando a geração de dados em {output_file_path}...")
    generate_data(output_path=output_file_path)
    print("Geração de dados concluída com sucesso.")

if __name__ == "__main__":
    main()