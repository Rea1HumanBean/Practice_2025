.PHONY: test-all test-unit test-integration

test-all: test-unit test-integration

test-unit:
	pytest --cov=src --cov-report=term --cov-branch test/unit

test-integration:
	docker-compose -f docker-compose.test.yml up -d
	pytest --cov=src --cov-report=term --cov-branch test/integrations