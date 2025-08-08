from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

print("✅ .env loaded from:", env_path.resolve())
print("🔑 CLOUDINARY_API_KEY:", os.getenv("CLOUDINARY_API_KEY"))
