# 🧠 MemOS — Enterprise Communications & Document Memory System

**MemOS** is an enterprise-grade AI memory and retrieval-augmented generation (RAG) platform. It is engineered to ingest high-volume enterprise communications—such as corporate emails (Outlook/Office 365, Gmail, IMAP) and organizational documents (PDFs, reports)—into a vector database ([Qdrant](https://qdrant.tech/)), enabling conversational querying and instant question-answering powered by Large Language Models (LLMs).

---

## 📊 Project Completion Status & Audit

Below is a transparent breakdown of what is currently implemented, partially completed, and planned for future phases:

| Component | Status | Completion % | Details |
| :--- | :---: | :---: | :--- |
| **PDF Ingestion Pipeline** | 🟢 Operational | **90%** | Django upload UI & REST API, asynchronous Celery task queue via Redis, PyMuPDF text parsing, text cleaning, overlapping chunking, dense vector embeddings (`all-MiniLM-L6-v2`), and Qdrant storage. |
| **Vector Storage (Qdrant)** | 🟢 Operational | **85%** | Automatic collection provisioning (`memos`), 384-dimensional cosine distance vector indexing, payload metadata storage (`pdf_id`, `chunk_index`, `text`). |
| **Semantic Retrieval Core** | 🟡 Partial | **35%** | `retrieval/retriever.py` implements cosine similarity vector search over Qdrant. Context assembly (`context.py`), filtering, and API views are pending. |
| **LLM Question-Answering (RAG)**| 🔴 Pending | **0%** | Grounded prompt templating, LLM provider integration (OpenAI / Claude / Gemini / Ollama), streaming answers, and citation generation. |
| **Enterprise Email Ingestion** | 🔴 Pending | **0%** | IMAP/POP3, Microsoft Graph API, Google Workspace API, or `.eml`/`.mbox` file ingestion, MIME parsing, header extraction, and attachment processing. |
| **Hybrid Search & Re-ranking** | 🔴 Pending | **0%** | BM25 sparse keyword search combined with dense vector retrieval, followed by a Cross-Encoder re-ranking step for enterprise precision. |
| **Enterprise RBAC & Security** | 🔴 Pending | **0%** | Multi-tenancy, department/user permissions, access control lists (ACLs) ensuring users can only query communications they are authorized to view. |

**Overall Project Completion: ~40%** (Core document ingestion and vector infrastructure are working; retrieval API, email connectors, and LLM generation layer remain to be built).

---

## 🏗️ System Architecture

```
[Enterprise Ingestion]
  ├── PDFs & Documents (Currently Implemented)
  └── Emails: IMAP / Microsoft 365 / Gmail / EML (Roadmap)
             │
             ▼
      [Django API & Web UI]
             │
             ▼ (Dispatches Task)
       [Redis Message Broker]
             │
             ▼
     [Celery Background Workers]
       ├── 1. Text Extraction (PyMuPDF / MIME Email Parser)
       ├── 2. Cleaning & Normalization
       ├── 3. Overlapping Text Chunker
       └── 4. Dense Embeddings (SentenceTransformers all-MiniLM-L6-v2)
             │
             ▼
      [Qdrant Vector Database] (Collection: 'memos', 384-dim, Cosine)
             │
             ▼
     [Semantic Retrieval] (Query Vectorizer -> Top-K Nearest Chunks)
             │
             ▼
   [Context Assembly & Re-Ranking]
             │
             ▼
    [LLM Generation (RAG)] ──> Grounded Answer with Source Citations
```

---

## 📁 Repository Structure

```
MemOS/
├── MemOS/                     # Django core project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py              # Celery worker & broker configuration
│   ├── settings.py            # Django settings (apps, media, database)
│   ├── urls.py                # Root routing
│   └── wsgi.py
├── api/                       # API application for upload & management
│   ├── models.py              # PDF document database model
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # Upload form view & PDF ModelViewSet
│   ├── urls.py                # Routes for / and /api/pdfs/
│   └── templates/api/         # Web upload interface
├── ingestion/                 # Document processing & vectorization pipeline
│   ├── parser.py              # Text extraction using PyMuPDF (fitz)
│   ├── cleaner.py             # Whitespace and formatting normalization
│   ├── chunker.py             # Character-based overlapping chunking
│   ├── embedder.py            # SentenceTransformers embedding model
│   ├── vector_store.py        # Qdrant client connection & upsert logic
│   └── tasks.py               # Celery async task: process_pdf
├── retrieval/                 # Search, context builder & RAG engine
│   ├── retriever.py           # Vector similarity search over Qdrant
│   ├── context.py             # Context assembler (to be implemented)
│   └── views.py               # Retrieval API views (to be implemented)
├── media/                     # Uploaded raw files (ignored by git)
├── .env.example               # Template for environment variables
├── .gitignore                 # Project ignore rules
├── docker-compose.yml         # Local Redis & Qdrant infrastructure
├── requirements.txt           # Python package dependencies
├── manage.py                  # Django CLI entrypoint
└── README.md                  # Project documentation
```

---

## ⚙️ Prerequisites & Infrastructure

Before running MemOS, ensure you have the following installed:

1. **Python 3.10+** (Tested on Python 3.12 / 3.14)
2. **Redis Server** (used as Celery message broker)
3. **Qdrant Vector Database** (local instance or Docker container)
4. **Docker** *(Recommended for launching Redis and Qdrant in seconds)*

---

## 🚀 Commands to Run

Follow these step-by-step commands to get MemOS running locally:

### Step 1: Start Infrastructure Services (Redis & Qdrant)

The fastest method is using the included `docker-compose.yml`:

```bash
docker compose up -d
```

This starts:
- **Redis** on port `6379`
- **Qdrant Vector DB** on ports `6333` (HTTP/REST) and `6334` (gRPC) with persistent volume storage in `./qdrant_storage`.

*(Alternatively, you can run them individually with `docker run`):*
```bash
# Start Redis
docker run -d --name memos-redis -p 6379:6379 redis:alpine

# Start Qdrant
docker run -d --name memos-qdrant -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

Verify Qdrant is running by visiting the Qdrant Web Dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard).

---

### Step 2: Set Up Virtual Environment & Dependencies

```bash
# Create virtual environment (if not already created)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate       # On Linux / macOS
# .venv\Scripts\activate        # On Windows

# Upgrade pip and install all required packages
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 3: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env
```

---

### Step 4: Run Database Migrations

Apply Django migrations to initialize SQLite (or your configured database):

```bash
python manage.py migrate
```

*(Optional) Create an admin superuser:*
```bash
python manage.py createsuperuser
```

---

### Step 5: Start the Celery Background Worker

In a **separate terminal window** (with your `.venv` activated):

```bash
source .venv/bin/activate
celery -A MemOS worker --loglevel=info
```

You should see Celery register the task:
```text
[tasks]
  . ingestion.tasks.process_pdf
```

---

### Step 6: Start the Django Development Server

In your **primary terminal window** (with your `.venv` activated):

```bash
python manage.py runserver
```

The application is now live at:
- **Web Upload Form**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **REST API (PDF List & Upload)**: [http://127.0.0.1:8000/api/pdfs/](http://127.0.0.1:8000/api/pdfs/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### Step 7: Verify Ingestion & Vector Retrieval

1. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser and upload any PDF file.
2. Observe your Celery terminal: it will extract text, clean it, split it into chunks, embed each chunk, and upload points to Qdrant.
3. Test semantic retrieval in the Django shell:
   ```bash
   python manage.py shell
   ```
   ```python
   from retrieval.retriever import retrieve

   # Replace with a question or topic relevant to your uploaded PDF
   results = retrieve("Summarize the main discussion points", limit=3)
   for r in results:
       print("Score:", r.score)
       print("Text Chunk:\n", r.payload["text"])
       print("-" * 50)
   ```

---

## 🗺️ Roadmap: Features to Implement Next

To evolve MemOS into a comprehensive Enterprise Communication & Email Memory System, the following features should be implemented:

### 1. Enterprise Email Ingestion Engine
- **Direct Mailbox Connectors**:
  - **IMAP / POP3 Client**: Sync periodically from standard enterprise email servers.
  - **Microsoft Graph API**: Native integration with Microsoft 365 / Outlook for enterprise tenants.
  - **Google Workspace (Gmail API)**: OAuth2-based continuous email sync.
  - **Direct File Ingestion**: Drag-and-drop support for `.eml` and `.msg` email archives.
- **Email Parser**:
  - Extract structured headers: `From`, `To`, `Cc`, `Bcc`, `Subject`, `Date`, `Message-ID`, and `Thread-ID`.
  - Strip redundant email signatures and historical reply threads (`> quoted text`).
  - Extract and route email attachments (PDFs, DOCX, XLSX) into the ingestion pipeline.
- **Rich Metadata Payloads in Qdrant**:
  - Store `sender`, `recipient_list`, `timestamp`, `subject`, and `thread_id` directly in Qdrant point payloads to enable filtered queries (e.g. *"Show vendor discussions from Q3"*).

### 2. Context Assembly & LLM Question-Answering (RAG)
- **`retrieval/context.py`**: Assemble the top retrieved chunks into a prompt with token limits and deduplication.
- **LLM Synthesis**:
  - Integrate with OpenAI (`gpt-4o`), Google Gemini (`gemini-1.5-pro`), or on-premise open-weights models (via Ollama / vLLM / Hugging Face TGI) for air-gapped enterprise compliance.
- **Citations & Verification**: Every LLM answer must cite the specific email/document, sender, and timestamp to prevent hallucinations and maintain audit trails.

### 3. Hybrid Search & Precision Re-ranking
- Combine **Dense Vector Search** (semantic understanding) with **BM25 Sparse Search** (exact keyword matching for transaction IDs, legal terminology, specific names).
- Implement a **Cross-Encoder Re-ranker** (e.g., `bge-reranker-large` or `cohere-rerank`) to re-score the top 25 candidates down to the top 5 most relevant passages before passing to the LLM.

### 4. Enterprise Security, Multi-Tenancy & Access Control (RBAC)
- **Data Isolation**: Multi-tenant namespace support in Qdrant so different corporate divisions or enterprise clients cannot access each other's data.
- **Permission Filtering**: Enforce security filters at query time based on user role and email recipient permissions.

### 5. Docker Compose & Production Deployment
- Multi-container `docker-compose.yml` defining `web`, `celery_worker`, `redis`, and `qdrant`.
- PostgreSQL database replacing SQLite for production reliability.
