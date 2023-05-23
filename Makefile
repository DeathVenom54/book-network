init:
	pip install -r requirements.txt
run:
	python3 main.py
dev:
	uvicorn main:app --reload
testdb:
	python3 database/database.py