# 📸 Screenshots Folder

## Instructions

This folder is for storing screenshots of your Anime Picker application.

### Required Screenshots:

1. **search-interface.png** - Screenshot of the main search interface

   - Show the hero section with the search bar
   - Include the glassmorphism effects
   - Capture the gradient background glow

2. **results-grid.png** - Screenshot of the search results
   - Show the anime cards in grid layout
   - Include match scores and genre tags
   - Capture hover effects if possible

### How to Take Screenshots:

1. **Run the application:**

   ```bash
   # Terminal 1 - Backend
   cd Backend
   python app.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Open browser:** http://localhost:3000

3. **For search-interface.png:**

   - Take a full-page screenshot of the initial page
   - Use browser dev tools (F12) → Device toolbar for consistent sizing
   - Recommended size: 1920x1080 or 1280x720

4. **For results-grid.png:**
   - Search for something like "action anime"
   - Wait for results to load
   - Take a screenshot showing the grid of anime cards
   - Recommended size: 1920x1080 or 1280x720

### Tools for Screenshots:

- **Windows:** Windows + Shift + S (Snipping Tool)
- **macOS:** Cmd + Shift + 4
- **Browser:** F12 → Device toolbar → Screenshot icon
- **Extensions:** Awesome Screenshot, Fireshot

### After Adding Screenshots:

```bash
cd "d:/Anime Picker system"
git add screenshots/
git commit -m "Add screenshots for README"
git push origin main
```

Your README will automatically display the screenshots on GitHub!
