# News AI

A web application that uses AI to analyze and summarize news articles about any topic.

## Project Structure

```
NewsAI/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── fetch_google_results.py
│   │   └── summarize.py
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.tsx
        ├── App.css
        └── services/
            └── api.ts
```

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_custom_search_engine_id
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Enter a topic in the search box
3. Click "Search" to get AI-generated insights from recent news articles
4. Click on source links to read the original articles

## Features

- Real-time news search and analysis
- AI-powered insights extraction
- Source attribution and links
- Modern, responsive UI
- Error handling and loading states 