import asyncio

from openai import OpenAI

from config.config import (
    DEFAULT_LLM_MODEL,
    LLM_MODELS,
    OPENROUTER_API_KEY,
    TOP_N_FREE_MODELS,
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def get_top_n_free_models(n=TOP_N_FREE_MODELS):
    """
    Returns the top N free LLM models from the LLM_MODELS list.
    """
    free_models = [model["name"] for model in LLM_MODELS if model["free"]]
    return free_models[:n]


async def get_llm_response(prompt, text, model=DEFAULT_LLM_MODEL):
    """
    Sends a prompt and text to the LLM and returns the response.
    """
    try:

        def sync_call():
            return client.chat.completions.create(
                extra_headers={
                    # Optionally customize these headers
                    # "HTTP-Referer": "<YOUR_SITE_URL>",
                    # "X-Title": "<YOUR_SITE_NAME>",
                },
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
            )

        completion = await asyncio.to_thread(sync_call)
        return completion.choices[0].message.content
    except Exception as e:
        import traceback

        print("Error getting LLM response:")
        traceback.print_exc()
        if hasattr(e, "response") and hasattr(e.response, "text"):
            print("API response content:", e.response.text)
        return "Unable to evaluate at this time"
