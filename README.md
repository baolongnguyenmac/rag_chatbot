---
title: Basic Docker SDK Space
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
---

[![CI and CD to HuggingSpace](https://github.com/baolongnguyenmac/chatbot/actions/workflows/main.yml/badge.svg)](https://github.com/baolongnguyenmac/chatbot/actions/workflows/main.yml)

# ChatBot

A full-stack chatbot which uses a LLM as its core and `gradio` as UI

## Some notes

- Create an environment file `.env` in this direction with the following content to run on local (with `compose.yml`):

    ```bash
    GOOGLE_API_KEY=<key>
    TAVILY_API_KEY=<key>
    PYTHONPATH='./src' # so you can run code from mother directory of `./src`
    ```

- Since there are a lot dependencies and resolving their version takes lots of time, I use `pip-compile` to resolve them before pushing everything to GitHub. `pip-compile` take `requirements.in` as input and return a `requirements.txt`. Just specify needed packages in `requirements.in` (without version) and `pip-compile requirements.in`

## Handle Secret

- Storing secret to GitHub Secret or Hugging Face Secret means that these secrets will be exported to system variable at runtime

- For GitHub Action, create 2 secrets to store these keys. In the workflow file `./.github/workflows/main.yml`, specify the environment by

    ```yml
    runs-on: ubuntu-latest
    env:
      GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
      TAVILY_API_KEY: ${{ secrets.TAVILY_API_KEY }}
    ```


- For HuggingFace Space & DockerHub: