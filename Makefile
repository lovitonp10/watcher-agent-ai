.PHONY: help setup install test update chat search stats clean

help:
	@echo "Tech Watch Agent - Available Commands:"
	@echo ""
	@echo "  make setup      - Initial setup (create venv, install deps)"
	@echo "  make install    - Install/update dependencies"
	@echo "  make test       - Run all tests"
	@echo "  make test-e2e   - Run end-to-end test"
	@echo "  make update     - Update knowledge base"
	@echo "  make chat       - Start interactive chat"
	@echo "  make stats      - Show database statistics"
	@echo "  make info       - Show configuration"
	@echo "  make clean      - Clean test databases"
	@echo ""

setup:
	@./setup.sh

install:
	@pip install -r requirements.txt

test:
	@echo "Running ingestion tests..."
	@python test_ingestion.py
	@echo ""
	@echo "Running database tests..."
	@python test_database.py

test-llm:
	@python test_llm.py

test-e2e:
	@python test_e2e.py

update:
	@python main.py update

chat:
	@python main.py chat

search:
	@python main.py search "$(q)"

stats:
	@python main.py stats

info:
	@python main.py info

clean:
	@rm -rf data/test_*
	@echo "Test databases cleaned"
