[![CI and CD to HuggingSpace](https://github.com/baolongnguyenmac/chatbot/actions/workflows/main.yml/badge.svg)](https://github.com/baolongnguyenmac/chatbot/actions/workflows/main.yml)

# ChatBot

A full-stack chatbot which uses a LLM as its core and `gradio` as UI

## Some notes

- Create an environment file `.env` in this direction with the following content:

    ```bash
    GOOGLE_API_KEY=<key>
    TAVILY_API_KEY=<key>
    ```

- For GitHub Action, create 2 secrets to store these keys. In the workflow file `./.github/workflows/main.yml`, specify the environment by

    ```yml
    runs-on: ubuntu-latest
    env:
      GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
      TAVILY_API_KEY: ${{ secrets.TAVILY_API_KEY }}
    ```

- `EXPORT PYTHONPATH='./src'` so you can run code from mother directory of `./src`
