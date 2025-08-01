Follow-Up Question Generation API

A FastAPI base microservice for genrating context aware follow-up questions from document chunks using OpenAI's GPt models.
Desgined with Async Processing and modular architecture for scalability. 

🚀 Features

1. 🔗 LLM-Powered: Uses OpenAI's gpt-4o for high-quality question generation.
2. ⚡ Asynchronous: Fully async with retries and exponential backoff.
3. 📄 Document Chunking: Handles multiple text chunks in a single session.
4. 📈 Structured Logging: Context-aware logs for every session.
5. 📦 Modular Design: Clean separation of concerns (routing, services, utils).

📁 Project Structure
```bash
.
├── app/
│   ├── api/
│   │   └── v01/
│   │       ├── routes/
│   │       │   └── followup_routes.py
│   │       ├── services/
│   │       │   ├── qa_service.py
│   │       │   ├── followup_manager.py
│   │       │   └── chunk_processor_service.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── utils.py
│   ├── main.py
├── .env
├── config.yaml
├── requirements.txt
├── README.md
```

⚙️ Setup

1. Clone the repo
```bash
git clone <Repo URI>
cd app
```

2. Set environment variables
Create a .env fiel
```bash
OPENAI_API_KEY = 'your-openai-key'
```

5. Run the Service
```bash
uvicorn app_main:app --reload
```

🧪 API Usage

Endpoint
```bash
POST /api/v01/generate-followups
```

Request Body
```bash
{
  "session_id": "string",
  "current_question": "string",
  "source_documents": 
  [
    {
      "metadata": {
        "additionalProp1": {}
      },
      "page_content": "string"
    }
  ]
}
```

Response
```bash
{
  "session_id": "string",
  "questions": [
    {
      "question": "string",
      "answer": "string"
    }
  ]
}
```
🛠️ Developer Notes
1. Uses "tenacity" for retry logic.
2. Uses "tiktoken" for monitoring token activity.
3. Utilized Async OpenAI for generating Q&A.
4. All routes and services have built-in logging with session context.

🧭 Future Improvements
1. 🔄 Support for stream=True with proper async yield for real-time UX.
2. 🧪 Unit and integration test coverage.

