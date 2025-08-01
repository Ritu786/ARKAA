# Arkaa Indexer

This project provides a modular and production-ready framework for ingesting and parsing PDF and DOCX documents into structured chunks using LangChain-compatible & Unstructured.io loaders. It includes logging, error handling, environment-based configuration, and abstracted loaders for flexibility.

## 🔧 Features

- Support for both PDF (`PyPDFLoader`,`Unstructured`) and DOCX (`Unstructured`) formats
- Modular loader architecture with a factory pattern
- Custom logging for each loader
- configuration via `.env` & `.yaml`
- Validation and Error handling included
- Processing techniques including, normalizing document structure,language detection & translation. 
- Embedding Creations using `OpenAI` & Storing them in `PGVector`

## 📁 Folder Structure
```bash
├── main.py # Entry point for processing documents
├── loaders/ # Contains loader classes
│ ├── base_loader.py
│ ├── pypdf_loader.py  # Utilizes PyPDF Loader
│ ├── doc_loader.py    # Uses unstructured.io to parse word documents
  ├── unstruct_pdf_loader.py  # Uses unstrucutred.io to parse pdf documents, choose this for complex pdf documents
│ └── loader_factory.py # That chooses the above loaders based on the document extension
├── data/  # contains sample data documents 
├── processors/
│   ├── language_detector.py # uses langid to detect the language
│   ├── preprocessor_pipeline.py # Entire Processing pipeline
│   ├── translation_process.py # performs the translation process 
│   └── translator/
│       ├── argos_translator.py # Open-Source & Offline Translators
│       ├── base_translator.py 
│       ├── google_translator.py # Uses Google Translator API
│       ├── microsoft_translator.py # Uses Microsoft Translator
│       ├── openai_translator.py # LLM as a Translator 
│       └── translator_factory.py # Chooses the Translator
├── prompts/ 
    ├── openai_translator_prompt.py # Prompt for the LLM Translator
├── vectorstores/
│   ├── base_vectorstore.py
│   ├── pgvector_store.py  # Postgres Vector Database
│   └── vectorstore_factory.py # Choose between the vectorstores.
├── app_utils/   
  ├── app.log   # Stores all the application Log
│ ├── logger.py # Logger Config File
  ├── exceptions.py # Defines the Custom Exceptions 
│ └── validators.py # for validating file paths
│ └── yaml_loader.py # for loading & overriding the config File.
├── embeddings/
│   ├── base_embedder.py
│   └── openai_embedder.py # Uses Open AI Embedding 
├── config/
│   └── config.yaml # Config File that drives the entire indexing process.
├── api/                           # API layer
│   └── v1/
│       ├── celery_worker.py       # Celery app and task registration
│       ├── ingest_route.py        # FastAPI route for document ingestion
│       ├── schemas/
│       │   └── ingest_schema.py   # Pydantic schema for API input validation
│       ├── services/
│       │   └── ingest_service.py  # Service logic for handling ingestion [Indexing Logic]
│       └── tasks/
│           └── indexing_task.py  # Celery background indexing task, entry point for celery
├── .env   # to store credentials
├── requirements.txt
└── README.md
```
## 🚀 Getting Started


### 1. Clone the repository
```bash
git clone https://github.com/spiredata/Arkaa_BackEnd.git
cd Arkaa_BackEnd
```
### 2. Create & Activate Virtual Environment
```bash
conda create -n arkaaenv python=3.10
conda activate arkaaenv
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run RabbitMQ
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```
### 5. Run the Celery Task

The below command is only for windows OS

```bash
celery -A api.v1.celery_worker.celery_app worker --loglevel=info --concurrency=4 -Q indexing_queue -pool=solo
```
OR

```bash
pip install gevent

celery -A api.v1.celery_worker.celery_app worker --loglevel=info --concurrency=4 -Q indexing_queue -P gevent
```

For other Operating Systems, [Celery will utilize its default concurrency module "prefork"]
```bash
celery -A api.v1.celery_worker.celery_app worker --loglevel=info --concurrency=4 -Q indexing_queue
```

## Input Schema (FastAPI)
```bash
{
  "file_paths": [
    {
      "id": 0,
      "path": "string"
    }
  ],
  "collection_name": "string",
  "base_path": "string"
}
```
