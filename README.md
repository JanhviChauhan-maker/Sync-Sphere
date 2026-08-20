# SyncSphere AI

**Enterprise-grade AI workflow orchestration platform powered by the Model Context Protocol (MCP).**

SyncSphere AI connects AI agents with multiple external services and allows users to create, execute, and manage intelligent workflows from natural-language instructions.

It combines **MCP, RAG, vector search, LLMs, FastAPI, React, and MongoDB** into a unified orchestration platform.

---

## 🚀 What is SyncSphere?

Modern applications often require AI agents to interact with multiple tools and services.

SyncSphere acts as an **AI orchestration layer** between the user, AI models, and external applications.

A user can describe a workflow in natural language, and SyncSphere can transform that intent into executable workflow steps.

### Example

> "Create a project task, notify the team on Slack, and update the tracking data."

The platform can:

1. Understand the user's intent.
2. Break the request into workflow steps.
3. Identify the required tools/connectors.
4. Retrieve relevant tool information using RAG/vector search.
5. Generate an executable workflow.
6. Execute the workflow through MCP-based integrations.
7. Track execution and handle failures.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    │ Natural Language     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Frontend     │
                    │ TypeScript + Tailwind│
                    │      React Flow      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │     Backend API      │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌────────────┐ ┌────────────┐ ┌────────────┐
          │ AI Planner │ │ RAG /      │ │ Workflow   │
          │ / Compiler │ │ Vector     │ │ Engine     │
          │            │ │ Search     │ │            │
          └─────┬──────┘ └────────────┘ └──────┬─────┘
                │                              │
                └──────────────┬───────────────┘
                               ▼
                    ┌──────────────────────┐
                    │     MCP Gateway      │
                    │  Connector Runtime   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐    ┌───────────┐
        │   Slack   │    │  GitHub   │    │   Jira    │
        │ / Others  │    │ / Others  │    │ / Others  │
        └───────────┘    └───────────┘    └───────────┘
```

---

## ✨ Key Features

### 🤖 AI Workflow Planning

Converts natural-language instructions into structured workflow plans and executable steps.

### 🔌 MCP Integration

Uses the **Model Context Protocol (MCP)** as the integration layer between AI agents and external tools.

### 🧠 Retrieval-Augmented Generation

RAG provides the AI planner with relevant connector documentation, available actions, parameters, and tool capabilities.

### 🔎 Vector Search

Connector and action information can be represented as embeddings and retrieved based on semantic similarity.

### ⚙️ Workflow Orchestration

Workflows can be represented as structured execution graphs containing multiple dependent actions.

### 🔄 Multi-Service Automation

Designed to connect multiple external services through pluggable connectors.

### 🖥️ Visual Workflow Builder

The React frontend uses **React Flow** to visualize workflow nodes, connections, and execution logic.

### 📊 Execution Management

The backend is designed to manage workflow execution, errors, retries, and execution state.

---

## 🛠️ Technology Stack

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* React Flow

### Backend

* Python
* FastAPI
* AsyncIO
* MongoDB
* Beanie / Motor
* Redis

### AI

* Large Language Models
* MCP
* RAG
* Embeddings
* Vector Search

### Infrastructure

* Docker
* Docker Compose
* GitHub Actions
* Deployment configurations

---

## 📁 Project Structure

```text
Sync-Sphere/
│
├── backend/
│   ├── src/
│   ├── tests/
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
│
├── deploy/
│   └── ...
│
├── scratch/
│   └── ...
│
├── .gitignore
├── Makefile
├── README.md
└── TODO.md
```

> The exact contents of individual directories may evolve as the platform develops.

---

## ⚡ Getting Started

### Prerequisites

Install the following before running SyncSphere locally:

* Git
* Python 3.11+
* Node.js and npm
* Docker
* Docker Compose

---

## 🔧 Environment Configuration

Clone the repository:

```bash
git clone https://github.com/Mr-HarshRaval07/Sync-Sphere.git
cd Sync-Sphere
```

Create your environment file from the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure the required environment variables inside `.env`.

**Never commit `.env` or API keys to GitHub.**

---

## 🐳 Running with Docker

Build and start the services:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

Stop the services:

```bash
docker compose down
```

---

## 💻 Running Backend Locally

Create and activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the FastAPI application according to the backend entry point configured in the project.

---

## 🌐 API Documentation

When the backend is running:

**Swagger UI**

```text
http://localhost:8000/docs
```

**ReDoc**

```text
http://localhost:8000/redoc
```

---

## 🎨 Running the Frontend

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The development server will display the local URL in the terminal.

---

## 🧪 Testing

Run the project's configured test suite using:

```bash
make test
```

Backend tests can also be executed with:

```bash
pytest
```

Frontend tests should be executed using the testing scripts configured in `frontend/package.json`.

---

## 🔐 Security

SyncSphere is designed with security in mind.

### Never commit:

* `.env`
* API keys
* Access tokens
* Passwords
* Private credentials
* Database credentials
* Cloud provider secrets

Use environment variables for sensitive configuration.

---

## 🧩 Extensibility

SyncSphere is designed as a modular platform.

New integrations can be added through the connector architecture without redesigning the entire application.

Potential integrations include:

* Project management platforms
* Communication platforms
* Code repositories
* Databases
* Analytics platforms
* Productivity tools
* Custom APIs

The MCP-based architecture allows the platform to evolve as new tools and services are introduced.

---

## 🔮 Future Improvements

Planned areas of development include:

* Additional MCP connectors
* Advanced workflow execution
* Improved human-in-the-loop approvals
* Persistent workflow memory
* Enhanced observability
* More sophisticated RAG pipelines
* Connector marketplace
* Workflow templates
* Advanced authentication and authorization
* Production deployment improvements
* More robust retry and failure recovery

---

## 🎓 Project Status

SyncSphere AI is currently an **academic prototype / active development project** demonstrating AI-powered workflow orchestration using MCP, RAG, vector search, and modern web technologies.

Some advanced features may still be under development.

---

## 👥 Contributors

Developed as a collaborative project.

* **Harsh Raval**
* **Janhvi Chauhan**
* **Dhruvin**
* **Project Contributors**

---

## 📄 License

This project is currently intended for educational and development purposes.

A formal open-source license can be added when the project is prepared for public distribution.

---

## ⭐ Support

If you find the project interesting, consider starring the repository and following its development.

**SyncSphere AI — Turning natural-language intent into connected, executable workflows.**
