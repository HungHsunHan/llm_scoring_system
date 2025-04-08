# Scoring System

This project is an AI-powered scoring system that evaluates documents based on multiple criteria using Large Language Models (LLMs). It supports single file and batch processing with detailed, structured output.

## Features

- Upload and score individual files or entire directories
- Uses LLMs to evaluate text on:
  - Grammar
  - Structure
  - Creativity
  - Relevance
- Outputs detailed scores and reasons in a CSV file
- Customizable prompt and model selection
- Gradio web interface for easy use

## Project Structure

```
config/                 # Configuration files (default prompt, API keys, models)
src/
  gradio_ui/            # Gradio interface components
  llm/                  # LLM interaction logic
  processing/           # File handling, parsing, scoring logic
  utils/                # Helper functions
requirements.txt        # Python dependencies
scoring_results.csv     # Output CSV file with scores
```

## Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd scoring_system
```

2. **Create a virtual environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API keys**

Set your OpenRouter API key in `config/config.py` or as an environment variable:

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

## Usage

### Run the Gradio app

```bash
python src/gradio_ui/app.py
```

### Process files

- Upload a single file via the UI
- Or process a directory of files (batch mode)
- Results will be saved to `scoring_results.csv`

## Customization

- Modify `config/config.py` to change the default prompt or models.
- The prompt instructs the LLM to return a JSON with detailed scores and reasons.
- You can extend criteria or adjust weights by editing the prompt.

## Notes

- Ensure your API key has access to the selected LLM models.
- The system expects the LLM to return valid JSON. Non-JSON responses will trigger errors.
- The CSV output includes fixed columns for consistent analysis.

## License

MIT License
