# FindMT Aplicación de Empleos – Scraper y Envío de Notificaciones

Esta aplicación realiza lo siguiente:

- **Scrapeo de Empleos:** Consulta la API de [MinisterioTrabajo](https://empleateya.mt.gob.do) para extraer puestos de trabajo.
- **Filtrado y Deduplificación:** Filtra los empleos según palabras clave configuradas y evita enviar empleos duplicados mediante un registro en un archivo JSON.
- **Envío de Correos:** Genera y envía un correo electrónico con una plantilla HTML (compatible con Outlook y otros clientes) que incluye la información de cada empleo y un botón "Aplicar".
- **Endpoint Intermedio (Proxy):** Proporciona un endpoint intermedio (desarrollado con Flask) que obtiene un token de acceso mediante el flujo *client_credentials*, lo inyecta en una cookie y redirige al usuario primero al dashboard y luego a la página de detalle del puesto.

## Características

- **Configuración a través de .env:** Toda la configuración (datos SMTP, credenciales, endpoints, etc.) se carga desde un archivo `.env`.
- **Modularidad:** La aplicación está dividida en módulos:
  - **config.py:** Carga y expone las variables de entorno.
  - **scraper.py:** Contiene la clase `MinisterioTrabajo` para extraer y filtrar empleos, y funciones para el manejo de IDs procesados.
  - **email_utils.py:** Genera la plantilla HTML del correo y define la función para el envío.
  - **main.py:** Orquesta el flujo: scrapeo, filtrado, actualización de IDs, generación del correo y envío.
- **Registro (Logging):** Se genera un archivo de log (`app.log`) con información de la ejecución, errores y detalles del envío.

## Estructura del Proyecto
mi_proyecto/ <br>├── .env # Variables de entorno (configuración SMTP, credenciales, endpoints, etc.) <br>├── config.py # Carga las variables de entorno y las expone a la aplicación. <br>├── scraper.py # Lógica para consultar la API de empleos y filtrar resultados. <br>├── email_utils.py # Funciones para generar la plantilla HTML y enviar el correo. <br>├── main.py # Punto de entrada para ejecutar el proceso de scraping y envío de correos. <br>├── app.py # Endpoint intermedio (Flask) que obtiene el token y redirige al usuario. <br>├── json/ │ <br>├── keywords.json # Archivo JSON con las palabras clave de filtrado. │ <br>└── processed_jobs.json # Archivo JSON que almacena los IDs de empleos ya procesados. <br>├── requirements.txt # Lista de dependencias del proyecto. <br>└── README.md # Este archivo.


## Requisitos

- **Python 3.7+**
- Dependencias listadas en [requirements.txt](requirements.txt)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://tu-repositorio.git
   cd mi_proyecto
   
2. **Crear y activar un entorno virtual (opcional pero recomendado):**
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

3. **Instalar las dependencias:**
pip install -r requirements.txt

4. **Configuración**
Crea un archivo .env en el directorio raíz con las siguientes variables (ajusta los valores según tu entorno):
# Configuración SMTP
SMTP_SERVER=smtp.gmail.com<br>
SMTP_PORT=587<br>
SMTP_LOGIN=tu_correo@gmail.com<br>
SMTP_PASSWORD=tu_contraseña<br>
SENDER_EMAIL=tu_correo@gmail.com<br>
RECEIVER_EMAIL=destinatario@gmail.com<br>
EMAIL_SUBJECT=Oportunidades de Empleo - Nuevas Vacantes<br>
LOGO_PATH=logo.png

# Configuración para la obtención del token (OpenID Connect)
CLIENT_ID=tu_client_id<br>
CLIENT_SECRET=tu_client_secret<br>
TOKEN_ENDPOINT=https://empleateya.mt.gob.do/idp/connect/token<br>

# Configuración de provincias permitidas (IDs separados por comas)
ALLOWED_PROVINCIAS=41,190,42<br>
listado de provincias en -> json/listado_regiones.json

5. **Archivo de Palabras Clave**
Crea el archivo json/keywords.json con la estructura de palabras clave. Ejemplo:

{<br>
     "posiciones": [<br>
       "gerente de tienda",<br>
       "encargada de poligono",<br>
       "encargada administrativa"<br>
     ],<br>
     "instituciones": [<br>
       "franquicias del mundo",<br>
       "oficina nacional de estadistica",<br>
       "mercantil c",<br>
       "enae business school",<br>
       "universidad del caribe"<br>
     ],<br>
}
