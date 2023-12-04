# C:\ProgramData\chocolatey\lib\make

build-dev:
	docker-compose -f .\docker-compose.yaml -f .\docker-compose-development.yaml up -d

build-prod:
	docker-compose -f .\docker-compose.yaml up -d