import requests
from datetime import datetime
import unicodedata
import json
import os
from config import ALLOWED_PROVINCIAS

def normalize_text(text):
    """
    Convierte el texto a minúsculas y elimina acentos.
    """
    if not isinstance(text, str):
        return ""
    normalized = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return normalized.lower()

class MinisterioTrabajo:
    BASE_URL = "https://empleateya.mt.gob.do"
    
    def __init__(self):
        self.conceptos_url = f"{self.BASE_URL}/api/conceptos"
        self.regiones_url = f"{self.BASE_URL}/api/conceptos/regionesFlat"
        self.salary_map = self.get_salary_map()
        self.region_map = self.get_region_map()
    
    def get_salary_map(self):
        try:
            response = requests.get(self.conceptos_url)
            response.raise_for_status()
            data = response.json()
            conceptos = data.get("conceptos", {})
            salario = conceptos.get("salario", [])
            salary_mapping = {}
            for item in salario:
                codigo = item.get("codigo")
                descripcion = item.get("descripcion")
                if codigo is not None:
                    if descripcion is None:
                        descripcion = "Rango no especificado"
                    salary_mapping[codigo] = descripcion
            return salary_mapping
        except Exception as e:
            print("Error al obtener conceptos de salario:", e)
            return {}
    
    def get_region_map(self):
        try:
            response = requests.get(self.regiones_url)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print("Error al obtener regiones:", e)
            return {}
    
    def scrape_jobs(self):
        """
        Recorre las páginas de puestos, filtra por fecha y provincia, 
        formatea la fecha a "27 Agosto 2025" y agrega el campo 'id' para cada empleo.
        """
        all_jobs = []
        page_index = 1
        page_size = 6
        
        allowed_provincias = ALLOWED_PROVINCIAS
        current_date = datetime.now()
        
        # Diccionario para traducir el número de mes a su nombre en español.
        meses_es = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }
        
        while True:
            url = f"{self.BASE_URL}/api/puestos?filters=%7B%7D&pageIndex={page_index}&pageSize={page_size}"
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                print(f"Error al obtener la página {page_index}:", e)
                break
            
            if "data" not in data or not data["data"]:
                break
            
            for item in data["data"]:
                puesto = item.get("puesto", {})
                job_id = puesto.get("id")
                if job_id is None:
                    continue
                
                fecha_vencimiento_str = puesto.get("fechaVencimiento")
                if not fecha_vencimiento_str:
                    continue
                try:
                    fecha_vencimiento = datetime.fromisoformat(fecha_vencimiento_str)
                except Exception as e:
                    print("Error parseando fecha:", e)
                    continue
                if fecha_vencimiento <= current_date:
                    continue
                
                # Formatear la fecha a "27 Agosto 2025"
                fecha_formateada = f"{fecha_vencimiento.day} {meses_es.get(fecha_vencimiento.month, '')} {fecha_vencimiento.year}"
                
                id_provincia = puesto.get("idProvincia")
                if id_provincia not in allowed_provincias:
                    continue
                
                salario_code = puesto.get("salarioOfrecido")
                salario_text = self.salary_map.get(salario_code, "No especificado")
                provincia_descripcion = self.region_map.get(str(id_provincia), "Desconocida")
                
                job_info = {
                    "id": job_id,
                    "titulo": puesto.get("titulo", "No especificado"),
                    "descripcion": puesto.get("descripcion", "No especificado"),
                    "beneficiosGenerales": puesto.get("beneficiosGenerales", "No especificado"),
                    "requisitosGenerales": puesto.get("requisitosGenerales", "No especificado"),
                    "salario": salario_text,
                    "cantidad": f"{puesto.get('cantidad')} {' Plaza disponible' if puesto.get('cantidad') == 1 else ' Plazas disponibles'}",
                    "fechaVencimiento": fecha_formateada,
                    "provincia": provincia_descripcion,
                }
                
                all_jobs.append(job_info)
            
            page_index += 1
        
        return all_jobs
    
    def filter_jobs_by_keywords(self, jobs, keywords_dict):
        """
        Filtra una lista de empleos por palabras clave (normalizando textos y palabras clave).
        """
        all_keywords = []
        for category, words in keywords_dict.items():
            for word in words:
                all_keywords.append(normalize_text(word))
        filtered_jobs = []
        for job in jobs:
            titulo = normalize_text(job.get("titulo", ""))
            descripcion = normalize_text(job.get("descripcion", ""))
            texto_completo = f"{titulo} {descripcion}"
            for keyword in all_keywords:
                if keyword in texto_completo:
                    filtered_jobs.append(job)
                    break
        return filtered_jobs

def load_processed_ids(filepath):
    """
    Carga los IDs procesados desde un archivo JSON. Si no existe, retorna un conjunto vacío.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                content = f.read().strip()
                if not content:  # Si el contenido está vacío, se retorna un conjunto vacío.
                    return set()
                data = json.loads(content)
                return set(data)
        except Exception as e:
            print("Error al cargar el archivo de IDs procesados:", e)
            return set()
    return set()

def save_processed_ids(filepath, processed_ids):
    """
    Guarda los IDs procesados en un archivo JSON.
    """
    try:
        with open(filepath, "w") as f:
            json.dump(list(processed_ids), f)
    except Exception as e:
        print("Error al guardar el archivo de IDs procesados:", e)
