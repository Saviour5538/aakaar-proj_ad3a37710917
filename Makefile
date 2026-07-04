# Variables
DOCKER_COMPOSE_FILE=docker-compose.yml

# Install dependencies
install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

# Start development environment
dev:
	./scripts/dev.sh

# Build the project
build:
	cd frontend && npm run build
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

# Run tests
test:
	pytest backend/tests
	cd frontend && npm test

# Start Docker containers
docker-up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop Docker containers
docker-down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Clean up build artifacts and Docker containers
clean:
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	docker-compose -f $(DOCKER_COMPOSE_FILE) down --volumes --remove-orphans