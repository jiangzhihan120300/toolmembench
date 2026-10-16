import os
import time
from openai import (
    OpenAI,
    APITimeoutError,
    APIConnectionError,
    RateLimitError,
    APIStatusError,
)

class OpenAICompatibleBackend:
    def __init__(self):
        api_key = os.environ.get("TOOLMEMBENCH_API_KEY") or os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("TOOLMEMBENCH_BASE_URL")
        self.model = os.environ.get("TOOLMEMBENCH_MODEL", "gpt-4o-mini")
        self.timeout = float(os.environ.get("TOOLMEMBENCH_TIMEOUT", "120"))
        self.max_retries = int(os.environ.get("TOOLMEMBENCH_MAX_RETRIES", "5"))

        if not api_key:
            raise RuntimeError(
                "Missing API key. Set TOOLMEMBENCH_API_KEY or OPENAI_API_KEY."
            )

        kwargs = {
            "api_key": api_key,
            "timeout": self.timeout,
            "max_retries": 0,
        }
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)

    def generate(self, prompt, temperature=0.0):
        last_err = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                )
                return resp.choices[0].message.content
            except (APITimeoutError, APIConnectionError, RateLimitError, APIStatusError) as e:
                last_err = e
                wait_s = min(60, 2 ** attempt)
                print(f"[LLM retry] attempt={attempt + 1}/{self.max_retries + 1} error={type(e).__name__}: {e}")
                if attempt < self.max_retries:
                    time.sleep(wait_s)
        raise last_err
