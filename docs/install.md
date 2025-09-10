
# Installation Guide

This guide explains how to set up the Framework.

---

## 1. Clone the Repository

```bash
    git clone https://github.com/alexhenriquepv/vesta-framework.git
    cd vesta-framework
```

## 2. Setup Virtual Environment
```bash
    python -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .venv\Scripts\activate      # Windows
```

## 3. Install Dependencies
```bash
  pip install -r requirements.txt
```

## 4. Configure Environment Variables
Create a ```.env``` file in the root folder:
```ini
GOOGLE_API_KEY=your_api_key_here
```

## 5. Run the service
```bash
  uvicorn main:app --reload
```

Open Swagger UI:

👉 http://127.0.0.1:8000/docs