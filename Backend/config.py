"""
Configuration settings for Anime Picker System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Model Settings
    MODEL_NAME = 'sentence-transformers/all-mpnet-base-v2'  # Better accuracy model (420 MB, ~63 MTEB score)
    METADATA_FILE = 'anime_metadata.csv'
    EMBEDDINGS_FILE = 'anime_embeddings.npy'
    
    # Search Settings
    MAX_RESULTS = 5
    CANDIDATE_POOL_SIZE = 50
    MAX_QUERY_LENGTH = 500
    
    # Server Settings
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')  # Changed for production deployment
    
    # Cache Settings
    ENABLE_QUERY_CACHE = True
    MAX_CACHE_SIZE = 100
    
    
    # Logging Settings
    LOG_FILE = 'anime_picker.log'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Default to INFO if not set
