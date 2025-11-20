# 📡 Anime Picker System - API Documentation

**Version:** 1.0  
**Base URL:** `http://127.0.0.1:5000` (Development)  
**Production URL:** `https://your-domain.com/api` (To be configured)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
   - [Health Check](#1-health-check)
   - [Search Anime](#2-search-anime)
4. [Response Formats](#response-formats)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [CORS Policy](#cors-policy)
8. [Frontend Integration Examples](#frontend-integration-examples)

---

## Overview

The Anime Picker API provides semantic search capabilities for anime recommendations using AI-powered natural language processing. The API returns anime suggestions based on user queries with support for filtering, exclusions, and pagination.

**Key Features:**

- Natural language search
- Semantic similarity matching
- Franchise deduplication
- Pagination support
- Exclusion filters
- Fast response times (<100ms)

---

## Authentication

**Current:** No authentication required (Development)  
**Production:** Will require API key (To be implemented)

For production deployment, you'll need to add:

```http
Authorization: Bearer YOUR_API_KEY
```

---

## Endpoints

### 1. Health Check

Check if the API server is running and ready to handle requests.

#### **Request**

```http
GET /health
```

#### **Parameters**

None

#### **Response**

**Success (200 OK)**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "data_loaded": true,
  "total_anime": 3424
}
```

**Unhealthy (503 Service Unavailable)**

```json
{
  "status": "unhealthy",
  "model_loaded": false,
  "data_loaded": false,
  "total_anime": 0
}
```

#### **Response Fields**

| Field          | Type    | Description                       |
| -------------- | ------- | --------------------------------- |
| `status`       | string  | "healthy" or "unhealthy"          |
| `model_loaded` | boolean | Whether AI model is loaded        |
| `data_loaded`  | boolean | Whether anime data is loaded      |
| `total_anime`  | integer | Total number of anime in database |

#### **Example Usage**

```javascript
// JavaScript/Fetch
fetch("http://127.0.0.1:5000/health")
  .then((response) => response.json())
  .then((data) => console.log(data));

// Axios
axios
  .get("http://127.0.0.1:5000/health")
  .then((response) => console.log(response.data));
```

---

### 2. Search Anime

Search for anime using natural language queries with optional filters and pagination.

#### **Request**

```http
GET /search?q={query}&limit={limit}&offset={offset}&exclude={titles}
```

#### **Parameters**

| Parameter | Type    | Required | Default | Description                       |
| --------- | ------- | -------- | ------- | --------------------------------- |
| `q`       | string  | **Yes**  | -       | Search query (max 500 chars)      |
| `limit`   | integer | No       | 5       | Number of results (1-50)          |
| `offset`  | integer | No       | 0       | Number of results to skip         |
| `exclude` | string  | No       | -       | Comma-separated titles to exclude |

#### **Query Examples**

```http
# Basic search
GET /search?q=action anime with superpowers

# With limit
GET /search?q=dark fantasy&limit=10

# With pagination
GET /search?q=slice of life&limit=5&offset=5

# With exclusions
GET /search?q=fantasy adventure&exclude=sword art online,naruto

# Complete example
GET /search?q=romantic comedy&limit=10&offset=0&exclude=toradora
```

#### **Response**

**Success (200 OK)**

```json
{
  "results": [
    {
      "title": "My Hero Academia",
      "score": 0.8547,
      "synopsis": "In a world where most humans have superpowers called 'Quirks', Izuku Midoriya dreams of becoming a hero despite being born without powers...",
      "image_url": "https://cdn.myanimelist.net/images/anime/10/78745.jpg",
      "genres": "Action, Comedy, School, Shounen, Super Power"
    },
    {
      "title": "One Punch Man",
      "score": 0.8234,
      "synopsis": "Saitama is a hero who only became a hero for fun. After three years of special training...",
      "image_url": "https://cdn.myanimelist.net/images/anime/12/76049.jpg",
      "genres": "Action, Comedy, Parody, Sci-Fi, Seinen, Super Power, Supernatural"
    }
  ],
  "total": 15,
  "limit": 5,
  "offset": 0,
  "has_more": true
}
```

**No Results (200 OK)**

```json
{
  "results": [],
  "total": 0,
  "limit": 5,
  "offset": 0,
  "message": "No anime found matching your query. Try different keywords."
}
```

#### **Response Fields**

**Root Level:**

| Field      | Type    | Description                             |
| ---------- | ------- | --------------------------------------- |
| `results`  | array   | Array of anime objects                  |
| `total`    | integer | Total number of results found           |
| `limit`    | integer | Requested limit                         |
| `offset`   | integer | Requested offset                        |
| `has_more` | boolean | Whether more results are available      |
| `message`  | string  | Optional message (only when no results) |

**Anime Object:**

| Field       | Type   | Description                              |
| ----------- | ------ | ---------------------------------------- |
| `title`     | string | Anime title                              |
| `score`     | float  | Similarity score (0-1, higher is better) |
| `synopsis`  | string | Anime description/plot summary           |
| `image_url` | string | URL to anime cover image                 |
| `genres`    | string | Pipe-separated list of genres            |

#### **Example Usage**

```javascript
// JavaScript/Fetch
const searchAnime = async (query, limit = 5, offset = 0) => {
  const params = new URLSearchParams({
    q: query,
    limit: limit,
    offset: offset,
  });

  const response = await fetch(`http://127.0.0.1:5000/search?${params}`);
  const data = await response.json();
  return data;
};

// Usage
searchAnime("action anime", 10, 0).then((data) => {
  console.log(`Found ${data.total} results`);
  data.results.forEach((anime) => {
    console.log(`${anime.title} (${anime.score})`);
  });
});

// React Example
const [animeList, setAnimeList] = useState([]);
const [loading, setLoading] = useState(false);

const handleSearch = async (query) => {
  setLoading(true);
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}&limit=10`
    );
    const data = await response.json();
    setAnimeList(data.results);
  } catch (error) {
    console.error("Search failed:", error);
  } finally {
    setLoading(false);
  }
};
```

---

## Response Formats

### Success Response Structure

All successful responses follow this structure:

```json
{
  "results": [...],
  "total": 0,
  "limit": 5,
  "offset": 0,
  "has_more": false
}
```

### Error Response Structure

All error responses follow this structure:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning               | Description            |
| ---- | --------------------- | ---------------------- |
| 200  | OK                    | Request successful     |
| 400  | Bad Request           | Invalid parameters     |
| 500  | Internal Server Error | Server error           |
| 503  | Service Unavailable   | System not initialized |

### Error Examples

**400 - Missing Query Parameter**

```json
{
  "error": "Query parameter 'q' is required"
}
```

**400 - Query Too Long**

```json
{
  "error": "Query too long (max 500 characters)"
}
```

**400 - Invalid Pagination**

```json
{
  "error": "Invalid limit or offset parameter"
}
```

**503 - System Not Ready**

```json
{
  "error": "System not initialized",
  "message": "The AI model or data is not loaded. Please check server logs."
}
```

**500 - Internal Error**

```json
{
  "error": "Internal server error",
  "message": "An error occurred while processing your search. Please try again."
}
```

### Frontend Error Handling

```javascript
const searchAnime = async (query) => {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Search failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Search error:", error.message);
    // Show error to user
    return { results: [], total: 0, error: error.message };
  }
};
```

---

## Rate Limiting

**Current:** No rate limiting (Development)  
**Production:** To be implemented

Recommended limits for production:

- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## CORS Policy

**Current:** CORS enabled for all origins (Development)

```python
CORS(app)  # Allows all origins
```

**Production:** Restrict to your frontend domain

```python
CORS(app, origins=["https://your-frontend-domain.com"])
```

---

## Frontend Integration Examples

### React Component Example

```jsx
import React, { useState, useEffect } from "react";

const API_BASE_URL = "http://127.0.0.1:5000";

function AnimeSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(false);

  const LIMIT = 10;

  const searchAnime = async (searchQuery, offset = 0) => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        q: searchQuery,
        limit: LIMIT,
        offset: offset,
      });

      const response = await fetch(`${API_BASE_URL}/search?${params}`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Search failed");
      }

      const data = await response.json();

      if (offset === 0) {
        setResults(data.results);
      } else {
        setResults((prev) => [...prev, ...data.results]);
      }

      setHasMore(data.has_more);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(0);
    searchAnime(query, 0);
  };

  const loadMore = () => {
    const newPage = page + 1;
    setPage(newPage);
    searchAnime(query, newPage * LIMIT);
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search anime..."
        />
        <button type="submit">Search</button>
      </form>

      {error && <div className="error">{error}</div>}

      {loading && <div>Loading...</div>}

      <div className="results">
        {results.map((anime, index) => (
          <div key={index} className="anime-card">
            <img src={anime.image_url} alt={anime.title} />
            <h3>{anime.title}</h3>
            <p className="score">Score: {(anime.score * 100).toFixed(1)}%</p>
            <p className="genres">{anime.genres}</p>
            <p className="synopsis">{anime.synopsis}</p>
          </div>
        ))}
      </div>

      {hasMore && !loading && <button onClick={loadMore}>Load More</button>}
    </div>
  );
}

export default AnimeSearch;
```

### Vue.js Example

```vue
<template>
  <div class="anime-search">
    <form @submit.prevent="handleSearch">
      <input v-model="query" placeholder="Search anime..." />
      <button type="submit">Search</button>
    </form>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="loading">Loading...</div>

    <div class="results">
      <div v-for="anime in results" :key="anime.title" class="anime-card">
        <img :src="anime.image_url" :alt="anime.title" />
        <h3>{{ anime.title }}</h3>
        <p>Score: {{ (anime.score * 100).toFixed(1) }}%</p>
        <p>{{ anime.synopsis }}</p>
      </div>
    </div>

    <button v-if="hasMore && !loading" @click="loadMore">Load More</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: "",
      results: [],
      loading: false,
      error: null,
      page: 0,
      hasMore: false,
      LIMIT: 10,
      API_BASE_URL: "http://127.0.0.1:5000",
    };
  },
  methods: {
    async searchAnime(searchQuery, offset = 0) {
      this.loading = true;
      this.error = null;

      try {
        const params = new URLSearchParams({
          q: searchQuery,
          limit: this.LIMIT,
          offset: offset,
        });

        const response = await fetch(`${this.API_BASE_URL}/search?${params}`);
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Search failed");
        }

        if (offset === 0) {
          this.results = data.results;
        } else {
          this.results = [...this.results, ...data.results];
        }

        this.hasMore = data.has_more;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    handleSearch() {
      this.page = 0;
      this.searchAnime(this.query, 0);
    },
    loadMore() {
      this.page++;
      this.searchAnime(this.query, this.page * this.LIMIT);
    },
  },
};
</script>
```

### Vanilla JavaScript Example

```javascript
const API_BASE_URL = "http://127.0.0.1:5000";
let currentPage = 0;
let currentQuery = "";
const LIMIT = 10;

async function searchAnime(query, offset = 0) {
  const params = new URLSearchParams({
    q: query,
    limit: LIMIT,
    offset: offset,
  });

  try {
    const response = await fetch(`${API_BASE_URL}/search?${params}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Search failed");
    }

    return data;
  } catch (error) {
    console.error("Search error:", error);
    throw error;
  }
}

