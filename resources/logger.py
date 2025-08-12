# utils/logger.py
from enum import Enum

class LogCategory(Enum):
    USER = 'user'
    THOUGHT = 'thought'
    ACTION = 'action'
    OBSERVATION = 'observation'
    END = 'end'

# Códigos ANSI para cores no console
_COLORS = {
    LogCategory.USER: '\033[94m',      # Azul
    LogCategory.THOUGHT: '\033[96m',   # Ciano
    LogCategory.ACTION: '\033[92m',    # Verde
    LogCategory.OBSERVATION: '\033[93m', # Amarelo
    LogCategory.END: '\033[0m'         # Resetar
}

def log(message: str, category: LogCategory):
    """
    Imprime uma mensagem colorida no console.
    :param message: A mensagem a ser impressa.
    :param category: A categoria da mensagem (usando LogCategory Enum).
    """
    color = _COLORS.get(category, _COLORS[LogCategory.END])
    print(f"{color}{message}{_COLORS[LogCategory.END]}")