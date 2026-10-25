# Git Lab 2 REST Service

Навчальний REST-сервіс, створений для лабораторної роботи №2
з дисципліни "Основи безперервної інтеграції, доставки та розгортання програмних засобів".

## Technologies

- Python
- FastAPI
- Uvicorn
- uv
- Git

## Continuous Integration

Pull Requests are validated using GitHub Actions.
The workflow builds the Python package and verifies SHA-256 checksums.

## Health Check

The application provides a health check endpoint
for monitoring API availability.

### Request

GET /health

### Response

The endpoint returns the health status of the service.

## Installation

Install dependencies:

```bash
uv sync


