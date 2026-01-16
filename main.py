"""
Main entry point para Railway
"""
import os
from app_factura import app

# Railway expone la app directamente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
