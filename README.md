# AURORA - AI-Powered Data Analysis Platform

A monorepo project structure for building an AI-powered data analysis platform using FastAPI, LangChain, PandasAI, React, Tailwind CSS, and Plotly.js.

## Project Structure

```
aurora/
├── aurora-backend/      # FastAPI + LangChain + PandasAI backend
├── aurora-frontend/     # React + Tailwind + Plotly.js frontend
├── shared/              # Shared schemas and utilities
└── README.md           # This file
```

## Architecture Overview

### Backend (`/aurora-backend`)
- **FastAPI**: RESTful API server
- **LangChain**: AI agent orchestration and LLM integration
- **PandasAI**: Natural language interface for data analysis
- Handles data processing, AI analysis, and API endpoints

### Frontend (`/aurora-frontend`)
- **React**: User interface framework
- **Tailwind CSS**: Styling and design system
- **Plotly.js**: Interactive data visualizations
- Communicates with backend via REST API

### Shared (`/shared`)
- **Schemas**: Pydantic models for type-safe data validation (Python) and TypeScript definitions (JavaScript)
- **Utilities**: Common validation and formatting functions
- Ensures consistency between frontend and backend

## Agent Interaction Architecture

The AURORA platform uses a multi-agent architecture where different AI agents collaborate to provide comprehensive data analysis:

### 1. **Query Understanding Agent** (LangChain)
- **Location**: Backend
- **Role**: Parses and understands natural language queries from users
- **Interactions**:
  - Receives user queries from frontend
  - Analyzes intent and extracts parameters
  - Routes to appropriate downstream agents
  - Returns structured query understanding

### 2. **Data Retrieval Agent** (PandasAI)
- **Location**: Backend
- **Role**: Retrieves and prepares data based on queries
- **Interactions**:
  - Receives structured queries from Query Understanding Agent
  - Accesses data sources (CSV, database, APIs)
  - Performs data transformations
  - Returns cleaned and prepared datasets

### 3. **Analysis Agent** (LangChain + PandasAI)
- **Location**: Backend
- **Role**: Performs AI-powered data analysis
- **Interactions**:
  - Receives prepared data from Data Retrieval Agent
  - Uses LangChain to orchestrate analysis workflows
  - Leverages PandasAI for natural language data queries
  - Generates insights, statistics, and recommendations
  - Returns analysis results with explanations

### 4. **Visualization Agent** (Backend → Frontend)
- **Location**: Backend generates configs, Frontend renders
- **Role**: Creates appropriate visualizations for data
- **Interactions**:
  - Receives analysis results from Analysis Agent
  - Determines optimal chart types (bar, line, scatter, etc.)
  - Generates Plotly.js configuration
  - Sends visualization configs to frontend
  - Frontend renders interactive charts using Plotly.js

### 5. **Response Synthesis Agent** (LangChain)
- **Location**: Backend
- **Role**: Synthesizes final user-friendly responses
- **Interactions**:
  - Combines analysis results, visualizations, and metadata
  - Generates natural language explanations
  - Formats response according to shared schemas
  - Returns complete response to frontend

## Agent Communication Flow

```
User Query (Frontend)
    ↓
[HTTP Request] → Query Understanding Agent (Backend)
    ↓
    ├──→ Data Retrieval Agent (PandasAI)
    │       ↓
    │   [Structured Data]
    │       ↓
    ├──→ Analysis Agent (LangChain + PandasAI)
    │       ↓
    │   [Analysis Results]
    │       ↓
    ├──→ Visualization Agent
    │       ↓
    │   [Plotly Configs]
    │       ↓
    └──→ Response Synthesis Agent
            ↓
    [Complete Response]
            ↓
[HTTP Response] → Frontend (React + Plotly.js)
    ↓
User sees: Charts + Analysis + Explanations
```

## Data Flow

1. **Request Phase**:
   - Frontend sends user query via REST API
   - Backend receives request and validates using shared schemas
   - Query Understanding Agent processes the query

2. **Processing Phase**:
   - Agents collaborate sequentially/parallelly based on query type
   - Data flows: Query → Data Retrieval → Analysis → Visualization → Synthesis
   - Each agent uses shared utilities for validation and formatting

3. **Response Phase**:
   - Response Synthesis Agent creates final output
   - Backend returns structured response (JSON) using shared schemas
   - Frontend renders visualizations and displays results

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd aurora-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env and add your API keys

# Run the server
python main.py
# Server runs on http://localhost:8000
```

### Frontend Setup

```bash
cd aurora-frontend
npm install

# Run the development server
npm run dev
# App runs on http://localhost:3000
```

### Shared Module Setup

For Python projects using shared schemas:
```bash
cd shared
pip install -r requirements.txt
```

For TypeScript projects:
```bash
cd shared/schemas
npm install
npm run build
```

## Environment Variables

### Backend (.env)
```bash
OPENAI_API_KEY=your_openai_api_key_here
PANDASAI_API_KEY=your_pandasai_api_key_here
ENVIRONMENT=development
```

## API Endpoints (Planned)

- `GET /health` - Health check
- `POST /api/query` - Submit natural language query
- `POST /api/analyze` - Request AI analysis
- `GET /api/data/{dataset_id}` - Retrieve dataset
- `POST /api/visualize` - Generate visualization config

## Shared Schemas

The `shared/` directory contains:
- **Python schemas**: Pydantic models for backend validation
- **TypeScript schemas**: Type definitions for frontend type safety
- **Common utilities**: Validation and formatting functions

This ensures type safety and consistency across the entire stack.

## Development Workflow

1. Make changes to shared schemas when needed
2. Update backend to implement new agent logic
3. Update frontend to consume new API endpoints
4. Test end-to-end flow from query to visualization

## Future Enhancements

- WebSocket support for real-time agent communication
- Agent orchestration framework for complex workflows
- Caching layer for improved performance
- Multi-user support with authentication
- Custom agent plugin system

## License

[Add your license here]

