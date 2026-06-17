# cv-agent

An AI-powered CV and job post analysis agent built with OpenAI.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and replace `your-key-here` with your actual OpenAI API key.

3. **Run the project**
   ```bash
   python src/main.py
   ```

## Project Structure

```
cv-agent/
├── src/
│   └── main.py       # Main entry point
├── .env.example      # Environment variable template
├── requirements.txt  # Python dependencies
└── README.md         # This file
```
