"""Módulo de utilitários da automação"""

from utils.logger import Logger
from utils.browser import BrowserManager
from utils.automation import WebAutomation
from utils.files import FileManager

__all__ = [
    "Logger",
    "BrowserManager",
    "WebAutomation",
    "FileManager",
    "ResumoDados"
]