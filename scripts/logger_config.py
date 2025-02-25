import logging
from pathlib import Path

# Caminho para a pasta de logs | Path to the logs folder
caminho_logs = Path.home() / "Documents" / "BolsaValores" / "logs"
caminho_logs.mkdir(parents=True, exist_ok=True)

# Configuração do logging | Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(caminho_logs / "app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)