function displayResults(data, append = false) {
  const container = document.getElementById("results");

  if (!append) {
    container.innerHTML = "";
  }

  data.results.forEach((anime) => {
    const card = document.createElement("div");
    card.className = "anime-card";
    card.innerHTML = `
      <img src="${anime.image_url}" alt="${anime.title}">
      <h3>${anime.title}</h3>
      <p class="score">Score: ${(anime.score * 100).toFixed(1)}%</p>
      <p class="genres">${anime.genres}</p>
      <p class="synopsis">${anime.synopsis}</p>
    `;
    container.appendChild(card);
  });

  // Show/hide load more button
  const loadMoreBtn = document.getElementById("load-more");
  loadMoreBtn.style.display = data.has_more ? "block" : "none";
}

document.getElementById("search-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  currentQuery = document.getElementById("search-input").value;
  currentPage = 0;

  try {
    const data = await searchAnime(currentQuery, 0);
    displayResults(data, false);
  } catch (error) {
    alert("Search failed: " + error.message);
  }
});

document.getElementById("load-more").addEventListener("click", async () => {
  currentPage++;

  try {
    const data = await searchAnime(currentQuery, currentPage * LIMIT);
    displayResults(data, true);
  } catch (error) {
    alert("Failed to load more: " + error.message);
  }
});
```

---

## Best Practices

### 1. **URL Encoding**

Always encode query parameters:

```javascript
const query = "action & adventure";
const encoded = encodeURIComponent(query);
fetch(`/search?q=${encoded}`);
```

### 2. **Debouncing Search**

Avoid excessive API calls:

```javascript
let searchTimeout;
const debouncedSearch = (query) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    searchAnime(query);
  }, 300); // Wait 300ms after user stops typing
};
```

### 3. **Loading States**

Always show loading indicators:

```javascript
setLoading(true);
try {
  const data = await searchAnime(query);
  // Handle data
} finally {
  setLoading(false);
}
```

### 4. **Error Handling**

Provide user-friendly error messages:

```javascript
try {
  const data = await searchAnime(query);
} catch (error) {
  showError("Unable to search. Please try again.");
}
```

### 5. **Caching**

Cache results to reduce API calls:

```javascript
const cache = new Map();

