# Multi-Agent Workflow Demo 🤖

This project demonstrates a multi-agent collaboration system using Google's Gemini models. It includes both a CLI demo and a Streamlit-based web interface.

## Features

- **Multi-Agent Collaboration**: Three distinct agents (Editor, Writer, Reviewer) work together to produce high-quality blog posts.
- **Streamlit UI**: A professional and interactive web interface to trigger and watch the workflow in real-time.
- **Gemini Powered**: Uses `gemini-2.5-flash` for fast and intelligent content generation.
- **Rate Limit Handling**: Built-in delays to respect API quotas.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sidehustlesCoder/Multi-Agent-Workflow.git
   cd Multi-Agent-Workflow
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Usage

### Streamlit App (Recommended)
Run the professional web interface:
```bash
streamlit run streamlit_app.py
```

### CLI Demo
Run the command-line version:
```bash
python multi_agent_demo.py
```

## How it Works
1. **Editor**: Creates a detailed outline based on the user's topic.
2. **Writer**: Drafts the blog post based on the outline.
3. **Reviewer**: Critiques the draft for logic, flow, and quality.
4. **Writer (Revision)**: Refines the final post based on the reviewer's feedback.
