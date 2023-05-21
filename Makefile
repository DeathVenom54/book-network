init:
	pip install -r requirements.txt
run:
	python3 main.py
dev:
	uvicorn main:app --reload