import gdown
import os

FOLDER_ID = "1XvhX-R3-oJoEbT1ib38Q7DP2uBlyHlZc"  


os.makedirs("data/raw/", exist_ok=True)

gdown.download_folder(FOLDER_ID, output="data/raw")

