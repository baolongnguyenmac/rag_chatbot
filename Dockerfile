FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt update -y
RUN apt install -y ffmpeg libsm6 libxext6
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

EXPOSE 7860

CMD python -m chat_rag
