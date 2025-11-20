"""
Configuration settings for Anime Picker System
"""
import os


class Config:
    """Application configuration"""
    
    # Model Settings
    MODEL_NAME = 'all-MiniLM-L6-v2'  # Lightweight model (80 MB, works on 1 GB RAM)
    EMBEDDINGS_FILE = 'anime_embeddings.pkl'
    
    # Search Settings
    MAX_RESULTS = 5
    CANDIDATE_POOL_SIZE = 50
    MAX_QUERY_LENGTH = 500
    
    # Server Settings
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '127.0.0.1')
    
    # Cache Settings
    ENABLE_QUERY_CACHE = True
    MAX_CACHE_SIZE = 100
    
    # Logging Settings
    LOG_FILE = 'anime_picker.log'
    LOG_LEVEL = 'INFO'
