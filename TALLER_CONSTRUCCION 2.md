# TALLER: Construcción de E-commerce con Chat IA

**Universidad EAFIT**

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [¿Qué Vas a Construir?](#qué-vas-a-construir)
   - [Visión General del Sistema](#visión-general-del-sistema)
   - [Lógica de Negocio](#lógica-de-negocio-que-implementarás)
   - [Ejemplo Completo de Flujo](#ejemplo-completo-de-flujo-end-to-end)
3. [Objetivos de Aprendizaje](#objetivos-de-aprendizaje)
4. [Arquitectura del Sistema](#arquitectura-del-sistema)
5. [Estructura de Directorios](#estructura-de-directorios-a-crear)
6. [Requisitos Previos e Instalación](#requisitos-previos-e-instalación)
   - [Instalación de Python](#instalación-de-python)
   - [Instalación de Docker](#instalación-de-docker)
6. [Introducción Rápida a FastAPI](#introducción-rápida-a-fastapi)
7. [Entendiendo Clean Architecture](#entendiendo-clean-architecture)
8. [FASE 1: Configuración Inicial](#fase-1-configuración-inicial-del-proyecto)
9. [FASE 2: Capa de Dominio](#fase-2-capa-de-dominio-domain-layer)
10. [FASE 3: Capa de Aplicación](#fase-3-capa-de-aplicación-application-layer)
11. [FASE 4: Capa de Infraestructura](#fase-4-capa-de-infraestructura-infrastructure-layer)
12. [FASE 5: Containerización con Docker](#fase-5-containerización-con-docker)
13. [FASE 6: Testing](#fase-6-testing)
14. [FASE 7: Documentación](#fase-7-documentación)
15. [Checklist Final](#checklist-final)
16. [**ENTREGABLES DEL TALLER**](#entregables-del-taller)
    - [Repositorio de GitHub](#1-repositorio-de-github)
    - [Evidencias (Screenshots)](#2-evidencias-requeridas-screenshots)
    - [Mejores Prácticas de Git](#3-mejores-prácticas-de-git)
    - [README del Proyecto](#4-readmemd-del-proyecto)
17. [Criterios de Evaluación](#criterios-de-evaluación)
18. [Recursos Adicionales](#recursos-adicionales)

---

## Descripción del Proyecto

Construirás una **API REST de e-commerce de zapatos con chat inteligente** usando arquitectura en capas (Clean Architecture). El sistema permitirá a los usuarios consultar productos mediante un chat conversacional potenciado por Google Gemini AI.

**Duración estimada:** 8-12 horas  
**Nivel:** Intermedio-Avanzado  
**Requisitos previos:** Python, conceptos básicos de APIs REST, SQL

---

## ¿Qué Vas a Construir?

### Visión General del Sistema

Imagina una tienda online de zapatos donde los clientes pueden:
1. **Navegar productos** mediante endpoints REST tradicionales
2. **Conversar con un asistente de IA** que les ayuda a encontrar el zapato perfecto
3. El asistente **recuerda la conversación** para dar respuestas coherentes

### Lógica de Negocio que Implementarás

#### 1. **Gestión de Productos (E-commerce Básico)**

**Entidades principales:**
- **Product (Producto)**: Representa un zapato en inventario
  - Atributos: nombre, marca, categoría, talla, color, precio, stock
  - Reglas de negocio:
    - El precio debe ser mayor a 0
    - El stock no puede ser negativo
    - Solo se pueden vender productos con stock disponible
    - Al vender, el stock debe reducirse automáticamente

**Operaciones disponibles:**
- Listar todos los productos
- Buscar producto por ID
- Filtrar por marca (Nike, Adidas, Puma, etc.)
- Filtrar por categoría (Running, Casual, Formal)
- Verificar disponibilidad (stock > 0)

**Ejemplo de flujo:**
```
Cliente → GET /products → API retorna lista de zapatos
Cliente → GET /products/1 → API retorna detalles del zapato con ID 1
```

#### 2. **Chat Inteligente con IA (Funcionalidad Principal)**

**¿Cómo funciona?**

El usuario puede conversar naturalmente con un asistente de IA que conoce el inventario de zapatos.

**Flujo completo de una conversación:**

```
1. Usuario envía mensaje: "Hola, busco zapatos para correr"
   ↓
2. API recibe el mensaje y:
   - Obtiene todos los productos disponibles
   - Recupera el historial de conversación (últimos 6 mensajes)
   - Crea un contexto conversacional
   ↓
3. API envía a Google Gemini:
   - Lista de productos disponibles
   - Historial de la conversación
   - Mensaje actual del usuario
   ↓
4. Gemini AI genera respuesta contextual:
   "¡Hola! Tengo varias opciones para running. Te recomiendo:
   - Nike Air Zoom Pegasus (Talla 42, $120)
   - Adidas Ultraboost (Talla 41, $150)
   ¿Qué talla necesitas?"
   ↓
5. API guarda en base de datos:
   - Mensaje del usuario
   - Respuesta del asistente
   ↓
6. API retorna respuesta al cliente
```

**Continuación de la conversación:**

```
Usuario: "Talla 42"
   ↓
API recupera historial (recuerda que preguntó por zapatos para correr)
   ↓
Gemini responde: "Perfecto! El Nike Air Zoom Pegasus está disponible 
en talla 42 por $120. Tenemos 5 unidades en stock. ¿Te interesa?"
```

**Componentes clave:**

- **ChatMessage**: Cada mensaje en la conversación
  - Atributos: session_id, role (user/assistant), message, timestamp
  - Permite distinguir quién dijo qué

- **ChatContext**: Memoria conversacional
  - Mantiene los últimos 6 mensajes
  - Formatea el historial para enviarlo a la IA
  - Permite que la IA tenga "memoria" de la conversación

- **Session ID**: Identificador único por usuario
  - Cada usuario tiene su propia conversación
  - Las conversaciones no se mezclan entre usuarios

#### 3. **Persistencia de Datos**

**Base de Datos SQLite con dos tablas:**

**Tabla: products**
```
id | name                  | brand  | category | size | color  | price | stock
1  | Air Zoom Pegasus     | Nike   | Running  | 42   | Negro  | 120   | 5
2  | Ultraboost 21        | Adidas | Running  | 41   | Blanco | 150   | 3
3  | Suede Classic        | Puma   | Casual   | 40   | Azul   | 80    | 10
```

**Tabla: chat_memory**
```
id | session_id | role      | message                        | timestamp
1  | user123    | user      | Hola, busco zapatos para correr| 2024-01-15 10:30:00
2  | user123    | assistant | ¡Hola! Tengo varias opciones...| 2024-01-15 10:30:02
3  | user123    | user      | Talla 42                       | 2024-01-15 10:31:00
4  | user123    | assistant | Perfecto! El Nike Air Zoom...  | 2024-01-15 10:31:01
```

#### 4. **Arquitectura en 3 Capas (Clean Architecture)**

**¿Por qué 3 capas?**

Para separar responsabilidades y hacer el código mantenible:

**CAPA DE DOMINIO (Núcleo del negocio)**
- Define QUÉ es un producto, QUÉ es un mensaje de chat
- Establece las reglas: "el precio debe ser > 0"
- NO sabe nada de bases de datos o APIs
- Es puro Python, sin dependencias externas

**CAPA DE APLICACIÓN (Casos de uso)**
- Define CÓMO se usan las entidades del dominio
- Orquesta: "Para procesar un mensaje de chat, necesito obtener productos, recuperar historial, llamar a la IA, y guardar todo"
- Coordina entre dominio e infraestructura
- Implementa la lógica de negocio de alto nivel

**CAPA DE INFRAESTRUCTURA (Detalles técnicos)**
- Define DÓNDE y CON QUÉ se guardan los datos
- Implementa: FastAPI, SQLAlchemy, Google Gemini
- Se puede cambiar (de SQLite a PostgreSQL) sin afectar el dominio
- Contiene todos los frameworks y librerías

### Ejemplo Completo de Flujo End-to-End

**Escenario:** Un cliente quiere comprar zapatos Nike para correr

```
1. CLIENTE hace request:
   POST /chat
   {
     "session_id": "cliente_001",
     "message": "Quiero zapatos Nike para correr, talla 42"
   }

2. INFRAESTRUCTURA (FastAPI endpoint):
   - Recibe el request HTTP
   - Valida datos con Pydantic
   - Crea instancias de repositorios y servicios

3. APLICACIÓN (ChatService):
   - Obtiene productos del ProductRepository
   - Obtiene historial del ChatRepository
   - Crea ChatContext con historial
   - Llama a GeminiService con: mensaje + productos + contexto

4. INFRAESTRUCTURA (GeminiService):
   - Formatea prompt para Gemini AI
   - Envía request a Google Gemini API
   - Recibe respuesta de la IA

5. APLICACIÓN (ChatService):
   - Crea entidad ChatMessage para mensaje del usuario
   - Crea entidad ChatMessage para respuesta del asistente
   - Guarda ambos mensajes usando ChatRepository

6. INFRAESTRUCTURA (ChatRepository):
   - Convierte entidades a modelos ORM
   - Guarda en base de datos SQLite
   - Hace commit de la transacción

7. APLICACIÓN (ChatService):
   - Crea ChatMessageResponseDTO
   - Retorna al endpoint

8. INFRAESTRUCTURA (FastAPI endpoint):
   - Serializa DTO a JSON
   - Envía response HTTP al cliente

9. CLIENTE recibe:
   {
     "session_id": "cliente_001",
     "user_message": "Quiero zapatos Nike para correr, talla 42",
     "assistant_message": "¡Perfecto! Tengo el Nike Air Zoom Pegasus en talla 42 por $120. Tenemos 5 unidades disponibles. Es ideal para correr con excelente amortiguación. ¿Te gustaría más información?",
     "timestamp": "2024-01-15T10:30:00"
   }
```

### Tecnologías y Su Propósito

| Tecnología | Propósito | Dónde se usa |
|------------|-----------|--------------|
| **FastAPI** | Framework web para crear endpoints HTTP | Capa de Infraestructura (API) |
| **Pydantic** | Validación automática de datos | Capa de Aplicación (DTOs) |
| **SQLAlchemy** | ORM para interactuar con base de datos | Capa de Infraestructura (Repositorios) |
| **SQLite** | Base de datos ligera | Capa de Infraestructura (Persistencia) |
| **Google Gemini** | IA conversacional | Capa de Infraestructura (Servicio externo) |
| **Docker** | Containerización de la aplicación | Deployment |
| **Pytest** | Testing unitario | Testing |

### Lo Que Aprenderás Haciendo

1. **Separación de responsabilidades**: Cada capa tiene un propósito claro
2. **Inyección de dependencias**: Los servicios reciben lo que necesitan, no lo crean
3. **Patrón Repository**: Abstracción del acceso a datos
4. **DTOs**: Transferencia segura de datos entre capas
5. **Validaciones**: En múltiples niveles (entidades, DTOs, API)
6. **Integración con IA**: Cómo usar APIs externas manteniendo arquitectura limpia
7. **Gestión de contexto**: Cómo mantener memoria conversacional
8. **Containerización**: Empaquetar la aplicación para deployment

---

### IMPORTANTE: Entregables

Al finalizar el taller, deberás entregar:

1. **Repositorio de GitHub** con el código completo
2. **6 Screenshots** (evidencias) en carpeta `evidencias/`:
   - Swagger UI de la API
   - Logs de Docker
   - Docker corriendo
   - Llamado a `/products` desde Postman/Insomnia
   - Llamado a `/chat` con respuesta de IA
   - Base de datos con productos
3. **README.md** completo con instrucciones
4. **Código completamente documentado** (docstrings en todas las clases y métodos)
5. **Commits siguiendo convenciones** (feat:, fix:, docs:, etc.)

**Todas las evidencias deben mostrar que es tu computadora** (nombre de usuario, fecha/hora visible)

Ver sección completa de [ENTREGABLES](#entregables-del-taller) para más detalles.

---

## Objetivos de Aprendizaje

Al completar este taller, habrás aprendido:

1. Implementar **Clean Architecture** con 3 capas
2. Aplicar patrones de diseño: **Repository**, **Service Layer**, **Dependency Injection**
3. Crear APIs REST con **FastAPI**
4. Integrar **IA conversacional** (Google Gemini)
5. Gestionar **contexto conversacional** con memoria
6. Usar **SQLAlchemy** como ORM
7. Containerizar con **Docker**
8. Validar datos con **Pydantic**

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend)                       │
│                  (Navegador, Postman, etc.)                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI (main.py)                                   │  │
│  │  - Endpoints HTTP                                    │  │
│  │  - Validación de requests                            │  │
│  │  - Serialización de responses                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Repositories (SQLAlchemy)                           │  │
│  │  - product_repository.py                             │  │
│  │  - chat_repository.py                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  External Services                                   │  │
│  │  - gemini_service.py (Google Gemini AI)              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Services (Casos de Uso)                             │  │
│  │  - product_service.py                                │  │
│  │  - chat_service.py                                   │  │
│  │  Orquesta: Repositorios + Servicios Externos         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DTOs (Data Transfer Objects)                        │  │
│  │  - Validación con Pydantic                           │  │
│  │  - Transformación de datos                           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              DOMAIN LAYER                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Entities (Lógica de Negocio)                        │  │
│  │  - Product                                           │  │
│  │  - ChatMessage                                       │  │
│  │  - ChatContext                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Repositories (Interfaces)                           │  │
│  │  - IProductRepository                                │  │
│  │  - IChatRepository                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Exceptions (Excepciones del Dominio)                │  │
│  │  - ProductNotFoundError                              │  │
│  │  - InvalidProductDataError                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Estructura de Directorios a Crear

```
e-commerce-chat-ai/
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # Configuración global
│   │
│   ├── domain/                        # 🔷 CAPA DE DOMINIO
│   │   ├── __init__.py
│   │   ├── entities.py                # Product, ChatMessage, ChatContext
│   │   ├── repositories.py            # IProductRepository, IChatRepository
│   │   └── exceptions.py              # Excepciones del dominio
│   │
│   ├── application/                   # 🔶 CAPA DE APLICACIÓN
│   │   ├── __init__.py
│   │   ├── dtos.py                    # DTOs con Pydantic
│   │   ├── product_service.py         # Servicio de productos
│   │   └── chat_service.py            # Servicio de chat
│   │
│   └── infrastructure/                # 🔸 CAPA DE INFRAESTRUCTURA
│       ├── __init__.py
│       │
│       ├── api/                       # FastAPI
│       │   ├── __init__.py
│       │   └── main.py                # Aplicación FastAPI
│       │
│       ├── db/                        # Base de Datos
│       │   ├── __init__.py
│       │   ├── database.py            # Configuración SQLAlchemy
│       │   ├── models.py              # Modelos ORM
│       │   └── init_data.py           # Datos iniciales
│       │
│       ├── repositories/              # Implementaciones
│       │   ├── __init__.py
│       │   ├── product_repository.py
│       │   └── chat_repository.py
│       │
│       └── llm_providers/             # Proveedores de IA
│           ├── __init__.py
│           └── gemini_service.py
│
├── tests/                             # Tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── data/                              # Base de datos (se crea automáticamente)
│   └── ecommerce_chat.db
│
├── .env                               # Variables de entorno (NO versionar)
├── .env.example                       # Ejemplo de variables
├── .gitignore
├── .dockerignore
│
├── Dockerfile                         # Imagen Docker
├── docker-compose.yml                 # Orquestación
│
├── requirements.txt                   # Dependencias Python
├── pyproject.toml                     # Configuración pytest
│
└── README.md                          # Documentación
```

---

## Requisitos Previos e Instalación

### Instalación de Python

Asegúrate de tener Python 3.10 o superior instalado:

```bash
python --version
# Debe mostrar Python 3.10.x o superior
```

Si no lo tienes instalado:
- **Windows**: Descarga desde https://www.python.org/downloads/
- **Mac**: Usa Homebrew: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11` (Ubuntu/Debian)

### Instalación de Docker

Docker es necesario para la FASE 5 del taller. Puedes instalarlo ahora o cuando llegues a esa fase.

#### Windows

**Opción 1: Docker Desktop (Recomendado)**

1. **Requisitos previos**:
   - Windows 10 64-bit: Pro, Enterprise o Education (Build 19041 o superior)
   - O Windows 11
   - Habilitar WSL 2 (Windows Subsystem for Linux)

2. **Habilitar WSL 2**:
   ```powershell
   # Ejecutar en PowerShell como Administrador
   wsl --install
   ```
   Reinicia tu computadora después de esto.

3. **Descargar Docker Desktop**:
   - Ve a: https://www.docker.com/products/docker-desktop/
   - Descarga "Docker Desktop for Windows"
   - Ejecuta el instalador
   - Sigue las instrucciones del instalador
   - Asegúrate de seleccionar "Use WSL 2 instead of Hyper-V"

4. **Verificar instalación**:
   ```powershell
   docker --version
   docker-compose --version
   ```

**Opción 2: Docker con WSL 2 (Alternativa)**

Si no puedes usar Docker Desktop, puedes instalar Docker directamente en WSL 2:
- Sigue la guía: https://docs.docker.com/engine/install/ubuntu/

#### Mac

**Docker Desktop para Mac**

1. **Requisitos previos**:
   - macOS 11 o superior
   - Mac con chip Apple Silicon (M1/M2) o Intel

2. **Descargar e instalar**:
   - Ve a: https://www.docker.com/products/docker-desktop/
   - Descarga "Docker Desktop for Mac"
   - Selecciona la versión correcta:
     - **Apple Silicon** (M1/M2/M3)
     - **Intel Chip**
   - Abre el archivo .dmg descargado
   - Arrastra Docker a la carpeta Applications
   - Abre Docker desde Applications
   - Sigue las instrucciones de configuración inicial

3. **Verificar instalación**:
   ```bash
   docker --version
   docker-compose --version
   ```

#### Linux (Ubuntu/Debian)

```bash
# Actualizar paquetes
sudo apt-get update

# Instalar dependencias
sudo apt-get install ca-certificates curl gnupg lsb-release

# Agregar la clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verificar instalación
docker --version
docker compose version
```

**Configurar Docker sin sudo (opcional)**:
```bash
sudo usermod -aG docker $USER
# Cierra sesión y vuelve a iniciar para aplicar cambios
```

### Verificación de Instalación

Una vez instalado Docker, verifica que funciona correctamente:

```bash
# Ejecutar contenedor de prueba
docker run hello-world

# Si ves un mensaje de bienvenida, Docker está funcionando correctamente
```

### Editor de Código Recomendado

- **Visual Studio Code**: https://code.visualstudio.com/
  - Extensiones recomendadas:
    - Python
    - Pylance
    - Docker
    - SQLite Viewer

---

## Introducción Rápida a FastAPI

FastAPI es un framework moderno y rápido para construir APIs con Python. Aquí algunos conceptos clave:

### Características Principales

- **Rápido**: Alto rendimiento, comparable con NodeJS y Go
- **Fácil**: Diseñado para ser intuitivo y fácil de usar
- **Documentación automática**: Genera documentación interactiva automáticamente
- **Type hints**: Usa anotaciones de tipo de Python
- **Validación automática**: Valida datos con Pydantic

### Ejemplo Básico

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Ejecutar la Aplicación

```bash
uvicorn main:app --reload
```

- Accede a la documentación interactiva en: http://localhost:8000/docs
- Documentación alternativa en: http://localhost:8000/redoc

### Recursos de Aprendizaje

- **Tutorial oficial**: https://fastapi.tiangolo.com/tutorial/
- **Documentación completa**: https://fastapi.tiangolo.com/
- **Ejemplos**: https://github.com/tiangolo/fastapi/tree/master/docs_src

---

## Entendiendo Clean Architecture

Antes de comenzar, es fundamental entender qué es cada capa y por qué las separamos:

### CAPA DE DOMINIO (Domain Layer)
**¿Qué es?** El corazón de tu aplicación. Contiene las reglas de negocio puras, independientes de frameworks o bases de datos.

**Contiene:**
- **Entidades**: Objetos que representan conceptos del negocio (Product, ChatMessage)
- **Interfaces de Repositorios**: Contratos que definen cómo acceder a datos (sin implementación)
- **Excepciones del Dominio**: Errores específicos del negocio

**Regla de Oro:** Esta capa NO debe importar nada de las otras capas. Es completamente independiente.

### CAPA DE APLICACIÓN (Application Layer)
**¿Qué es?** Orquesta los casos de uso de tu aplicación. Coordina el flujo entre el dominio y la infraestructura.

**Contiene:**
- **Services**: Implementan casos de uso específicos (crear producto, procesar chat)
- **DTOs**: Objetos para transferir datos entre capas con validación

**Regla de Oro:** Puede importar del dominio, pero NO de infraestructura. Recibe dependencias por inyección.

### CAPA DE INFRAESTRUCTURA (Infrastructure Layer)
**¿Qué es?** Implementa los detalles técnicos: bases de datos, APIs externas, frameworks web.

**Contiene:**
- **Repositorios**: Implementaciones concretas de las interfaces del dominio
- **API (FastAPI)**: Endpoints HTTP
- **Servicios Externos**: Integración con Gemini AI
- **Modelos ORM**: Representación de tablas de base de datos

**Regla de Oro:** Puede importar de todas las capas. Es la capa más externa.

---

## FASE 1: Configuración Inicial del Proyecto

### Paso 1.1: Crear Estructura de Directorios

**Tarea:** Crea la estructura completa de carpetas mostrada arriba.

**Comandos para ejecutar:**

```bash
# Crear el proyecto
mkdir e-commerce-chat-ai
cd e-commerce-chat-ai

# Crear estructura de carpetas
mkdir -p src/domain
mkdir -p src/application
mkdir -p src/infrastructure/api
mkdir -p src/infrastructure/db
mkdir -p src/infrastructure/repositories
mkdir -p src/infrastructure/llm_providers
mkdir -p tests
mkdir -p data

# Crear archivos __init__.py
touch src/__init__.py
touch src/domain/__init__.py
touch src/application/__init__.py
touch src/infrastructure/__init__.py
touch src/infrastructure/api/__init__.py
touch src/infrastructure/db/__init__.py
touch src/infrastructure/repositories/__init__.py
touch src/infrastructure/llm_providers/__init__.py
touch tests/__init__.py
```

**Checkpoint:** Verifica que tienes todas las carpetas y archivos `__init__.py`

---

### Paso 1.2: Configurar Entorno Virtual y Dependencias

**Tarea:** Configura el entorno Python e instala dependencias.

**Comandos para ejecutar:**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

**Crear archivo `requirements.txt`:**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
google-generativeai==0.3.1
pytest==7.4.3
httpx==0.25.1
```

**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**Checkpoint:** Ejecuta `pip list` y verifica que todas las dependencias estén instaladas

---

### Paso 1.3: Configurar Variables de Entorno

**Tarea:** Crea archivos `.env` y `.env.example`

**Crear archivo `.env.example` (plantilla para versionar):**

```bash
GEMINI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development
```

**Crear archivo `.env` (con tus valores reales):**

```bash
GEMINI_API_KEY=AIzaSy...  # Tu API key real de Google Gemini
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development
```

**Obtener tu API Key de Gemini:**
1. Ve a: https://aistudio.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API key
4. Cópiala y pégala en tu archivo `.env`

**Crear archivo `.gitignore`:**

```txt
# Entorno virtual
venv/
env/

# Variables de entorno
.env

# Base de datos
data/
*.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
```

**Checkpoint:** Archivo `.env` creado con tu API key real y `.gitignore` configurado

---

## FASE 2: Capa de Dominio (Domain Layer)

**Recordatorio:** Esta capa contiene la lógica de negocio pura. NO debe depender de frameworks, bases de datos o servicios externos.

### Paso 2.1: Crear Entidades del Dominio

**Archivo:** `src/domain/entities.py`

**¿Qué son las Entidades?** Son objetos que representan conceptos importantes de tu negocio. Contienen datos Y comportamiento (lógica de negocio).

**Código de inicio:**

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# TODO: Implementar las entidades Product, ChatMessage y ChatContext
```

---

#### Entidad: `Product`

**¿Qué representa?** Un producto (zapato) en tu e-commerce.

**Código de inicio:**

```python
@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    Contiene la lógica de negocio relacionada con productos.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str
    
    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        TODO: Implementar validaciones:
        - price debe ser mayor a 0
        - stock no puede ser negativo
        - name no puede estar vacío
        Lanza ValueError si alguna validación falla
        """
        pass  # Implementa aquí las validaciones
    
    def is_available(self) -> bool:
        """
        TODO: Retorna True si el producto tiene stock disponible
        """
        pass
    
    def reduce_stock(self, quantity: int) -> None:
        """
        TODO: Reduce el stock del producto
        - Valida que quantity sea positivo
        - Valida que haya suficiente stock
        - Lanza ValueError si no se puede reducir
        """
        pass
    
    def increase_stock(self, quantity: int) -> None:
        """
        TODO: Aumenta el stock del producto
        - Valida que quantity sea positivo
        """
        pass
```

**Lo que debes implementar:**
1. Validaciones en `__post_init__()`: price > 0, stock >= 0, name no vacío
2. `is_available()`: retorna `self.stock > 0`
3. `reduce_stock()`: valida y reduce el stock
4. `increase_stock()`: valida y aumenta el stock

---

#### Entidad: `ChatMessage`

**¿Qué representa?** Un mensaje en la conversación entre el usuario y el asistente de IA.

**Código de inicio:**

```python
@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime
    
    def __post_init__(self):
        """
        TODO: Implementar validaciones:
        - role debe ser 'user' o 'assistant'
        - message no puede estar vacío
        - session_id no puede estar vacío
        """
        pass
    
    def is_from_user(self) -> bool:
        """
        TODO: Retorna True si el mensaje es del usuario
        """
        pass
    
    def is_from_assistant(self) -> bool:
        """
        TODO: Retorna True si el mensaje es del asistente
        """
        pass
```

**Lo que debes implementar:**
1. Validar que `role` sea 'user' o 'assistant'
2. Validar que `message` y `session_id` no estén vacíos
3. Implementar los métodos de verificación de rol

---

#### Value Object: `ChatContext`

**¿Qué representa?** El contexto conversacional. Mantiene los mensajes recientes para que la IA tenga memoria.

**Código de inicio:**

```python
@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.
    """
    messages: list[ChatMessage]
    max_messages: int = 6
    
    def get_recent_messages(self) -> list[ChatMessage]:
        """
        TODO: Retorna los últimos N mensajes (max_messages)
        Pista: Usa slicing de Python messages[-self.max_messages:]
        """
        pass
    
    def format_for_prompt(self) -> str:
        """
        TODO: Formatea los mensajes para incluirlos en el prompt de IA
        Formato esperado:
        "Usuario: mensaje del usuario
        Asistente: respuesta del asistente
        Usuario: otro mensaje
        ..."
        
        Pista: Itera sobre get_recent_messages() y construye el string
        """
        pass
```

**Lo que debes implementar:**
1. `get_recent_messages()`: retorna los últimos N mensajes usando slicing
2. `format_for_prompt()`: crea un string formateado con el historial

**Checkpoint:** Todas las entidades creadas con validaciones funcionando. Prueba crear objetos y verifica que las validaciones lancen errores cuando corresponda.

---

### Paso 2.2: Crear Interfaces de Repositorios

**Archivo:** `src/domain/repositories.py`

**¿Qué son las Interfaces de Repositorio?** Son contratos que definen CÓMO acceder a los datos, pero NO implementan el acceso. Esto permite que el dominio sea independiente de la base de datos.

**Código de inicio:**

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage

# TODO: Implementar las interfaces IProductRepository e IChatRepository
```

---

#### Interface: `IProductRepository`

**¿Para qué sirve?** Define las operaciones que se pueden hacer con productos, sin especificar si se usa SQL, MongoDB, archivos, etc.

**Código de inicio:**

```python
class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    Las implementaciones concretas estarán en la capa de infraestructura.
    """
    
    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        TODO: Define el método para obtener todos los productos
        No implementes nada, solo la firma del método
        """
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        TODO: Define el método para obtener un producto por ID
        Retorna None si no existe
        """
        pass
    
    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """TODO: Obtiene productos de una marca específica"""
        pass
    
    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """TODO: Obtiene productos de una categoría específica"""
        pass
    
    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        TODO: Guarda o actualiza un producto
        Si tiene ID, actualiza. Si no tiene ID, crea uno nuevo
        Retorna el producto guardado (con ID asignado si es nuevo)
        """
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        TODO: Elimina un producto por ID
        Retorna True si se eliminó, False si no existía
        """
        pass
```

---

#### Interface: `IChatRepository`

**¿Para qué sirve?** Define cómo guardar y recuperar mensajes del chat para mantener el historial conversacional.

**Código de inicio:**

```python
class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones.
    """
    
    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        TODO: Guarda un mensaje en el historial
        Retorna el mensaje guardado con su ID
        """
        pass
    
    @abstractmethod
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        TODO: Obtiene el historial completo de una sesión
        Si limit está definido, retorna solo los últimos N mensajes
        Los mensajes deben estar en orden cronológico (más antiguos primero)
        """
        pass
    
    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        TODO: Elimina todo el historial de una sesión
        Retorna la cantidad de mensajes eliminados
        """
        pass
    
    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        TODO: Obtiene los últimos N mensajes de una sesión
        Crucial para mantener el contexto conversacional
        Retorna en orden cronológico
        """
        pass
```

**Lo que debes implementar:**
- Solo las firmas de los métodos con `@abstractmethod`
- NO implementes la lógica (eso va en Infrastructure)
- Documenta qué hace cada método

**Checkpoint:** Interfaces definidas. Verifica que no puedas instanciar estas clases directamente (son abstractas).

---

### Paso 2.3: Crear Excepciones del Dominio

**Archivo:** `src/domain/exceptions.py`

**¿Para qué sirven?** Las excepciones del dominio representan errores de negocio específicos. Son más descriptivas que excepciones genéricas.

**Código de inicio:**

```python
"""
Excepciones específicas del dominio.
Representan errores de negocio, no errores técnicos.
"""

class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.
    
    TODO: Implementa el constructor:
    - Debe aceptar un product_id opcional
    - Mensaje por defecto: "Producto no encontrado"
    - Si se pasa product_id: "Producto con ID {product_id} no encontrado"
    """
    pass


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.
    
    TODO: Implementa el constructor:
    - Debe aceptar un mensaje personalizado
    - Mensaje por defecto: "Datos de producto inválidos"
    """
    pass


class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.
    
    TODO: Implementa el constructor:
    - Debe aceptar un mensaje personalizado
    - Mensaje por defecto: "Error en el servicio de chat"
    """
    pass
```

**Ejemplo de implementación para guiarte:**

```python
class ProductNotFoundError(Exception):
    def __init__(self, product_id: int = None):
        if product_id:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)
```

**Lo que debes implementar:**
- Constructores para cada excepción
- Mensajes descriptivos por defecto
- Capacidad de personalizar mensajes

**Checkpoint:** Excepciones definidas. Prueba lanzarlas y capturarlas para verificar que funcionan.

---

## FASE 3: Capa de Aplicación (Application Layer)

**Recordatorio:** Esta capa orquesta los casos de uso. Coordina el dominio con la infraestructura usando Dependency Injection.

### Paso 3.1: Crear DTOs (Data Transfer Objects)

**Archivo:** `src/application/dtos.py`

**¿Qué son los DTOs?** Objetos para transferir datos entre capas. Usan Pydantic para validación automática.

**Código de inicio:**

```python
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

# TODO: Implementar los DTOs
```

#### DTO: `ProductDTO`

**Código de inicio:**

```python
class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos.
    Pydantic valida automáticamente los tipos.
    """
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str
    
    @validator('price')
    def price_must_be_positive(cls, v):
        """TODO: Valida que el precio sea mayor a 0"""
        pass
    
    @validator('stock')
    def stock_must_be_non_negative(cls, v):
        """TODO: Valida que el stock no sea negativo"""
        pass
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM
```

---

#### DTO: `ChatMessageRequestDTO`

**Código de inicio:**

```python
class ChatMessageRequestDTO(BaseModel):
    """DTO para recibir mensajes del usuario"""
    session_id: str
    message: str
    
    @validator('message')
    def message_not_empty(cls, v):
        """TODO: Valida que el mensaje no esté vacío"""
        pass
    
    @validator('session_id')
    def session_id_not_empty(cls, v):
        """TODO: Valida que session_id no esté vacío"""
        pass
```

---

#### DTO: `ChatMessageResponseDTO`

**Código de inicio:**

```python
class ChatMessageResponseDTO(BaseModel):
    """DTO para enviar respuestas del chat"""
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime
```

---

#### DTO: `ChatHistoryDTO`

```python
class ChatHistoryDTO(BaseModel):
    """DTO para mostrar historial de chat"""
    id: int
    role: str
    message: str
    timestamp: datetime
    
    class Config:
        from_attributes = True
```

**Lo que debes implementar:**
- Validadores en ProductDTO y ChatMessageRequestDTO
- Los validadores deben lanzar `ValueError` si la validación falla

**Checkpoint:** DTOs con validación Pydantic funcionando. Prueba crear DTOs con datos inválidos y verifica que lance errores.

---

### Paso 3.2: Implementar ProductService

**Archivo:** `src/application/product_service.py`

**Tarea:** Crea el servicio de aplicación para productos

**Constructor:**
- Recibe `IProductRepository` por dependency injection

**Métodos a implementar:**
- `get_all_products()` - Lista todos los productos
- `get_product_by_id(product_id)` - Busca por ID, lanza excepción si no existe
- `search_products(filters)` - Filtra productos por criterios
- `create_product(product_dto)` - Crea nuevo producto
- `update_product(product_id, product_dto)` - Actualiza producto
- `delete_product(product_id)` - Elimina producto
- `get_available_products()` - Solo productos con stock

**Sugerencias:**
- Usa el repositorio inyectado, no lo crees aquí
- Convierte DTOs a entidades antes de guardar
- Lanza excepciones del dominio en caso de error
- Valida que el producto existe antes de actualizar/eliminar

**Checkpoint:** Servicio implementado con todos los métodos

---

### Paso 3.3: Implementar ChatService

**Archivo:** `src/application/chat_service.py`

**Tarea:** Crea el servicio de chat con IA

**Constructor:**
- Recibe `IProductRepository`
- Recibe `IChatRepository`
- Recibe `ai_service` (GeminiService)

**Método principal: `process_message(request: ChatMessageRequestDTO)`**

**Flujo a implementar:**
1. Obtener todos los productos del repositorio
2. Obtener historial reciente (últimos 6 mensajes)
3. Crear `ChatContext` con el historial
4. Llamar a `ai_service.generate_response()` con:
   - Mensaje del usuario
   - Lista de productos
   - Contexto conversacional
5. Guardar mensaje del usuario en el repositorio
6. Guardar respuesta del asistente en el repositorio
7. Retornar `ChatMessageResponseDTO`

**Métodos adicionales:**
- `get_session_history(session_id, limit)` - Obtiene historial
- `clear_session_history(session_id)` - Elimina historial

**Sugerencias:**
- Usa `async/await` para llamadas a IA
- Maneja errores con try/except
- Usa `datetime.utcnow()` para timestamps
- El contexto es clave para respuestas coherentes

**Checkpoint:** Servicio de chat implementado (sin IA aún)

---

## FASE 4: Capa de Infraestructura (Infrastructure Layer)

### Paso 4.1: Configurar Base de Datos

**Archivo:** `src/infrastructure/db/database.py`

**Tarea:** Configura SQLAlchemy

**Componentes necesarios:**
- `engine` - Motor de conexión a SQLite
- `SessionLocal` - Factory de sesiones
- `Base` - Clase base para modelos ORM
- `get_db()` - Dependency para FastAPI (usa `yield`)
- `init_db()` - Inicializa BD y carga datos

**Sugerencias:**
- URL de SQLite: `sqlite:///./data/ecommerce_chat.db`
- Usa `check_same_thread=False` para SQLite
- `get_db()` debe usar `yield` y `finally` para cerrar sesión
- `init_db()` llama a `Base.metadata.create_all()`

---

**Archivo:** `src/infrastructure/db/models.py`

**Tarea:** Define modelos ORM con SQLAlchemy

#### Modelo: `ProductModel`
**Tabla:** `products`
**Columnas:**
- `id` - Integer, primary_key, autoincrement
- `name` - String(200), not null
- `brand` - String(100)
- `category` - String(100)
- `size` - String(20)
- `color` - String(50)
- `price` - Float
- `stock` - Integer
- `description` - Text

---

#### Modelo: `ChatMemoryModel`
**Tabla:** `chat_memory`
**Columnas:**
- `id` - Integer, primary_key
- `session_id` - String(100), indexed
- `role` - String(20)
- `message` - Text
- `timestamp` - DateTime, default=utcnow

**Sugerencias:**
- Hereda de `Base`
- Usa `__tablename__` para nombre de tabla
- Agrega índices en columnas de búsqueda frecuente
- Documenta cada columna

---

**Archivo:** `src/infrastructure/db/init_data.py`

**Tarea:** Crea función para cargar datos iniciales

**Función: `load_initial_data()`**
- Verifica si ya existen productos
- Si no existen, crea 10 productos de ejemplo
- Productos variados: Nike, Adidas, Puma, etc.
- Diferentes categorías: Running, Casual, Formal
- Precios entre $50 y $200
- Stock variado

**Sugerencias:**
- Usa `session.query().count()` para verificar
- Crea productos realistas y variados
- Usa `session.add_all()` para insertar múltiples
- Haz `commit()` al final

**Checkpoint:** Base de datos configurada y con datos iniciales

---

### Paso 4.2: Implementar Repositorios

**Archivo:** `src/infrastructure/repositories/product_repository.py`

**Tarea:** Implementa `SQLProductRepository(IProductRepository)`

**Métodos a implementar:**
- `get_all()` - Query a ProductModel
- `get_by_id()` - Filter por ID
- `get_by_brand()` - Filter por brand
- `get_by_category()` - Filter por category
- `save()` - Add/Update según tenga ID
- `delete()` - Delete por ID

**Métodos auxiliares:**
- `_model_to_entity(model)` - Convierte ORM → Entity
- `_entity_to_model(entity)` - Convierte Entity → ORM

**Sugerencias:**
- Usa `self.db.query(ProductModel)`
- Usa `.filter()`, `.all()`, `.first()`
- Siempre convierte modelos ORM a entidades del dominio
- Haz `commit()` después de modificaciones
- Usa `refresh()` para obtener ID generado

---

**Archivo:** `src/infrastructure/repositories/chat_repository.py`

**Tarea:** Implementa `SQLChatRepository(IChatRepository)`

**Métodos a implementar:**
- `save_message()` - Guarda mensaje
- `get_session_history()` - Obtiene historial con limit
- `delete_session_history()` - Elimina por session_id
- `get_recent_messages()` - Últimos N mensajes ordenados

**Métodos auxiliares:**
- `_model_to_entity(model)` - ORM → Entity
- `_entity_to_model(entity)` - Entity → ORM

**Sugerencias:**
- Usa `.order_by(timestamp.desc())` para orden
- Usa `.limit()` para limitar resultados
- Invierte lista con `.reverse()` para orden cronológico
- El orden correcto es crucial para el contexto

**Checkpoint:** Repositorios implementados y funcionando

---

### Paso 4.3: Integrar Google Gemini AI

**Archivo:** `src/infrastructure/llm_providers/gemini_service.py`

**Tarea:** Implementa servicio de IA con Gemini

**Clase: `GeminiService`**

**Constructor:**
- Carga `GEMINI_API_KEY` desde variables de entorno
- Configura cliente de Gemini
- Inicializa modelo: `gemini-2.5-flash`

**Método: `generate_response(user_message, products, context)`**

**Flujo:**
1. Formatear lista de productos en texto
2. Formatear contexto conversacional
3. Construir prompt completo con:
   - Instrucciones del sistema
   - Lista de productos disponibles
   - Historial de conversación
   - Mensaje actual del usuario
4. Llamar a Gemini API
5. Retornar respuesta generada

**Método auxiliar: `format_products_info(products)`**
- Convierte lista de productos a texto legible
- Formato: "- Nombre | Marca | Precio | Stock"

**Prompt del sistema (sugerido):**
```
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
[lista de productos]

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Si no tienes información, sé honesto

[historial de conversación]

Usuario: [mensaje actual]

Asistente:
```

**Sugerencias:**
- Usa `google.generativeai` library
- Maneja errores de API con try/except
- Usa `async/await` para llamadas
- El prompt es crucial para buenas respuestas
- Incluye contexto para coherencia

**Checkpoint:** Servicio de IA funcionando con respuestas coherentes

---

### Paso 4.4: Crear API con FastAPI

**Archivo:** `src/infrastructure/api/main.py`

**Tarea:** Implementa la aplicación FastAPI

**Inicialización:**
- Crea instancia de FastAPI con título y descripción
- Configura CORS middleware
- Define evento `startup` que llama a `init_db()`

**Endpoints a implementar:**

#### `GET /`
- Retorna información básica de la API
- Versión, descripción, endpoints disponibles

#### `GET /products`
- Lista todos los productos
- Response model: `List[ProductDTO]`
- Usa `Depends(get_db)` para obtener sesión
- Crea repositorio y servicio
- Retorna productos

#### `GET /products/{product_id}`
- Obtiene producto por ID
- Path parameter: `product_id`
- Lanza HTTPException 404 si no existe
- Response model: `ProductDTO`

#### `POST /chat`
- Procesa mensaje de chat
- Request body: `ChatMessageRequestDTO`
- Response model: `ChatMessageResponseDTO`
- Crea todos los servicios necesarios
- Maneja errores con HTTPException 500

#### `GET /chat/history/{session_id}`
- Obtiene historial de sesión
- Path parameter: `session_id`
- Query parameter: `limit` (default: 10)
- Response model: `List[ChatHistoryDTO]`

#### `DELETE /chat/history/{session_id}`
- Elimina historial de sesión
- Retorna cantidad de mensajes eliminados

#### `GET /health`
- Health check endpoint
- Retorna status y timestamp

**Sugerencias:**
- Usa decoradores: `@app.get()`, `@app.post()`, etc.
- Usa `Depends(get_db)` para inyectar sesión
- Crea repositorios y servicios en cada endpoint
- Usa `async def` para endpoints con IA
- Maneja errores con `HTTPException`
- Documenta cada endpoint con docstrings

**Checkpoint:** API completa con todos los endpoints funcionando

---

## FASE 5: Containerización con Docker

### Paso 5.1: Crear Dockerfile

**Archivo:** `Dockerfile`

**Tarea:** Define imagen Docker para la aplicación

**Estructura sugerida:**
1. FROM python:3.11-slim
2. WORKDIR /app
3. COPY requirements.txt
4. RUN pip install --no-cache-dir -r requirements.txt
5. COPY . .
6. EXPOSE 8000
7. CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

**Sugerencias:**
- Usa imagen slim para reducir tamaño
- Copia requirements.txt primero (cache de layers)
- No copies archivos innecesarios (usa .dockerignore)
- Expone puerto 8000

---

### Paso 5.2: Crear docker-compose.yml

**Archivo:** `docker-compose.yml`

**Tarea:** Define orquestación de servicios

**Servicio: `api`**
- build: context y dockerfile
- container_name: ecommerce-api
- ports: "8000:8000"
- environment: GEMINI_API_KEY, DATABASE_URL
- env_file: .env
- volumes: 
  - ./data:/app/data (persistencia)
  - .:/app (desarrollo)
- command: uvicorn con --reload
- restart: unless-stopped

**Volúmenes:**
- db-data: para persistencia

**Networks:**
- app-network: para comunicación

**Sugerencias:**
- Usa variables de entorno para configuración
- Monta volumen para datos persistentes
- Usa --reload solo en desarrollo
- Configura health check

**Checkpoint:** Aplicación corriendo en Docker

---

## FASE 6: Testing

### Paso 6.1: Configurar Pytest

**Archivo:** `pyproject.toml`

**Tarea:** Configura pytest

**Configuración:**
- testpaths = ["tests"]
- python_files = ["test_*.py"]
- python_classes = ["Test*"]
- python_functions = ["test_*"]

---

### Paso 6.2: Crear Tests Unitarios

**Archivo:** `tests/test_entities.py`

**Tests a implementar:**
- Test validaciones de Product
- Test métodos de Product (is_available, reduce_stock)
- Test validaciones de ChatMessage
- Test ChatContext.format_for_prompt()

---

**Archivo:** `tests/test_services.py`

**Tests a implementar:**
- Test ProductService con mock repository
- Test ChatService con mocks
- Test manejo de excepciones

**Sugerencias:**
- Usa `pytest.fixture` para setup
- Crea mocks de repositorios
- Usa `pytest.raises` para excepciones
- Cubre casos edge

**Checkpoint:** Tests pasando con >80% coverage

---

## FASE 7: Documentación

### Paso 7.1: Crear README.md

**Secciones necesarias:**
- Descripción del proyecto
- Características principales
- Arquitectura (diagrama)
- Instalación
- Configuración
- Uso (ejemplos de endpoints)
- Testing
- Docker
- Tecnologías utilizadas
- Estructura del proyecto

---

### Paso 7.2: Documentar Código

**Tarea:** Agrega docstrings en español a:
- Todas las clases
- Todos los métodos públicos
- Funciones importantes
- Módulos principales

**IMPORTANTE:** La documentación es OBLIGATORIA y será evaluada. Sin documentación, se aplicará penalización.

#### Formato de Docstrings (Google Style)

**Para Clases:**
```python
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    
    Esta clase encapsula la lógica de negocio relacionada con productos,
    incluyendo validaciones de precio, stock y disponibilidad.
    
    Attributes:
        id (Optional[int]): Identificador único del producto
        name (str): Nombre del producto
        price (float): Precio en dólares, debe ser mayor a 0
        stock (int): Cantidad disponible en inventario
    """
```

**Para Métodos:**
```python
def reduce_stock(self, quantity: int) -> None:
    """
    Reduce el stock del producto en la cantidad especificada.
    
    Este método valida que haya suficiente stock antes de reducir.
    Se usa típicamente cuando se realiza una venta.
    
    Args:
        quantity (int): Cantidad a reducir del stock. Debe ser positivo.
    
    Raises:
        ValueError: Si quantity es negativo o mayor al stock disponible.
    
    Example:
        >>> product = Product(name="Zapato", stock=10, price=100)
        >>> product.reduce_stock(3)
        >>> print(product.stock)
        7
    """
```

**Para Funciones:**
```python
def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas.
    
    Esta función crea las tablas definidas en los modelos ORM
    y carga los datos iniciales si la base de datos está vacía.
    
    Returns:
        None
    
    Note:
        Esta función debe ejecutarse antes de iniciar la aplicación.
    """
```

**Para Endpoints de FastAPI:**
```python
@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de productos disponibles.
    
    Este endpoint retorna todos los productos registrados en la base de datos,
    incluyendo aquellos sin stock.
    
    Args:
        db (Session): Sesión de base de datos inyectada por FastAPI.
    
    Returns:
        List[ProductDTO]: Lista de productos con toda su información.
    
    Example:
        GET /products
        Response: [
            {
                "id": 1,
                "name": "Nike Air Zoom",
                "price": 120.0,
                "stock": 5
            }
        ]
    """
```

**Para Servicios:**
```python
class ChatService:
    """
    Servicio de aplicación para gestionar el chat con IA.
    
    Este servicio orquesta la interacción entre el repositorio de productos,
    el repositorio de chat y el servicio de IA de Gemini para proporcionar
    respuestas contextuales a los usuarios.
    
    Attributes:
        product_repo (IProductRepository): Repositorio de productos
        chat_repo (IChatRepository): Repositorio de mensajes de chat
        ai_service (GeminiService): Servicio de IA de Google Gemini
    """
    
    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con IA.
        
        Este método realiza el flujo completo:
        1. Obtiene productos disponibles
        2. Recupera historial de conversación
        3. Genera respuesta con IA usando contexto
        4. Guarda mensaje del usuario y respuesta
        5. Retorna la respuesta
        
        Args:
            request (ChatMessageRequestDTO): Mensaje del usuario con session_id.
        
        Returns:
            ChatMessageResponseDTO: Respuesta generada por la IA con timestamp.
        
        Raises:
            ChatServiceError: Si hay un error al procesar el mensaje o
                            comunicarse con el servicio de IA.
        
        Example:
            >>> request = ChatMessageRequestDTO(
            ...     session_id="user123",
            ...     message="Busco zapatos Nike"
            ... )
            >>> response = await chat_service.process_message(request)
            >>> print(response.assistant_message)
            "Tengo varios modelos Nike disponibles..."
        """
```

#### Checklist de Documentación

- [ ] Todas las clases del dominio documentadas
- [ ] Todas las interfaces documentadas
- [ ] Todos los servicios documentados
- [ ] Todos los repositorios documentados
- [ ] Todos los endpoints de FastAPI documentados
- [ ] Funciones de configuración documentadas
- [ ] Excepciones personalizadas documentadas
- [ ] DTOs documentados

**Checkpoint:** Ejecuta `pydoc` o revisa la documentación automática de FastAPI en `/docs` para verificar que toda la documentación sea visible y clara.

---

## CHECKLIST FINAL

### Funcionalidades Core
- [ ] Listar productos
- [ ] Buscar producto por ID
- [ ] Chat con IA funcionando
- [ ] Contexto conversacional (memoria)
- [ ] Historial de chat persistente
- [ ] Eliminar historial

### Arquitectura
- [ ] 3 capas bien definidas (Domain, Application, Infrastructure)
- [ ] Dependency Injection implementada
- [ ] Repository Pattern aplicado
- [ ] Service Layer implementado
- [ ] DTOs para transferencia de datos

### Calidad
- [ ] Validaciones en entidades
- [ ] Validaciones con Pydantic
- [ ] Manejo de excepciones
- [ ] Tests unitarios
- [ ] **Código completamente documentado con docstrings**
- [ ] Todas las clases tienen docstrings
- [ ] Todos los métodos públicos tienen docstrings
- [ ] Todos los endpoints tienen docstrings
- [ ] Docstrings en español con formato Google Style

### Infraestructura
- [ ] Base de datos SQLite funcionando
- [ ] 10 productos iniciales cargados
- [ ] FastAPI con todos los endpoints
- [ ] Documentación automática (/docs)
- [ ] Docker funcionando
- [ ] docker-compose configurado

### Integración IA
- [ ] Google Gemini integrado
- [ ] Prompt bien diseñado
- [ ] Contexto conversacional incluido
- [ ] Respuestas coherentes

---

## ENTREGABLES DEL TALLER

### 1. Repositorio de GitHub

**Requisitos:**
- Código fuente completo del proyecto
- Repositorio público o privado (compartido con el profesor)
- README.md con instrucciones de instalación y uso
- Archivo .gitignore configurado correctamente
- **Código completamente documentado con docstrings**
- Commits con mensajes descriptivos siguiendo convenciones

**Link del repositorio:** Debes subir el link en la plataforma de entrega

**IMPORTANTE:** Todo el código debe estar documentado con docstrings en español. Cada clase, método y función debe tener su documentación.

### 2. Evidencias Requeridas (Screenshots)

Debes incluir las siguientes capturas de pantalla en una carpeta `evidencias/` en tu repositorio:

#### a) Swagger UI de la API
- **Archivo:** `evidencias/01-swagger-ui.png`
- **Contenido:** Captura de pantalla de http://localhost:8000/docs mostrando todos los endpoints
- **Debe mostrar:** Fecha/hora del sistema operativo visible

#### b) Logs de Docker
- **Archivo:** `evidencias/02-docker-logs.png`
- **Contenido:** Terminal mostrando `docker-compose logs` o `docker logs`
- **Debe mostrar:** 
  - Logs de la aplicación corriendo
  - Nombre de usuario de tu PC visible en el prompt
  - Fecha/hora del sistema

#### c) Docker Desktop o Docker PS
- **Archivo:** `evidencias/03-docker-running.png`
- **Contenido:** Docker Desktop mostrando contenedores corriendo O salida de `docker ps`
- **Debe mostrar:** Contenedor de la aplicación activo

#### d) Llamado a la API desde Postman/Insomnia
- **Archivo:** `evidencias/04-api-call-products.png`
- **Contenido:** Request GET a `/products` con respuesta exitosa
- **Debe mostrar:** Lista de productos retornada

#### e) Llamado al Chat con IA
- **Archivo:** `evidencias/05-api-call-chat.png`
- **Contenido:** Request POST a `/chat` con respuesta del asistente
- **Debe mostrar:** Mensaje del usuario y respuesta de la IA

#### f) Base de Datos con Productos
- **Archivo:** `evidencias/06-database.png`
- **Contenido:** Visualización de la base de datos SQLite con productos cargados
- **Herramienta sugerida:** DB Browser for SQLite, VS Code SQLite Viewer

**IMPORTANTE:** Todas las capturas deben mostrar evidencia de que es tu computadora (nombre de usuario, fecha/hora del sistema, etc.)

### 3. Mejores Prácticas de Git

#### Estructura de Ramas

```bash
main (o master)
├── develop
│   ├── feature/setup-project
│   ├── feature/domain-layer
│   ├── feature/application-layer
│   ├── feature/infrastructure-layer
│   ├── feature/docker-setup
│   └── feature/tests
```

#### Convención de Commits (Conventional Commits)

Usa el siguiente formato para tus commits:

```
<tipo>: <descripción breve>

[cuerpo opcional]
```

**Tipos de commits:**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato, punto y coma faltante, etc (sin cambios de código)
- `refactor:` - Refactorización de código
- `test:` - Agregar o modificar tests
- `chore:` - Tareas de mantenimiento, actualizar dependencias

**Ejemplos de buenos commits:**

```bash
feat: add Product entity with validations
feat: implement ProductRepository with SQLAlchemy
feat: create FastAPI endpoints for products
feat: integrate Google Gemini AI for chat
fix: correct stock validation in Product entity
docs: update README with installation instructions
test: add unit tests for Product entity
chore: add requirements.txt with dependencies
refactor: improve error handling in ChatService
```

#### Flujo de Trabajo con Git (IMPORTANTE)

**REGLA DE ORO: NUNCA hacer commits directamente a la rama `main`**

Siempre trabaja en ramas de features y haz merge cuando esté completo y probado.

##### Paso a Paso: Cómo Trabajar con Ramas

**1. Configuración Inicial del Repositorio**

```bash
# Crear repositorio local
git init

# Crear archivo .gitignore primero
# (ya lo tienes del paso 1.3)

# Primer commit en main
git add .
git commit -m "chore: initial project structure"

# Crear y conectar con GitHub
git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main

# Crear rama develop (rama de desarrollo)
git checkout -b develop
git push -u origin develop
```

**2. Trabajar en una Nueva Funcionalidad (Feature)**

```bash
# SIEMPRE partir desde develop, NO desde main
git checkout develop

# Asegurarte de tener la última versión
git pull origin develop

# Crear rama para la nueva funcionalidad
# Nomenclatura: feature/nombre-descriptivo
git checkout -b feature/domain-layer

# Ahora estás en la rama feature/domain-layer
# Puedes verificarlo con:
git branch
# El asterisco (*) indica la rama actual
```

**3. Hacer Cambios y Commits en la Rama Feature**

```bash
# Trabajar en tus archivos...
# Por ejemplo, crear las entidades del dominio

# Ver qué archivos cambiaron
git status

# Agregar archivos específicos
git add src/domain/entities.py
git commit -m "feat: add Product entity with validations"

# Continuar trabajando...
git add src/domain/repositories.py
git commit -m "feat: add IProductRepository interface"

git add src/domain/exceptions.py
git commit -m "feat: add domain exceptions"

# Ver historial de commits
git log --oneline
```

**4. Subir la Rama Feature a GitHub**

```bash
# Primera vez que subes la rama
git push -u origin feature/domain-layer

# Siguientes veces (después de más commits)
git push
```

**5. Hacer Merge a Develop (Cuando la Feature Esté Completa)**

**Opción A: Merge Local (Más Rápido)**

```bash
# Cambiar a la rama develop
git checkout develop

# Asegurarte de tener la última versión
git pull origin develop

# Hacer merge de tu feature
git merge feature/domain-layer

# Si no hay conflictos, el merge se hace automáticamente
# Subir develop actualizado a GitHub
git push origin develop

# Opcional: Eliminar la rama feature localmente
git branch -d feature/domain-layer

# Opcional: Eliminar la rama feature en GitHub
git push origin --delete feature/domain-layer
```

**Opción B: Pull Request en GitHub (Recomendado para Trabajo en Equipo)**

```bash
# 1. Después de hacer push de tu feature
git push origin feature/domain-layer

# 2. Ir a GitHub en tu navegador
# 3. Verás un botón "Compare & pull request"
# 4. Crear Pull Request:
#    - Base: develop
#    - Compare: feature/domain-layer
#    - Título: "feat: implement domain layer"
#    - Descripción: Explicar qué cambios hiciste
# 5. Click en "Create pull request"
# 6. Revisar los cambios
# 7. Click en "Merge pull request"
# 8. Click en "Confirm merge"
# 9. Opcional: Eliminar la rama feature

# 10. Actualizar tu repositorio local
git checkout develop
git pull origin develop
```

**6. Ciclo Completo: Trabajar en Múltiples Features**

```bash
# Feature 1: Domain Layer
git checkout develop
git checkout -b feature/domain-layer
# ... trabajar, commits ...
git push origin feature/domain-layer
# ... merge a develop ...

# Feature 2: Application Layer
git checkout develop
git pull origin develop  # Importante: actualizar primero
git checkout -b feature/application-layer
# ... trabajar, commits ...
git push origin feature/application-layer
# ... merge a develop ...

# Feature 3: Infrastructure Layer
git checkout develop
git pull origin develop
git checkout -b feature/infrastructure-layer
# ... trabajar, commits ...
git push origin feature/infrastructure-layer
# ... merge a develop ...

# Y así sucesivamente...
```

**7. Merge Final a Main (Solo Cuando Todo Esté Completo y Probado)**

```bash
# Cuando TODAS las features estén completas y probadas en develop
git checkout develop
git pull origin develop

# Asegurarte de que todo funciona
# Ejecutar tests, probar la aplicación, etc.

# Cambiar a main
git checkout main
git pull origin main

# Hacer merge de develop a main
git merge develop

# Subir main actualizado
git push origin main

# Opcional: Crear un tag para la versión
git tag -a v1.0.0 -m "Primera versión completa del e-commerce"
git push origin v1.0.0
```

**8. Resolver Conflictos (Si Aparecen)**

```bash
# Si al hacer merge aparece un conflicto:
git merge feature/mi-feature
# Auto-merging src/domain/entities.py
# CONFLICT (content): Merge conflict in src/domain/entities.py

# 1. Abrir el archivo con conflicto
# Verás marcas como:
# <<<<<<< HEAD
# código de la rama actual
# =======
# código de la rama que estás mergeando
# >>>>>>> feature/mi-feature

# 2. Editar el archivo manualmente
# Decidir qué código mantener o combinar ambos

# 3. Eliminar las marcas de conflicto (<<<<, ====, >>>>)

# 4. Agregar el archivo resuelto
git add src/domain/entities.py

# 5. Completar el merge
git commit -m "merge: resolve conflicts in entities.py"

# 6. Subir los cambios
git push
```

**9. Comandos Útiles Durante el Desarrollo**

```bash
# Ver en qué rama estás
git branch

# Ver todas las ramas (locales y remotas)
git branch -a

# Cambiar de rama
git checkout nombre-rama

# Crear y cambiar a nueva rama en un solo comando
git checkout -b nueva-rama

# Ver diferencias antes de hacer commit
git diff

# Ver diferencias de un archivo específico
git diff src/domain/entities.py

# Ver estado de los archivos
git status

# Ver historial de commits
git log --oneline --graph --all

# Deshacer cambios no commiteados en un archivo
git checkout -- archivo.py

# Ver qué cambios tiene una rama respecto a otra
git diff develop..feature/mi-feature

# Actualizar tu rama feature con cambios de develop
git checkout feature/mi-feature
git merge develop
```

**10. Buenas Prácticas**

✅ **HACER:**
- Crear una rama nueva para cada feature
- Hacer commits pequeños y frecuentes
- Escribir mensajes de commit descriptivos
- Hacer pull de develop antes de crear nueva rama
- Probar tu código antes de hacer merge
- Eliminar ramas feature después de hacer merge

❌ **NO HACER:**
- Hacer commits directamente a main
- Crear ramas desde main (siempre desde develop)
- Hacer commits gigantes con muchos cambios
- Mensajes de commit vagos como "fix" o "update"
- Hacer merge sin probar el código
- Dejar ramas feature sin eliminar



#### Archivo .gitignore (Ya incluido en el taller)

Asegúrate de NO subir:
- `venv/` o `env/` - Entorno virtual
- `.env` - Variables de entorno con API keys
- `__pycache__/` - Archivos compilados de Python
- `*.pyc` - Bytecode de Python
- `data/*.db` - Base de datos local
- `.pytest_cache/` - Cache de pytest

#### Comandos Git Útiles

```bash
# Inicializar repositorio
git init
git add .
git commit -m "chore: initial commit"

# Conectar con GitHub
git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main

# Ver estado
git status

# Ver historial de commits
git log --oneline

# Crear y cambiar a nueva rama
git checkout -b feature/nombre-feature

# Ver ramas
git branch

# Cambiar de rama
git checkout nombre-rama

# Actualizar desde remoto
git pull origin main

# Ver diferencias
git diff

# Deshacer cambios no commiteados
git checkout -- archivo.py

# Ver commits de una rama
git log --graph --oneline --all
```

### 4. README.md del Proyecto

Tu README debe incluir:

```markdown
# E-commerce con Chat IA

## Descripción
API REST de e-commerce de zapatos con chat inteligente usando Clean Architecture.

## Tecnologías
- Python 3.11
- FastAPI
- SQLAlchemy
- Google Gemini AI
- Docker
- Pytest

## Instalación

### Requisitos Previos
- Python 3.10+
- Docker y Docker Compose
- API Key de Google Gemini

### Pasos

1. Clonar repositorio
\`\`\`bash
git clone <tu-repo>
cd e-commerce-chat-ai
\`\`\`

2. Crear entorno virtual
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows
\`\`\`

3. Instalar dependencias
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Configurar variables de entorno
\`\`\`bash
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
\`\`\`

5. Ejecutar con Docker
\`\`\`bash
docker-compose up --build
\`\`\`

## Uso

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Endpoints

- GET /products - Lista todos los productos
- GET /products/{id} - Obtiene un producto
- POST /chat - Envía mensaje al chat
- GET /chat/history/{session_id} - Obtiene historial

## Tests

\`\`\`bash
pytest
\`\`\`

## Autor
[Tu Nombre] - Universidad EAFIT
```

---

## Criterios de Evaluación

**Nota sobre 5.0**

Cada fase tiene el mismo peso en la calificación final:

### Distribución de Puntos (Cada fase vale 0.71 puntos)

1. **FASE 1: Configuración Inicial (0.71 pts)**
   - Estructura de directorios correcta
   - Dependencias instaladas
   - Variables de entorno configuradas

2. **FASE 2: Capa de Dominio (0.71 pts)**
   - Entidades con validaciones
   - Interfaces de repositorios
   - Excepciones del dominio

3. **FASE 3: Capa de Aplicación (0.71 pts)**
   - DTOs con validación Pydantic
   - ProductService implementado
   - ChatService implementado

4. **FASE 4: Capa de Infraestructura (0.71 pts)**
   - Base de datos configurada
   - Repositorios implementados
   - API con FastAPI funcionando
   - Integración con Gemini AI

5. **FASE 5: Docker (0.71 pts)**
   - Dockerfile correcto
   - docker-compose.yml funcional
   - Aplicación corriendo en contenedor

6. **FASE 6: Testing (0.71 pts)**
   - Tests unitarios para entidades
   - Tests para servicios
   - Coverage >60%

7. **FASE 7: Documentación y Entregables (1.03 pts)**
   - README completo (0.15 pts)
   - **Código completamente documentado con docstrings (0.35 pts)**
   - Repositorio en GitHub con commits apropiados (0.20 pts)
   - Todas las evidencias (screenshots) incluidas (0.23 pts)
   - Convenciones de Git seguidas (0.10 pts)

### Rúbrica Detallada

| Aspecto | Excelente (100%) | Bueno (80%) | Suficiente (60%) | Insuficiente (<60%) |
|---------|------------------|-------------|------------------|---------------------|
| **Arquitectura** | 3 capas perfectamente separadas | Capas separadas con pequeñas mezclas | Capas definidas pero con dependencias incorrectas | No respeta arquitectura en capas |
| **Funcionalidad** | Todas las funcionalidades + extras | Todas las funcionalidades core | Funcionalidades básicas | Funcionalidades incompletas |
| **Código** | Limpio, documentado, type hints | Bien estructurado, documentación básica | Funcional pero desorganizado | Difícil de entender |
| **Documentación** | Docstrings completos en español, ejemplos incluidos | Docstrings en todas las clases y métodos principales | Documentación parcial | Sin documentación |
| **Git** | Commits convencionales, ramas, PRs | Buenos commits, estructura básica | Commits descriptivos | Commits sin sentido |
| **Docker** | Funciona perfectamente, optimizado | Funciona correctamente | Funciona con ajustes | No funciona |
| **Evidencias** | Todas completas y claras | Todas presentes | Algunas faltantes | No incluidas |

---

## Consejos y Mejores Prácticas

### Arquitectura
1. **Respeta las capas**: Domain NO debe importar de Infrastructure
2. **Usa interfaces**: Define contratos en Domain, implementa en Infrastructure
3. **Dependency Injection**: Inyecta dependencias, no las crees internamente
4. **Single Responsibility**: Cada clase debe tener una sola responsabilidad

### Código
1. **Type hints**: Usa anotaciones de tipo en todo el código
2. **Docstrings**: Documenta clases y métodos públicos
3. **Validaciones**: Valida datos lo antes posible (Fail Fast)
4. **Excepciones**: Usa excepciones del dominio, no genéricas

### Base de Datos
1. **Sesiones**: Siempre cierra sesiones de BD
2. **Transacciones**: Usa commit() después de modificaciones
3. **Índices**: Agrega índices en columnas de búsqueda frecuente
4. **Migraciones**: En producción usa Alembic para migraciones

### IA
1. **Prompt Engineering**: El prompt es crucial para buenas respuestas
2. **Contexto**: Incluye historial para coherencia
3. **Límites**: Limita tokens para controlar costos
4. **Errores**: Maneja errores de API gracefully

### Docker
1. **.dockerignore**: No copies archivos innecesarios
2. **Volúmenes**: Usa volúmenes para datos persistentes
3. **Variables**: Usa .env para configuración
4. **Multi-stage**: En producción usa multi-stage builds

---

## Extensiones Opcionales (Bonus)

### Nivel Intermedio
- [ ] Paginación en listado de productos
- [ ] Filtros avanzados (rango de precios, múltiples categorías)
- [ ] Búsqueda por texto en productos
- [ ] Rate limiting en endpoints
- [ ] Logging estructurado

### Nivel Avanzado
- [ ] Autenticación con JWT
- [ ] Roles de usuario (admin, cliente)
- [ ] Carrito de compras
- [ ] Sistema de órdenes
- [ ] Integración con pasarela de pago
- [ ] Envío de emails
- [ ] Caché con Redis
- [ ] Métricas con Prometheus
- [ ] CI/CD con GitHub Actions

### Nivel Experto
- [ ] Microservicios (separar productos y chat)
- [ ] Event Sourcing
- [ ] CQRS Pattern
- [ ] GraphQL API
- [ ] WebSockets para chat en tiempo real
- [ ] Kubernetes deployment
- [ ] Observabilidad completa (logs, metrics, traces)

---

## Recursos Adicionales

### Documentación Oficial

#### FastAPI
- **Documentación principal**: https://fastapi.tiangolo.com/
- **Tutorial completo**: https://fastapi.tiangolo.com/tutorial/
- **Guía de usuario**: https://fastapi.tiangolo.com/tutorial/first-steps/
- **Dependency Injection**: https://fastapi.tiangolo.com/tutorial/dependencies/
- **Path Operations**: https://fastapi.tiangolo.com/tutorial/path-params/
- **Request Body**: https://fastapi.tiangolo.com/tutorial/body/
- **Response Model**: https://fastapi.tiangolo.com/tutorial/response-model/
- **Documentación automática**: https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs

#### Otras Tecnologías
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **Google Gemini**: https://ai.google.dev/docs
- **Docker**: https://docs.docker.com/
- **Pytest**: https://docs.pytest.org/

### Tutoriales Recomendados
- **Clean Architecture**: https://blog.cleancoder.com/
- **Repository Pattern**: https://martinfowler.com/eaaCatalog/repository.html
- **Dependency Injection**: https://python-dependency-injector.ets-labs.org/
- **FastAPI Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices

### Libros
- "Clean Architecture" - Robert C. Martin
- "Domain-Driven Design" - Eric Evans
- "Patterns of Enterprise Application Architecture" - Martin Fowler

---

## Soporte

Si tienes dudas durante el desarrollo:

1. **Revisa la documentación** de las librerías
2. **Consulta los ejemplos** en la documentación oficial
3. **Usa el debugger** para entender el flujo
4. **Lee los mensajes de error** completos
5. **Busca en Stack Overflow** problemas similares

---

## Resultado Esperado

Al finalizar este taller, tendrás:

- Una **API REST completa** con arquitectura limpia  
- **Chat inteligente** con memoria conversacional  
- **Integración con IA** de Google Gemini  
- **Base de datos** con productos y historial  
- **Containerización** con Docker  
- **Tests** unitarios  
- **Documentación** automática con FastAPI  
- Comprensión profunda de **Clean Architecture**  
- Experiencia con **patrones de diseño** profesionales  

---

**¡Éxito en tu desarrollo!**

**Recuerda:** La clave está en respetar las capas y mantener el código limpio y bien organizado. ¡Tómate tu tiempo y disfruta el proceso de aprendizaje!
