install:
	sudo apt install curl && pip install --no-cache-dir -r requirements.txt

test:
	pytest -v