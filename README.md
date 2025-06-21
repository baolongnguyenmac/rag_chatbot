---
title: ChatBotDocker
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
---

[![CI and CD to HuggingSpace](https://github.com/baolongnguyenmac/chatbot/actions/workflows/main.yml/badge.svg)](https://github.com/baolongnguyenmac/chatbot/actions/workflows/main.yml)

# ChatBot

A full-stack chatbot which uses a LLM as its core and `gradio` as UI

## CI using GitHub Action

- Create 2 secrets to store these keys in GitHub Secret. In the workflow file `./.github/workflows/main.yml`, specify the environment by

    ```yml
    runs-on: ubuntu-latest
    env:
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        TAVILY_API_KEY: ${{ secrets.TAVILY_API_KEY }}
    ```

- Storing secret to GitHub Secret or Hugging Face Secret means that these secrets will be exported to system variable at runtime

## CD to DockerHub

- Create a [PAT](https://app.docker.com/settings/personal-access-tokens) so GitHubAction can push image to DockerHub
- Save this token to GitHub Secret and specify username of DockerHub account
- Setup `main.yml`

## Run locally

- Pull image from [DockerHub](https://hub.docker.com/repository/docker/baolongnguyenmac/chatbot/general)
- Config file `.env` as follows to run the image:

    ```bash
    GOOGLE_API_KEY=<key>
    TAVILY_API_KEY=<key>
    PYTHONPATH=/app/src # so you can run code from `/app/src`
    ```

- Note that `.env` file can contain `single/double quote` but only use for `docker compose up` (which means that you have to config a `compose.yml`). Otherwise, you should not use `quote` since we can run as follows:

    ```bash
    docker run --env-file .env --name ctn_chatbot -p 5555:7860 baolongnguyenmac/chatbot
    ```

- In case you want to run via `compose.yml`: Config the compose file as follows:

    ```yml
    services:
    chatbot:
        image: baolongnguyenmac/chatbot
        container_name: ctn_chatbot
        env_file:
            - .env

        ports:
            - 5555:7860
    ```

    - Then `docker compose up`

## CD to HF Space

<!-- - sẽ viết sau -->

## Dependency stuff

- Since there are a lot dependencies and resolving their version takes lots of time, I use `pip-compile` to resolve them before pushing everything to GitHub. `pip-compile` take `requirements.in` as input and return a `requirements.txt`. Just specify needed packages in `requirements.in` (without version) and `pip-compile requirements.in`
