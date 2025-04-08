import os

# OpenRouter API Key
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Available LLM Models
LLM_MODELS = [
    {"name": "google/gemini-2.0-flash-exp:free", "free": True},
    {"name": "openrouter/quasar-alpha", "free": True},
    {"name": "deepseek/deepseek-chat-v3-0324:free", "free": True},
    {"name": "google/gemini-2.5-pro-exp-03-25:free", "free": True},
]

# Default LLM Model
DEFAULT_LLM_MODEL = "google/gemini-2.0-flash-exp:free"

# Top N Free Models
TOP_N_FREE_MODELS = 3

# Default Prompt
DEFAULT_PROMPT = """You are an expert scoring system. Please evaluate the following text based on these criteria:

Grammar (Weight: 25%): Assess grammatical correctness, sentence structure, punctuation, and spelling. Provide a score out of 25 and a **very short keyword or phrase** summarizing the reason (e.g., "minor errors", "good grammar").

Structure (Weight: 25%): Evaluate organization and coherence. Provide a score out of 25 and a **very short keyword or phrase** (e.g., "simple", "well-structured").

Creativity (Weight: 25%): Assess originality and imagination. Provide a score out of 25 and a **very short keyword or phrase** (e.g., "minimal", "creative").

Relevance (Weight: 25%): How well does the text address the prompt or requirements? Provide a score out of 25 and a **very short keyword or phrase** (e.g., "relevant", "off-topic").

Calculate the total score by summing the four criteria scores, resulting in an integer between 0 and 100.

Return your evaluation strictly in the following JSON format:

{
  "final_score": total_score_integer,
  "criteria": [
    {
      "name": "Grammar",
      "score": grammar_score_integer,
      "reason": "short keyword or phrase"
    },
    {
      "name": "Structure",
      "score": structure_score_integer,
      "reason": "short keyword or phrase"
    },
    {
      "name": "Creativity",
      "score": creativity_score_integer,
      "reason": "short keyword or phrase"
    },
    {
      "name": "Relevance",
      "score": relevance_score_integer,
      "reason": "short keyword or phrase"
    }
  ]
}

Respond ONLY with the JSON object, without any additional commentary.
"""
