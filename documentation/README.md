# 🎌 Anime Picker System - Backend

An AI-powered anime recommendation system using semantic search to help users discover anime based on natural language queries.

## 🚀 Features

- **Semantic Search**: Natural language queries (e.g., "dark fantasy with strong characters")
- **Smart Filtering**: Exclude specific anime from results
- **Improved Franchise Deduplication**: Regex-based pattern matching for better grouping
- **Pagination Support**: Get more results with limit/offset parameters
- **Fast Performance**: Pre-computed embeddings for instant results
- **Robust Error Handling**: Comprehensive validation and error messages
- **Logging System**: Detailed logs for monitoring and debugging
- **Health Monitoring**: Health check endpoint for system status
- **Query Caching**: Faster responses for repeated searches

## 📋 Prerequisites

- Python 3.8 or higher
- ~15 MB of disk space for embeddings
- Internet connection (first run only, to download AI model)

## 🛠️ Installation

**Easy Way** (Recommended):

```bash
cd "d:/Anime Picker system/Backend"
.\install_requirements.ps1
# OR
install_requirements.bat
```

**Manual Way**:

1. Navigate to Backend directory
2. Activate virtual environment: `..\venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`

## ▶️ Running the Server

**Easy Way**:

```bash
.\run.ps1
# OR
run.bat
```

**Manual Way**:

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`

## 📡 API Endpoints

### 1. Health Check

**GET** `/health`

Check if the system is running properly.

**Response:**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "data_loaded": true,
  "total_anime": 3424
}
```

### 2. Search Anime

**GET** `/search`

Search for anime using natural language.

**Parameters:**

- `q` (required): Search query (max 500 characters)
- `exclude` (optional): Comma-separated titles to exclude
- **`limit` (optional)**: Number of results (1-50, default: 5) **NEW!**
- **`offset` (optional)**: Number of results to skip (default: 0) **NEW!**

**Example Requests:**

```bash
# Basic search (returns 5 results)
GET /search?q=action anime with superpowers

# Custom limit (returns 10 results)
GET /search?q=dark fantasy&limit=10

# Pagination (skip first 5, get next 5)
GET /search?q=slice of life&limit=5&offset=5

# With exclusions
GET /search?q=fantasy&exclude=berserk,attack on titan&limit=10
```

**Response:**

```json
{
  "results": [
    {
      "title": "My Hero Academia",
      "score": 0.85,
      "synopsis": "In a world where most humans have superpowers...",
      "image_url": "https://...",
      "genres": "Action, Comedy, School, Shounen, Super Power"
    }
  ],
  "total": 15,
  "limit": 5,
  "offset": 0,
  "has_more": true
}
```

**Response Fields:**

- `results`: Array of anime (paginated)
- `total`: Total number of results found
- `limit`: Requested limit
- `offset`: Requested offset
- `has_more`: Boolean indicating if more results available

**Error Responses:**

- `400`: Invalid query (empty, too long, invalid pagination params)
- `500`: Internal server error
- `503`: System not initialized

## 🔄 Regenerating Embeddings

If you update the anime dataset, regenerate embeddings:

```bash
python preprocess.py
```

This will:

1. Load `anime_clean.csv`
2. Generate embeddings for all anime
3. Save to `anime_embeddings.pkl`
4. Verify the saved file

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Search Settings
MAX_RESULTS = 5              # Default number of results
CANDIDATE_POOL_SIZE = 50     # Initial candidates to filter
MAX_QUERY_LENGTH = 500       # Maximum query length

# Server Settings
PORT = 5000
DEBUG = True
HOST = '127.0.0.1'

# Cache Settings
ENABLE_QUERY_CACHE = True
MAX_CACHE_SIZE = 100
```

Or use environment variables (create a `.env` file):

```bash
PORT=5000
HOST=127.0.0.1
DEBUG=True
```

## 📝 Logging

Logs are written to:

- **Console**: Real-time output
- **File**: `anime_picker.log`

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

Example:

```
2025-11-20 14:25:33 - __main__ - INFO - Search query: dark fantasy
2025-11-20 14:25:33 - __main__ - INFO - Pagination: limit=10, offset=0
2025-11-20 14:25:33 - __main__ - INFO - Found 15 total results, returning 10
```

## 🔍 How It Works

1. **Pre-processing** (done once):

   - Anime descriptions are converted to 768-dimensional embeddings
   - Stored in `anime_embeddings.pkl` (~14 MB)

2. **Search Process**:

   - User query → Converted to vector embedding
   - Compare with all anime embeddings (cosine similarity)
   - Filter excluded titles
   - Deduplicate franchises (using regex patterns)
   - Apply pagination
   - Return results with metadata

3. **Performance**:
   - Model stays in memory (no reload per request)
   - Query caching for repeated searches
   - Typical response time: <100ms

## 🎯 Franchise Deduplication

The system uses regex patterns to group franchise variants:

**Examples:**

- "Attack on Titan Season 2" → "Attack on Titan"
- "Sword Art Online: Alicization" → "Sword Art Online"
- "My Hero Academia Movie" → "My Hero Academia"
- "Re:Zero" → "Re:Zero" (special handling)

**Patterns matched:**

- Season numbers (Season 2, 2nd Season, etc.)
- Parts (Part 1, Part 2, etc.)
- Movies, OVAs, Specials
- Years in parentheses

## 🛡️ Error Handling

The system handles:

- ✅ Missing data files
- ✅ Invalid queries
- ✅ Model loading failures
- ✅ Invalid pagination parameters
- ✅ Malformed requests

All errors are logged with detailed information.

## 📊 System Requirements

**Memory**: ~500 MB RAM

- AI Model: ~400 MB
- Embeddings: ~15 MB
- Flask overhead: ~50 MB

**CPU**: Any modern processor (no GPU required)

## 🐛 Troubleshooting

### Server won't start

```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Use different port in config.py
PORT = 5001
```

### "File not found" error

```bash
# Verify files exist
ls anime_embeddings.pkl
ls anime_clean.csv

# Regenerate embeddings if needed
python preprocess.py
```

### Model download fails

```bash
# Ensure internet connection
# Model downloads automatically on first run (~400 MB)
```

## 📈 Performance Tips

1. **Keep server running**: Model loads once and stays in memory
2. **Use query caching**: Enabled by default
3. **Adjust candidate pool**: Increase `CANDIDATE_POOL_SIZE` for better results (slower)
4. **Disable debug mode**: Set `DEBUG=False` in production
5. **Use pagination**: Request only what you need

## 📦 Project Structure

```
Backend/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── preprocess.py             # Embedding generation script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── anime_embeddings.pkl     # Pre-computed embeddings (14 MB)
├── anime_clean.csv          # Anime dataset (4.4 MB)
├── run.ps1 / run.bat        # Helper scripts to run app
└── install_requirements.ps1/bat  # Helper scripts to install deps
```

## 🎯 Recent Improvements

### High Priority ✅

- Error handling
- Configuration management
- Input validation
- Logging system
- Pinned dependencies

### Medium Priority ✅

- Improved franchise deduplication (regex-based)
- Pagination support (limit/offset)
- Preprocessing script (separate embedding generation)
- Health check endpoint

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Contributions welcome! Please ensure:

- Code follows existing style
- Error handling is comprehensive
- Logging is informative
- Documentation is updated

---

**Built with ❤️ using Flask, Sentence Transformers, and scikit-learn**
