import json
import logging
import requests
from scraper import MinisterioTrabajo, load_processed_ids, save_processed_ids
from email_utils import generate_email_template, send_email
from config import SMTP_SERVER, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_SUBJECT, LOGO_PATH, TOKEN_ENDPOINT, CLIENT_ID, CLIENT_SECRET

# Configuración del logger
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_keywords(filepath):
    """
    Carga el diccionario de palabras clave desde un archivo JSON.
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        logging.error("Error al cargar el archivo de palabras clave: %s", e)
        return {}

def get_access_token():
    """
    Solicita un token de acceso al endpoint configurado usando el flujo client_credentials.
    Se envía el scope 'api1' (ajústalo según las necesidades de la API).
    """
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "squidex-api"  # Utiliza el scope que sea apropiado, por ejemplo "api1" o "openid api1" squidex-api
    }
    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload, timeout=15)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")
        logging.info("Token obtenido exitosamente.")
        return access_token
    except Exception as e:
        logging.error("Error al solicitar el token: %s", e)
        return None

def main():
    try:
        logging.info("Inicio de la ejecucion del programa.")
        
        # Instanciar el scraper y obtener los empleos
        scraper = MinisterioTrabajo()
        empleos = scraper.scrape_jobs()
        
        # Cargar palabras clave desde el archivo JSON
        keywords = load_keywords("json/keywords.json")
        empleos_filtrados = scraper.filter_jobs_by_keywords(empleos, keywords)
        
        # Cargar los IDs de empleos ya procesados (se crea el archivo si no existe)
        processed_ids_filepath = "json/processed_jobs.json"
        processed_ids = load_processed_ids(processed_ids_filepath)
        
        # Filtrar solo los empleos que no han sido procesados previamente
        nuevos_empleos = [job for job in empleos_filtrados if job.get("id") not in processed_ids]
        
        if nuevos_empleos:
            # Actualizar el conjunto de IDs procesados
            nuevos_ids = {job.get("id") for job in nuevos_empleos}
            processed_ids.update(nuevos_ids)
            save_processed_ids(processed_ids_filepath, processed_ids)
            
            # Solicitar el token de acceso
            access_token = get_access_token()
            
            # Generar contenido HTML del correo con los nuevos empleos
            email_content = generate_email_template(nuevos_empleos, token=access_token)
            
            send_email(EMAIL_SUBJECT, email_content, SENDER_EMAIL, RECEIVER_EMAIL,
                                SMTP_SERVER, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, LOGO_PATH)
            logging.info("Correo enviado exitosamente con %d nuevos empleos.", len(nuevos_empleos))
        else:
            logging.info("No se encontraron nuevos empleos para enviar.")
        
        logging.info("Fin de la ejecucion del programa.\n--------------------------------------------------\n\n")
    except Exception as e:
        logging.error("Ocurrio un error durante la ejecucion: %s", e)

if __name__ == "__main__":
    main()