async function searchWithCache(query) {
  if (cache.has(query)) {
    return cache.get(query);
  }

  const data = await searchAnime(query);
  cache.set(query, data);
  return data;
}
```

---

## Testing the API

### Using cURL

```bash
# Health check
curl http://127.0.0.1:5000/health

# Basic search
curl "http://127.0.0.1:5000/search?q=action+anime"

# With pagination
curl "http://127.0.0.1:5000/search?q=fantasy&limit=10&offset=0"

# With exclusions
curl "http://127.0.0.1:5000/search?q=adventure&exclude=naruto,one+piece"
```

### Using Postman

1. **Health Check**

   - Method: GET
   - URL: `http://127.0.0.1:5000/health`

2. **Search**
   - Method: GET
   - URL: `http://127.0.0.1:5000/search`
   - Params:
     - q: "action anime"
     - limit: 10
     - offset: 0

---

## Deployment Considerations

### Environment Variables

Create `.env` file for production:

```bash
PORT=5000
HOST=0.0.0.0
DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.com
```

### Production Checklist

- [ ] Set `DEBUG=False` in config
- [ ] Configure CORS for specific origins
- [ ] Add API authentication
- [ ] Implement rate limiting
- [ ] Set up HTTPS
- [ ] Configure logging
- [ ] Add monitoring
- [ ] Set up error tracking (e.g., Sentry)

---

## Support

For issues or questions:

- Check logs in `anime_picker.log`
- Verify server is running: `GET /health`
- Ensure all dependencies are installed

---

**API Version:** 1.0  
**Last Updated:** 2025-11-20  
**Status:** Production Ready ✅
