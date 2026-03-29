"""
Tech Watch Agent - Main Entry Point
"""
import os
import warnings

# Suppress ONNX Runtime GPU warnings
os.environ['ORT_LOGGING_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=UserWarning, module='onnxruntime')

from src.cli import app

if __name__ == "__main__":
    app()
