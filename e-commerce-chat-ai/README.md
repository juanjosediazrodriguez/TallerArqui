# ZapatoShop - E-commerce con Chat IA

API REST de e-commerce de zapatos con asistente de inteligencia artificial, construida con Clean Architecture (3 capas).

## Descripción

Sistema que permite consultar un catálogo de zapatos y conversar con un asistente de IA (Google Gemini) que recuerda el contexto de la conversación para ayudar a los clientes a encontrar el calzado perfecto.

## Tecnologías

- **Python 3.13** - Lenguaje principal
- **FastAPI** - Framework web para la API REST
- **SQLAlchemy** - ORM para interactuar con la base de datos
- **SQLite** - Base de datos ligera
- **Google Gemini AI** - IA conversacional (gemini-2.5-flash)
- **Pydantic** - Validación de datos
- **Docker** - Containerización
- **Pytest** - Pruebas unitarias

## Arquitectura

El proyecto implementa Clean Architecture con 3 capas bien definidas:

```
Domain Layer       → Entidades y reglas de negocio puras (sin dependencias externas)
Application Layer  → Casos de uso, servicios y DTOs
Infrastructure     → FastAPI, SQLAlchemy, Google Gemini, repositorios SQL
```

```
e-commerce-chat-ai/
├── src/
│   ├── domain/                  # Capa de Dominio
│   │   ├── entities.py          # Product, ChatMessage, ChatContext
│   │   ├── repositories.py      # Interfaces IProductRepository, IChatRepository
│   │   └── exceptions.py        # Excepciones del dominio
│   ├── application/             # Capa de Aplicación
│   │   ├── dtos.py              # DTOs con validación Pydantic
│   │   ├── product_service.py   # Casos de uso de productos
│   │   └── chat_service.py      # Caso de uso del chat con IA
│   └── infrastructure/          # Capa de Infraestructura
│       ├── api/main.py          # Aplicación FastAPI y endpoints
│       ├── db/                  # Configuración BD, modelos ORM, datos iniciales
│       ├── repositories/        # Implementaciones SQL de los repositorios
│       └── llm_providers/       # Integración con Google Gemini AI
├── tests/                       # Pruebas unitarias
├── evidencias/                  # Screenshots del taller
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Requisitos Previos

- Python 3.10 o superior
- Docker y Docker Compose
- API Key de Google Gemini (https://aistudio.google.com/app/apikey)

## Instalación y Uso

### Con Docker (Recomendado)

1. Clonar el repositorio
```bash
git clone <https://github.com/juanjosediazrodriguez/TallerArqui.git>
cd e-commerce-chat-ai
```

2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
```

3. Levantar con Docker Compose
```bash
docker-compose up --build
```

4. Acceder a la API
- API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs

### Sin Docker

1. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tu GEMINI_API_KEY
```

4. Ejecutar la aplicación
```bash
uvicorn src.infrastructure.api.main:app --reload
```

## Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Estado del servicio |
| GET | `/products` | Lista todos los productos |
| GET | `/products/{id}` | Obtiene un producto por ID |
| POST | `/chat` | Envía mensaje al asistente de IA |
| GET | `/chat/history/{session_id}` | Historial de conversación |
| DELETE | `/chat/history/{session_id}` | Elimina historial de sesión |

### Ejemplo de uso del chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "usuario_001",
    "message": "Busco zapatos Nike para correr en talla 42"
  }'
```

Respuesta:
```json
{
  "session_id": "usuario_001",
  "user_message": "Busco zapatos Nike para correr en talla 42",
  "assistant_message": "¡Hola! Tenemos el Air Zoom Pegasus 40 de Nike disponible en talla 42 por $120...",
  "timestamp": "2026-04-27T02:27:13.983779"
}
```

## Ejecutar Tests

```bash
pytest -v
```

Resultado esperado: **26 tests pasados**.

## Autor

jjdiazr - Universidad EAFIT
