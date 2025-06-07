# Codex Python CLI (experimental)

This is a very small Python reimplementation of the `codex` command.
It only supports sending a single prompt to a provider and printing the
response.  For feature parity use the official Node.js version.

```
python -m codex_py.cli -m codellama:34b -p ollama "hello"
```

`OPENAI_API_KEY` or `OLLAMA_API_KEY` environment variables are used if
required by the provider.
