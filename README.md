<!-- Imagen de cabecera (puedes alojarla en tu repo, en la carpeta assets o donde prefieras) -->
![Encabezado](ruta_a_tu_imagen_de_cabecera.png)

# FindMT :mag: Aplicación de Empleos – Scraper y Envío de Notificaciones

<span style="color:#2E86C1"><strong>FindMT</strong></span> es una aplicación que te ayuda a localizar oportunidades de trabajo de forma automatizada, filtrarlas y recibir notificaciones por correo electrónico. A continuación, te presentamos sus principales funcionalidades:

## :sparkles: Funcionalidades Principales

- :dart: **Scrapeo de Empleos:** Consulta la API de [MinisterioTrabajo](https://empleateya.mt.gob.do) para extraer puestos de trabajo.
- :heavy_check_mark: **Filtrado y Deduplificación:** Utiliza palabras clave (definidas en `keywords.json`) y evita empleos duplicados mediante un registro en un archivo `processed_jobs.json`.
- :email: **Envío de Correos:** Genera y envía un correo HTML con la información de cada puesto y un botón "Aplicar".
- :cyclone: **Endpoint Intermedio (Proxy):** Implementa un pequeño servidor en Flask que obtiene el token de acceso mediante *client_credentials*, lo inyecta en una cookie y redirige a la página de detalle del puesto.

---

## :clipboard: Características

1. <span style="color:green">**Configuración a través de `.env`**</span>  
   Toda la configuración (datos SMTP, credenciales, endpoints, etc.) se carga desde un archivo `.env`.

2. <span style="color:green">**Modularidad**</span>  
   - `config.py`: Carga y expone variables de entorno.  
   - `scraper.py`: Clase `MinisterioTrabajo` para extraer y filtrar empleos, y funciones para manejo de IDs procesados.  
   - `email_utils.py`: Generación de la plantilla HTML y función de envío.  
   - `main.py`: Orquesta el flujo principal (scrapeo, filtrado, actualización de IDs y envío de correo).

3. <span style="color:green">**Registro (Logging)**</span>  
   Se crea un archivo `app.log` con la bitácora de la ejecución, errores y detalles del envío.

---

## :file_folder: Estructura del Proyecto

```bash
mi_proyecto/
├── .env                  # Variables de entorno (SMTP, credenciales, endpoints, etc.)
├── config.py             # Carga las variables de entorno y las expone
├── scraper.py            # Consulta la API de empleos y filtra resultados
├── email_utils.py        # Genera la plantilla HTML y envía el correo
├── main.py               # Flujo principal de scraping y envío de correos
├── app.py                # Endpoint Flask que obtiene el token y redirige al usuario
├── json/
│   ├── keywords.json     # Palabras clave para filtrar
│   └── processed_jobs.json # Almacena los IDs de empleos ya procesados
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo
```
---
## :hammer_and_wrench: Requisitos

- <span style="color:#2E86C1;">**Python 3.7+**</span>  
- **Dependencias** listadas en [requirements.txt](requirements.txt)

## :rocket: Instalación
```bash
# Clonar el repositorio y configurar
   git clone https://tu-repositorio.git
   cd mi_proyecto
   
# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt

# Configuración
Crea un archivo .env en el directorio raíz con las siguientes variables (ajusta los valores según tu entorno):
# Configuración SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587<br>
SMTP_LOGIN=tu_correo@gmail.com
SMTP_PASSWORD=tu_contraseña<br>
SENDER_EMAIL=tu_correo@gmail.com
RECEIVER_EMAIL=destinatario@gmail.com
EMAIL_SUBJECT=Oportunidades de Empleo - Nuevas Vacantes
LOGO_PATH=logo.png

# Configuración para la obtención del token (OpenID Connect)
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
TOKEN_ENDPOINT=https://empleateya.mt.gob.do/idp/connect/token<br>

# Configuración de provincias permitidas (IDs separados por comas)
ALLOWED_PROVINCIAS=41,190,42
listado de provincias en: "json/listado_regiones.json"

# Archivo de Palabras Clave
Crea el archivo json/keywords.json con la estructura de palabras clave. Ejemplo:

{
     "posiciones": [
       "gerente de tienda",
       "encargada de poligono",
       "encargada administrativa"
     ],
     "instituciones": [
       "franquicias del mundo",
       "oficina nacional de estadistica",
       "mercantil c",
       "enae business school",
       "universidad del caribe"
     ],
}
