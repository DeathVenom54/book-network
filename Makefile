init:
	pip install -r requirements.txt
run:
	python3 main.py
dev:
	uvicorn main:app --reload
testdb:
	python3 models/Database.py
testbook:
	python3 models/Book.py