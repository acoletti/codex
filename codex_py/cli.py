import argparse
import os
import requests

PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
    },
    "ollama": {
        "name": "Ollama",
        "base_url": "http://localhost:11434/v1",
        "env_key": "OLLAMA_API_KEY",
    },
}

def call_chat_completion(provider: str, model: str, prompt: str) -> str:
    p = PROVIDERS.get(provider.lower())
    if p is None:
        raise ValueError(f"Unknown provider: {provider}")
    url = f"{p['base_url']}/chat/completions"
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv(p["env_key"], "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal Codex Python CLI")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to the model")
    parser.add_argument("--version", action="version", version="0.0.1")
    parser.add_argument("-m", "--model", default="codex-mini-latest")
    parser.add_argument("-p", "--provider", default="openai")
    args = parser.parse_args()

    if not args.prompt:
        parser.error("prompt is required")

    try:
        output = call_chat_completion(args.provider, args.model, args.prompt)
    except Exception as exc:
        raise SystemExit(f"Error: {exc}")

    print(output)


if __name__ == "__main__":
    main()
