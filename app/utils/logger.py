"""
Utilitários de logging
"""

import logging
from logging.handlers import RotatingFileHandler
import os

def configurar_logger(nome: str, arquivo_log: str = "app.log") -> logging.Logger:
    """Configura um logger"""
    logger = logging.getLogger(nome)
    logger.setLevel(logging.DEBUG)
    
    # Handler para arquivo
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    file_handler = RotatingFileHandler(f"logs/{arquivo_log}", maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
