from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy as np
import logging
import sys
import re
from config import Config

# ============================================
# LOGGING SETUP
# ============================================
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# FLASK APP INITIALIZATION
# ============================================
app = Flask(__name__)
CORS(app)

# ============================================
# GLOBAL VARIABLES
# ============================================
model = None
df = None
embeddings = None
query_cache = {}

# ============================================
# MODEL & DATA LOADING
# ============================================
def load_resources():
    """Load AI model and embeddings with proper error handling"""
    global model, df, embeddings
    
    try:
        logger.info("Loading AI Brain... (This stays in memory for speed)")
        
        # Load the sentence transformer model
        logger.info(f"Loading model: {Config.MODEL_NAME}")
        model = SentenceTransformer(Config.MODEL_NAME)
        logger.info("Model loaded successfully")
        
        # Load pre-computed embeddings
        logger.info(f"Loading embeddings from: {Config.EMBEDDINGS_FILE}")
        with open(Config.EMBEDDINGS_FILE, 'rb') as f:
            df, embeddings = pickle.load(f)
        
        logger.info(f"Loaded {len(df)} anime entries")
        logger.info(f"Embeddings shape: {embeddings.shape}")
        logger.info("System Ready!")
        
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error(f"Please ensure {Config.EMBEDDINGS_FILE} exists in the current directory")
        return False
        
    except Exception as e:
        logger.error(f"Error loading resources: {type(e).__name__}: {e}")
        return False


# ============================================
# HELPER FUNCTIONS
# ============================================
def get_franchise_name(title):
    """Extract base franchise name using regex patterns"""
    # Remove common suffixes and patterns
    patterns = [
        r'\s*:\s*.*',  # Everything after colon (but not Re:Zero style)
        r'\s+Season\s+\d+.*',
        r'\s+Part\s+\d+.*',
        r'\s+\d+(st|nd|rd|th)\s+Season.*',
        r'\s+Movie.*',
        r'\s+OVA.*',
        r'\s+ONA.*',
        r'\s+Special.*',
        r'\s+\(\d{4}\).*',  # Year in parentheses
        r'\s+\d{4}.*',  # Year
    ]
    
    clean_title = title
    
    # Special case: Don't split on colon if it's part of the title (like Re:Zero)
    if not title.startswith('Re:'):
        for pattern in patterns:
            clean_title = re.sub(pattern, '', clean_title, flags=re.IGNORECASE)
            if clean_title != title:  # If pattern matched, stop
                break
    
    return clean_title.strip()


def validate_query(query):
    """Validate and sanitize search query"""
    if not query:
        return None, "Query parameter 'q' is required"
    
    query = query.strip()
    
    if not query:
        return None, "Query cannot be empty"
    
    if len(query) > Config.MAX_QUERY_LENGTH:
        return None, f"Query too long (max {Config.MAX_QUERY_LENGTH} characters)"
    
    return query, None


def sanitize_exclude_params(exclude_str):
    """Sanitize and parse exclude parameters"""
    if not exclude_str:
        return []
    
    exclude_list = [
        e.strip().lower() 
        for e in exclude_str.split(',') 
        if e.strip()
    ]
    
    return exclude_list


def get_cached_query_vector(query):
    """Get query vector from cache or encode it"""
    global query_cache
    
    if not Config.ENABLE_QUERY_CACHE:
        return model.encode([query])
    
    # Check cache
    if query in query_cache:
        logger.debug(f"Cache hit for query: {query}")
        return query_cache[query]
    
    # Encode and cache
    query_vec = model.encode([query])
    query_cache[query] = query_vec
    
    # Limit cache size
    if len(query_cache) > Config.MAX_CACHE_SIZE:
        # Remove oldest entry (first item)
        oldest_key = next(iter(query_cache))
        del query_cache[oldest_key]
        logger.debug(f"Cache full, removed: {oldest_key}")
    
    logger.debug(f"Cached new query: {query}")
    return query_vec


# ============================================
# API ROUTES
# ============================================
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "data_loaded": df is not None,
        "total_anime": len(df) if df is not None else 0
    }
    
    status_code = 200 if status["status"] == "healthy" else 503
    return jsonify(status), status_code


