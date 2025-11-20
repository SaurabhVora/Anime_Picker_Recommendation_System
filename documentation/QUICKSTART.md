# ⚡ Quick Start Guide

Get Anime Picker running in **under 5 minutes**!

---

## 🎯 Prerequisites

- **Python 3.13+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **4 GB RAM** minimum

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/anime-picker.git
cd anime-picker
```

### 2️⃣ Backend Setup (2 minutes)

```bash
# Navigate to backend
cd Backend

# Create virtual environment
python -m venv ../venv

# Activate virtual environment
# Windows:
..\venv\Scripts\activate
# macOS/Linux:
source ../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate embeddings (one-time, ~1 minute)
python preprocess.py

# Start backend
python app.py
```

✅ **Backend running at:** `http://127.0.0.1:5000`

### 3️⃣ Frontend Setup (2 minutes)

Open a **new terminal** window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

✅ **Frontend running at:** `http://localhost:3000`

---

## 🎉 You're Done!

Open your browser and visit: **http://localhost:3000**

Try searching for:

- "action anime"
- "sad romance"
- "dark fantasy"

---

## 🐛 Troubleshooting

### Backend won't start?

```bash
# Check Python version
python --version  # Should be 3.13+

# Verify virtual environment is activated
# You should see (venv) in your terminal

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start?

```bash
# Check Node version
node -v  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "Could not connect to server" error?

Make sure the **backend is running** on port 5000:

```bash
curl http://127.0.0.1:5000/health
```

---

## 📚 Next Steps

- Read the [full README](README.md) for detailed information
- Check [Backend docs](Backend/README.md) for API details
- Check [Frontend docs](frontend/README.md) for customization
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

---

## 🎯 Quick Commands

### Backend

```bash
cd Backend
python app.py              # Start server
python preprocess.py       # Regenerate embeddings
```

### Frontend

```bash
cd frontend
npm run dev               # Development server
npm run build             # Production build
npm run lint              # Check code quality
```

---

**Need help?** [Open an issue](https://github.com/yourusername/anime-picker/issues)

**Happy searching! 🎭**
