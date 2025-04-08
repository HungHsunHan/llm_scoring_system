import asyncio

from openai import OpenAI

from config.config import (
    DEFAULT_LLM_MODEL,
    LLM_MODELS,
    OPENROUTER_API_KEY,
    TOP_N_FREE_MODELS,
)
from src.utils.helpers import retry

# 初始化OpenAI客戶端，連接到OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


# 從LLM_MODELS列表中獲取前N個免費模型
def get_top_n_free_models(n=TOP_N_FREE_MODELS):
    """
    Returns the top N free LLM models from the LLM_MODELS list.
    """
    free_models = [model["name"] for model in LLM_MODELS if model["free"]]
    return free_models[:n]


# 發送提示和文本到LLM並返回回應
# 包含重試機制，最多嘗試3次
async def get_llm_response(prompt, text, model=DEFAULT_LLM_MODEL):
    """
    Sends a prompt and text to the LLM and returns the response.
    """
    try:

        @retry(max_attempts=3, delay=2)
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
        print(completion)

        # Check for error in completion object
        if completion and hasattr(completion, "error") and completion.error:
            code = completion.error.get("code")
            message = completion.error.get("message", "Unknown error")
            if code == 429:
                raise RuntimeError(f"Rate limit exceeded: {message}")
            else:
                raise RuntimeError(f"LLM API error (code {code}): {message}")

        if not completion:
            raise ValueError("LLM response is None")

        try:
            return completion.choices[0].message.content
        except Exception:
            raise
    except Exception as e:
        import traceback

        print("Error getting LLM response:")
        traceback.print_exc()
        if hasattr(e, "response") and hasattr(e.response, "text"):
            print("API response content:", e.response.text)
        return "Unable to evaluate at this time"
