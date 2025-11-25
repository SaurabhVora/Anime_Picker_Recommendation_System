# 🎨 Anime Picker - Frontend

A stunning, modern React frontend for the Anime Picker AI-powered recommendation system.

---

## 🌟 Features

### **Core Functionality**

- ✅ **AI-Powered Search**: Natural language anime search using semantic understanding
- ✅ **Real-time Results**: Debounced search with instant feedback
- ✅ **Responsive Grid**: Beautiful card layout that adapts to all screen sizes
- ✅ **Image Optimization**: Next.js Image component for fast loading

### **Design & UX**

- ✅ **Cinematic Dark Mode**: Deep, rich color palette with vibrant accents
- ✅ **Glassmorphism**: Translucent UI elements with blur effects
- ✅ **Smooth Animations**: Hover effects, transitions, and micro-interactions
- ✅ **Premium Typography**: Clean, modern font stack
- ✅ **Match Scores**: Visual indicators showing relevance percentage

---

## 🛠️ Tech Stack

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| **Next.js 15**   | React framework with SSR capabilities |
| **React 19**     | UI library                            |
| **Vanilla CSS**  | Styling (CSS Modules + Global Styles) |
| **Lucide React** | Icon library                          |
| **Next/Image**   | Optimized image loading               |

---

## 📁 Project Structure

```
frontend/
├── src/
│   └── app/
│       ├── layout.js           # Root layout with metadata
│       ├── page.js             # Main search page
│       ├── page.module.css     # Component-specific styles
│       └── globals.css         # Global styles & design system
├── public/                     # Static assets
├── next.config.js              # Next.js configuration
├── package.json                # Dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### **Prerequisites**

- Node.js 18+ (you have v22.13.1 ✅)
- Backend API running on `http://127.0.0.1:5000`

### **Installation**

```bash
# Navigate to frontend directory
cd "d:/Anime Picker system/frontend"

# Install dependencies (already done)
npm install

# Start development server
npm run dev
```

The app will be available at **http://localhost:3000**

---

## 📜 Available Scripts

| Command         | Description                               |
| --------------- | ----------------------------------------- |
| `npm run dev`   | Start development server (with Turbopack) |
| `npm run build` | Build for production                      |
| `npm start`     | Start production server                   |
| `npm run lint`  | Run ESLint to check code quality          |

---

## 🎨 Design System

### **Color Palette**

```css
--bg-deep: #0a0a12        /* Almost black background */
--bg-card: #151520        /* Card background */
--bg-glass: rgba(21, 21, 32, 0.7)  /* Glassmorphism */

--primary: #8b5cf6        /* Vivid Violet */
--accent: #ec4899         /* Hot Pink */

--text-main: #ffffff      /* White text */
--text-muted: #94a3b8     /* Muted gray */
```

### **Typography**

- **Font Family**: Inter, system fonts
- **Sizes**: Responsive (3rem - 4.5rem for titles)

### **Effects**

- **Border Radius**: 16px (cards), 9999px (pills)
- **Transitions**: 0.3s cubic-bezier easing
- **Blur**: 12px for glassmorphism

---

## 🔌 API Integration

### **Backend Connection**

The frontend connects to the Flask backend at:

```javascript
http://127.0.0.1:5000/search?q={query}&limit=12
```

### **Expected Response Format**

```json
{
  "results": [
    {
      "title": "My Hero Academia",
      "score": 0.85,
      "synopsis": "Description...",
      "image_url": "https://cdn.myanimelist.net/...",
      "genres": "Action, Comedy, School"
    }
  ],
  "total": 15,
  "limit": 12,
  "offset": 0,
  "has_more": true
}
```

### **Error Handling**

The app gracefully handles:

- Backend offline (connection errors)
- Invalid responses
- Empty results
- Network timeouts

---

## 🧩 Component Breakdown

### **Main Page (`page.js`)**

**State Management:**

```javascript
- query: Current search input
- debouncedQuery: Debounced version (500ms delay)
- results: Array of anime objects
- loading: Boolean for loading state
- error: Error message string
```

**Key Features:**

- Debounced search (waits 500ms after typing stops)
- `useCallback` for optimized re-renders
- Responsive grid (1-4 columns based on screen size)

### **Styling (`page.module.css`)**

**Key Classes:**

- `.heroSection` - Top section with search
- `.searchContainer` - Glassmorphism search bar
- `.grid` - Responsive anime grid
- `.card` - Individual anime card with hover effects
- `.scoreBadge` - Match percentage indicator

---

## 📱 Responsive Breakpoints

| Screen Size     | Grid Columns | Description   |
| --------------- | ------------ | ------------- |
| < 640px         | 1 column     | Mobile        |
| 640px - 1024px  | 2 columns    | Tablet        |
| 1024px - 1280px | 3 columns    | Small desktop |
| 1280px+         | 4 columns    | Large desktop |