@app.route('/search', methods=['GET'])
def search():
    """Search for anime using natural language query"""
    
    # Check if system is ready
    if model is None or df is None or embeddings is None:
        logger.error("Search attempted but system not initialized")
        return jsonify({
            "error": "System not initialized",
            "message": "The AI model or data is not loaded. Please check server logs."
        }), 503
    
    try:
        # Get and validate query
        query_raw = request.args.get('q')
        query, error = validate_query(query_raw)
        
        if error:
            logger.warning(f"Invalid query: {error}")
            return jsonify({"error": error}), 400
        
        logger.info(f"Search query: {query}")
        
        # Get and sanitize exclude parameters
        exclude_str = request.args.get('exclude', '')
        exclude_params = sanitize_exclude_params(exclude_str)
        
        if exclude_params:
            logger.info(f"Excluding: {exclude_params}")
        
        # Get pagination parameters
        try:
            limit = int(request.args.get('limit', Config.MAX_RESULTS))
            offset = int(request.args.get('offset', 0))
        except ValueError:
            return jsonify({"error": "Invalid limit or offset parameter"}), 400
        
        # Validate pagination parameters
        limit = min(max(limit, 1), 50)  # Between 1-50
        offset = max(offset, 0)  # Non-negative
        
        logger.info(f"Pagination: limit={limit}, offset={offset}")
        
        # 1. Convert Query -> Vector (with caching)
        query_vec = get_cached_query_vector(query)
        
        # 2. Get Similarity Scores for ALL anime
        sim_scores = cosine_similarity(query_vec, embeddings)[0]
        
        # 3. Get Top candidates (we need more because we filter and paginate)
        # Calculate how many we need to get based on offset + limit
        candidates_needed = min(offset + limit + 100, len(df))
        top_indices = np.argsort(sim_scores)[::-1][:candidates_needed]
        
        results = []
        seen_franchises = set()
        
        for idx in top_indices:
            anime = df.iloc[idx]
            title = anime['title']
            
            # Use improved franchise name extraction
            franchise_name = get_franchise_name(title)
            
            # --- LOGIC 1: BLACKLIST ---
            # If the user explicitly said "No Kimetsu", skip it
            is_excluded = False
            for bad_word in exclude_params:
                if bad_word and bad_word in title.lower():
                    is_excluded = True
                    break
            
            if is_excluded:
                continue
            
            # --- LOGIC 2: FRANCHISE DEDUPLICATION ---
            # If we already have this franchise, skip it
            if franchise_name.lower() in seen_franchises:
                continue
            
            # Add to results
            results.append({
                "title": title,
                "score": float(sim_scores[idx]),
                "synopsis": anime['synopsis'],
                "image_url": anime['main_pic'],
                "genres": anime['genres']
            })
            
            seen_franchises.add(franchise_name.lower())
            
            # Stop once we have enough results (offset + limit)
            if len(results) >= offset + limit:
                break
        
        # Apply pagination
        total_results = len(results)
        paginated_results = results[offset:offset + limit]
        
        logger.info(f"Found {total_results} total results, returning {len(paginated_results)} (offset={offset}, limit={limit})")
        
        # Handle case where no results found
        if not paginated_results and offset == 0:
            logger.warning(f"No results found for query: {query}")
            return jsonify({
                "results": [],
                "total": 0,
                "limit": limit,
                "offset": offset,
                "message": "No anime found matching your query. Try different keywords."
            }), 200
        
        # Return with pagination metadata
        return jsonify({
            "results": paginated_results,
            "total": total_results,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total_results
        })
    
    except Exception as e:
        logger.error(f"Error during search: {type(e).__name__}: {e}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while processing your search. Please try again."
        }), 500


# ============================================
# APPLICATION STARTUP
# ============================================
# Load resources at module level (for gunicorn)
logger.info("Initializing application for production...")
load_resources()

if __name__ == '__main__':
    # Load resources before starting server
    if not load_resources():
        logger.critical("Failed to load resources. Exiting.")
        sys.exit(1)
    
    # Start Flask server
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
    app.run(
        debug=Config.DEBUG,
        port=Config.PORT,
        host=Config.HOST
    )