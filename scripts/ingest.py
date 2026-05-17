import kagglehub
import shutil
import os

# Descargar dataset desde Kaggle
path = kagglehub.dataset_download("muhammadtalhaawan/world-export-and-import-dataset")

# Crear carpetas del proyecto
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# Copiar CSV a data/raw/
for file in os.listdir(path):
    if file.endswith(".csv"):
        shutil.copy(os.path.join(path, file), "data/raw/")
        print(f"Archivo copiado: {file} → data/raw/{file}")

print("Ingesta completada.")