---

## 🎯 Key Features Explained

### **1. Debounced Search**

Waits 500ms after user stops typing before making API call:

```javascript
useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedQuery(query);
  }, 500);
  return () => clearTimeout(timer);
}, [query]);
```

### **2. Image Optimization**

Uses Next.js Image component for automatic optimization:

```javascript
<Image
  src={anime.image_url}
  alt={anime.title}
  fill
  sizes="(max-width: 768px) 100vw, 33vw"
/>
```

### **3. Glassmorphism Effect**

CSS-based translucent panels:

```css
background: rgba(21, 21, 32, 0.7);
backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.1);
```

---

## 🐛 Troubleshooting

### **"Could not connect to server" Error**

**Solution:**

1. Ensure backend is running:
   ```bash
   cd "../Backend"
   python app.py
   ```
2. Check backend is on port 5000
3. Verify CORS is enabled in backend

### **Images Not Loading**

**Solution:**

1. Check `next.config.js` has correct domain:
   ```javascript
   hostname: "cdn.myanimelist.net";
   ```
2. Verify image URLs in backend response

### **Styles Not Applying**

**Solution:**

1. Clear Next.js cache:
   ```bash
   rm -rf .next
   npm run dev
   ```
2. Check CSS module imports are correct

---

## 🐳 Running with Docker

This frontend is part of the Docker Compose setup. See the main [DOCKER_README.md](../DOCKER_README.md) for complete instructions.

To run the entire application:

```bash
# From project root
docker-compose up
```

The frontend will be available at **http://localhost:3000**

---

## 🔧 Configuration

### **Backend URL**

The frontend connects to the backend API. The default is configured for Docker Compose:

```javascript
// In page.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";
```

**For different setups:**

- **Docker Compose** (default): `http://localhost:5000`
- **Local development** (both running locally): `http://127.0.0.1:5000`
- **Custom setup**: Set `NEXT_PUBLIC_API_URL` environment variable

### **Results Limit**

Change the number of results per search:

```javascript
// In page.js, line 19
&limit=12  // Change to desired number (max 50)
```

---

## 📊 Performance

### **Lighthouse Scores (Target)**

- Performance: 95+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

### **Optimizations Applied**

- ✅ Image lazy loading
- ✅ CSS-in-JS avoided (using CSS modules)
- ✅ Debounced API calls
- ✅ Minimal JavaScript bundle
- ✅ Static generation where possible

---

## 🎨 Customization

### **Change Color Scheme**

Edit `globals.css`:

```css
:root {
  --primary: #your-color;
  --accent: #your-accent;
}
```

### **Modify Card Layout**

Edit `page.module.css`:

```css
.grid {
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem; /* Increase spacing */
}
```

---

## 🧪 Testing

### **Manual Testing Checklist**

- [ ] Search with various queries
- [ ] Test on mobile, tablet, desktop
- [ ] Verify images load correctly
- [ ] Check error states (backend offline)
- [ ] Test empty results
- [ ] Verify hover effects work
- [ ] Check loading states

### **Browser Compatibility**

Tested on:

- ✅ Chrome 120+
- ✅ Firefox 120+
- ✅ Safari 17+
- ✅ Edge 120+

---

## 📝 Code Quality

### **Linting**

```bash
npm run lint
```

All code passes ESLint with:

- ✅ No errors
- ✅ No warnings
- ✅ React best practices enforced

### **Build Verification**

```bash
npm run build
```

Build completes successfully with:

- ✅ Static page generation
- ✅ No TypeScript errors (using JavaScript)
- ✅ Optimized bundle size

---

## 🔮 Future Enhancements

### **Planned Features**

- [ ] "Load More" pagination button
- [ ] Filter by genre/year
- [ ] Anime detail modal
- [ ] Favorites/watchlist
- [ ] Dark/light mode toggle
- [ ] Search history
- [ ] Share results

---

## 📞 Support

### **Common Issues**

**Q: Why is the search slow?**  
A: The 500ms debounce is intentional to reduce API calls. Adjust in `page.js` if needed.

**Q: Can I use this with a different backend?**  
A: Yes! Just update the API URL and ensure the response format matches.

**Q: How do I add more anime per page?**  
A: Change `&limit=12` to a higher number (max 50).

---

## 📄 License

This project is part of the Anime Picker System.

---

## 🙏 Acknowledgments

- **MyAnimeList** for anime images
- **Lucide** for beautiful icons
- **Next.js** team for the amazing framework

---

**Frontend Version:** 1.0.0  
**Last Updated:** 2025-11-20  
**Status:** ✅ Production Ready
