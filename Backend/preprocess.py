"""
Preprocessing Script - Generate Anime Embeddings
This script processes the anime dataset and creates embeddings for semantic search.
"""
import pandas as pd
from sentence_transformers import SentenceTransformer
import pickle
import logging
import sys
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_and_clean_data(input_file='anime_clean.csv'):
    """Load and validate the anime dataset"""
    logger.info(f"Loading dataset from: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} anime entries")
        
        # Check required columns
        required_columns = ['title', 'synopsis', 'genres', 'main_pic', 'combined_text']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return None
        
        # Remove rows with missing combined text
        initial_count = len(df)
        df = df.dropna(subset=['combined_text'])
        removed = initial_count - len(df)
        
        if removed > 0:
            logger.warning(f"Removed {removed} rows with missing 'combined_text' text")
        
        logger.info(f"Final dataset: {len(df)} anime entries")
        return df
        
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        return None
    except Exception as e:
        logger.error(f"Error loading data: {type(e).__name__}: {e}")
        return None


def generate_embeddings(df, model_name=None):
    """Generate embeddings for all anime"""
    if model_name is None:
        model_name = Config.MODEL_NAME
    
    logger.info(f"Loading model: {model_name}")
    logger.info("This may take a few minutes on first run (downloading model)...")
    
    try:
        model = SentenceTransformer(model_name)
        logger.info("Model loaded successfully")
        
        # Get the combined text for embedding
        texts = df['combined_text'].tolist()
        logger.info(f"Generating embeddings for {len(texts)} anime...")
        logger.info("This may take several minutes depending on your CPU...")
        
        # Generate embeddings with progress bar
        embeddings = model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32  # Adjust based on your RAM
        )
        
        logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {type(e).__name__}: {e}")
        return None


def save_embeddings(df, embeddings, output_file=None):
    """Save dataframe and embeddings to pickle file"""
    if output_file is None:
        output_file = Config.EMBEDDINGS_FILE
    
    logger.info(f"Saving embeddings to: {output_file}")
    
    try:
        with open(output_file, 'wb') as f:
            pickle.dump((df, embeddings), f)
        
        # Get file size
        import os
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        logger.info(f"Saved successfully! File size: {file_size:.2f} MB")
        return True
        
    except Exception as e:
        logger.error(f"Error saving embeddings: {type(e).__name__}: {e}")
        return False


def verify_embeddings(output_file=None):
    """Verify the saved embeddings can be loaded"""
    if output_file is None:
        output_file = Config.EMBEDDINGS_FILE
    
    logger.info("Verifying saved embeddings...")
    
    try:
        with open(output_file, 'rb') as f:
            df_loaded, embeddings_loaded = pickle.load(f)
        
        logger.info(f"✅ Verification successful!")
        logger.info(f"   - Loaded {len(df_loaded)} anime entries")
        logger.info(f"   - Embeddings shape: {embeddings_loaded.shape}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Verification failed: {type(e).__name__}: {e}")
        return False


def main():
    """Main preprocessing pipeline"""
    logger.info("="*60)
    logger.info("ANIME EMBEDDINGS PREPROCESSING")
    logger.info("="*60)
    logger.info("")
    
    # Step 1: Load and clean data
    df = load_and_clean_data()
    if df is None:
        logger.error("Failed to load data. Exiting.")
        return False
    
    logger.info("")
    
    # Step 2: Generate embeddings
    embeddings = generate_embeddings(df)
    if embeddings is None:
        logger.error("Failed to generate embeddings. Exiting.")
        return False
    
    logger.info("")
    
    # Step 3: Save embeddings
    if not save_embeddings(df, embeddings):
        logger.error("Failed to save embeddings. Exiting.")
        return False
    
    logger.info("")
    
    # Step 4: Verify
    if not verify_embeddings():
        logger.error("Failed to verify embeddings. Exiting.")
        return False
    
    logger.info("")
    logger.info("="*60)
    logger.info("✅ PREPROCESSING COMPLETE!")
    logger.info("="*60)
    logger.info("")
    logger.info("You can now run the application with:")
    logger.info("  python app.py")
    logger.info("")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
