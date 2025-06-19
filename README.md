
## 🛠️ Setup Instructions

### 1. Create a virtual environment

```bash
# On Windows
python -m venv .venv
.\.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
uvicorn app.main:app --reload
```