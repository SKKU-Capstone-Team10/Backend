<div align="center">
  <h1>🚀 Capstone Backend</h1>
  <p>Streamlit‑powered AI chatbot &amp; data‑viz web application</p>
</div>

<br><hr><br>

<h2>🛠️ Setup</h2>

<pre><code># 1 – Create &amp; activate virtual env
Python version 3.12.7
python3 -m venv [name]
source [name]/bin/activate

# 2 – Install dependencies
pip install -r requirements.txt
</code></pre>

<br><hr><br>

<h2>⚙️ Environment Variable</h2>
Create a environment vairable named <code>.env</code><br>
Fill the content like below
<pre><code>
PASSWORD_ALGORITHM=[Your Hashing Algorithm Here]
SECRET_KEY=[Your Random Secret Key Here]
ACCESS_TOKEN_EXPIRE_MINUTES=11520
FRONTEND_HOST="0.0.0.0"
RAG_HOST="http://127.0.0.1:8001"
RAG_ROUTE="/api/rag/"
</code></pre>

<h2>⚡ Run</h2>

<pre><code>uvicorn main:app --port 8000</code></pre>

<br><hr><br>
## 📁 Project Structure

### 🔹 Top-Level Files

| File                   | Purpose                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `main.py`              | **Main entry point** – FastAPI app controller and page router           |
| `models.py`            | DB Table specification                                                  |
| `requirements.txt`     | Python dependency list (pip)                                            |
| `.env`                 | You must create it.                                                     |

---

### 🔸 Modules & Subdirectories

| Folder              | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `api/`              | API routers, End Points are defined here                                |
| `core/`             | Loading `.env` / DB Set-up / Authentification Modules                   |
| `crud/`             | Controllers, Directly interact with DB                                  |
| `schemas/`          | Req & Res data field definitions                                        |

---

<div align="center">
  <i>Capstone Team 10 · Sungkyunkwan University</i>
</div>
