# RodelSoft Domain Template

## Propósito

Este proyecto es la plantilla base para la creación de nuevos Platform Domains dentro de RodelSoft Platform.

Un Domain representa un servicio privado de plataforma con:

- API propia.
- Base de datos propia.
- Seguridad integrada con Control Plane.
- Framework de Governance integrado.
- Capacidad de extender servicios mediante providers y capabilities.

Este template es la base para dominios como:

- rs-dom-fiscal
- rs-dom-payment
- futuros dominios de plataforma.

---

# Arquitectura base

Un Domain funciona como un componente privado de plataforma.

Flujo general:

Portal
 |
 | JWT + contexto
 |
 v
Domain
 |
 | validación segura
 |
 v
Control Plane
 |
 | autorización de comunicación
 |
 v
Base de datos del Domain


Los Domains no forman parte del catálogo público de aplicaciones para usuarios finales.

---

# Estructura del proyecto

domain-template/

├── app
│ ├── core
│ │ ├── db.py
│ │ └── security.py
│ │
│ ├── models
│ │ ├── system_provider.py
│ │ └── system_service.py
│ │
│ ├── routes
│ │ ├── health.py
│ │ ├── secure.py
│ │ └── system.py
│ │
│ ├── permissions.py
│ └── main.py
│
├── database
│ ├── baseline
│ └── migrations
│
├── framework
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── .env.example

---

# Componentes base

## FastAPI

Cada Domain utiliza FastAPI como runtime HTTP.

La aplicación se expone mediante:


/ext/<domain-name>


Ejemplo:


/ext/dom-fiscal


---

## Database

Cada Domain administra su propia base de datos.

Reglas:

- No consultar bases de otros componentes.
- No acceder directamente a Control Plane DB.
- Toda integración debe realizarse mediante contratos API.

---

# Governance Framework

Cada Domain incluye el RodelSoft Governance Framework.

Responsabilidades:

- Baseline.
- Migraciones.
- Deploy controlado.
- Registro de ejecución.

Estructura:


database/

├── baseline

└── migrations
└── REQ-XXXXX
├── schema
└── populate


Ejemplo:


database/migrations/REQ-10B4F-001/

schema/
001_table.sql

populate/
002_catalog.sql


---

# Configuración

Variables mínimas:


APP_PORT=

APP_BASE_PATH=/ext/domain-name

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

DOMAIN_APP_ID=

CONTROL_PLANE_URL=

FRAMEWORK_DIR=
POLICIES_DIR=


---

# Identidad del Domain

Cada Domain tiene una identidad única dentro de Control Plane.

La identidad corresponde a:


applications.id


La variable:


DOMAIN_APP_ID


debe coincidir con ese valor.

Ejemplo:


applications

id | name | component_type

9 | Fiscal Domain | DOMAIN


Configuración:


DOMAIN_APP_ID=9


---

# Registro del Domain en Control Plane

Todo Domain debe registrarse como:


component_type = DOMAIN


No utilizar:


component_type = APP


porque corresponde a aplicaciones con interacción directa de usuario.

---

# Seguridad

Los Domains utilizan comunicación segura con Control Plane.

Headers requeridos:


Authorization: Bearer <JWT>

X-App-Id

X-Client-Id


Validaciones:

1. JWT válido.
2. X-App-Id coincide con DOMAIN_APP_ID.
3. Application existe.
4. Application pertenece al tipo DOMAIN.
5. Client válido.
6. Comunicación permitida.

---

# Diferencia con aplicaciones tradicionales

Las aplicaciones:


component_type=APP


validan:

- usuario.
- permisos.
- membresías.
- suscripciones.

Los Domains:


component_type=DOMAIN


validan:

- identidad del componente.
- comunicación segura.

Un Domain no depende de permisos del usuario final.

---

# System Services

Todos los Domains incluyen el modelo base:


system_providers
|
|
system_services


Estas tablas representan capacidades disponibles del Domain.

Ejemplo:


Provider:

RodelSoft

Services:

fiscal_catalogs
sat_validation


Consulta:


GET /system/services


Respuesta:

```json
{
  "domain": "example",
  "providers": []
}
Extensión de un Domain

Cada nuevo dominio agrega sus propios componentes.

Ejemplo:

app/

├── models
├── routes
├── services

database/

└── migrations

El template ya proporciona:

seguridad;
conexión;
framework;
estructura base;
comunicación con plataforma.
Creación de un nuevo Domain

Proceso:

Copiar domain-template.
Cambiar nombre del proyecto.
Configurar variables de entorno.
Crear registro en applications.
Asignar:
component_type=DOMAIN
Configurar:
DOMAIN_APP_ID
Crear base de datos propia.
Crear migraciones iniciales.
Registrar providers/services propios.
Ejemplo de dominios
domain-template

        |
        +── rs-dom-fiscal

        |
        +── rs-dom-payment

Cada Domain mantiene independencia funcional, pero comparte la infraestructura base de plataforma.

Reglas de desarrollo
No crear sistemas paralelos de seguridad.
Reutilizar contratos existentes de plataforma.
No acceder directamente a bases externas.
Toda modificación estructural debe pasar por migrations.
Los cambios deben ser reproducibles mediante Framework.
Los datos iniciales dependientes de ambiente deben manejarse como populate.

Este README representa el estado real alcanzado con `rs-dom-fiscal` y ya sirve como contrato inicial para generar `domain-template`.