"use client";

import { useState, useEffect, useCallback } from "react";
import Image from "next/image";
import { Search, Sparkles, Star, AlertCircle } from "lucide-react";
import styles from "./page.module.css";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [debouncedQuery, setDebouncedQuery] = useState("");

  const fetchAnime = useCallback(async (searchQuery) => {
    setLoading(true);
    setError(null);
    try {
      const API_URL =
        process.env.NEXT_PUBLIC_API_URL ||
        "https://anime-picker-backend.onrender.com";
      const response = await fetch(
        `${API_URL}/search?q=${encodeURIComponent(searchQuery)}&limit=12`
      );
      const data = await response.json();

      if (response.ok) {
        setResults(data.results || []);
      } else {
        setError(data.error || "Failed to fetch results");
      }
    } catch (err) {
      setError("Could not connect to the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  // Fetch data when debounced query changes
  useEffect(() => {
    if (debouncedQuery.trim().length < 2) {
      setResults([]);
      return;
    }
    fetchAnime(debouncedQuery);
  }, [debouncedQuery, fetchAnime]);

  return (
    <main className={styles.main}>
      {/* Hero Section */}
      <section className={styles.heroSection}>
        {/* Background Glow */}
        <div className={styles.heroGlow} />

        <div className={styles.heroContent}>
          <div className={styles.badge}>
            <Sparkles
              size={16}
              className="text-accent"
              style={{ color: "var(--accent)" }}
            />
            <span className={styles.badgeText}>AI-Powered Recommendations</span>
          </div>

          <h1 className={styles.title}>
            Find Your Next <br />
            <span className="text-gradient">Anime Obsession</span>
          </h1>

          <p className={styles.subtitle}>
            Describe what you want to watch in natural language.
            <br />
            &quot;Dark fantasy with a complex villain&quot; or &quot;Wholesome
            slice of life&quot;.
          </p>

          {/* Search Bar */}
          <div className={styles.searchWrapper}>
            <div className={styles.searchGlow} />
            <div className={styles.searchContainer}>
              <Search size={24} style={{ color: "#9ca3af" }} />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="What are you in the mood for?"
                className={styles.searchInput}
                autoFocus
              />
              {loading && <div className={styles.spinner} />}
            </div>
          </div>
        </div>
      </section>

      {/* Results Section */}
      <section className={styles.resultsSection}>
        {error && (
          <div className={styles.error}>
            <AlertCircle size={20} />
            <p>{error}</p>
          </div>
        )}

        {results.length > 0 ? (
          <div className={styles.grid}>
            {results.map((anime, index) => (
              <div key={index} className={styles.card}>
                {/* Image Container */}
                <div className={styles.imageContainer}>
                  <Image
                    src={anime.image_url}
                    alt={anime.title}
                    fill
                    className={styles.cardImage}
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                  />
                  {/* Overlay Gradient */}
                  <div className={styles.overlay} />

                  {/* Score Badge */}
                  <div className={styles.scoreBadge}>
                    <Star size={14} fill="#facc15" color="#facc15" />
                    <span>{Math.round(anime.score * 100)}% Match</span>
                  </div>
                </div>

                {/* Content */}
                <div className={styles.cardContent}>
                  <h3 className={styles.cardTitle}>{anime.title}</h3>

                  <div className={styles.genres}>
                    {anime.genres
                      .split(",")
                      .slice(0, 3)
                      .map((genre, i) => (
                        <span key={i} className={styles.genreTag}>
                          {genre.trim()}
                        </span>
                      ))}
                  </div>

                  <p className={styles.synopsis}>{anime.synopsis}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          !loading &&
          query.length > 2 && (
            <div className={styles.emptyState}>
              <p>No anime found matching your description.</p>
              <p style={{ fontSize: "0.875rem", marginTop: "0.5rem" }}>
                Try different keywords like &quot;cyberpunk&quot; or &quot;high
                school romance&quot;
              </p>
            </div>
          )
        )}
      </section>
    </main>
  );
}
