from celery import shared_task
import requests
from .models import Country
from django.db import transaction
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
MAX_TIMEZONE_LENGTH = 255 
@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def fetch_countries_data(self):
    print("Fetching countries data...")
    url = 'https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng'
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries_data = response.json()

        with transaction.atomic():
            for country_data in countries_data:
                name_common = country_data['name']['common']
                name_official = country_data['name']['official']
                
                native_name = country_data['name'].get('nativeName', {})
                native_name_common = native_name.get('eng', {}).get('common', None)
                native_name_official = native_name.get('eng', {}).get('official', None)

                flags_png = country_data['flags']['png']
                flags_svg = country_data['flags']['svg']
                flags_alt = country_data['flags'].get('alt', None)
                
                capital = country_data['capital'][0] if 'capital' in country_data and country_data['capital'] else None
                latitude, longitude = country_data['latlng'] if 'latlng' in country_data and len(country_data['latlng']) == 2 else (None, None)
                
                area = country_data['area']
                population = country_data['population']
                timezone = ','.join(country_data['timezones'])[:MAX_TIMEZONE_LENGTH]
                continent = ','.join(country_data['continents'])

                # Evitar duplicados por el nombre común
                Country.objects.update_or_create(
                    name_common=name_common,
                    defaults={
                        'name_official': name_official,
                        'native_name_common': native_name_common,
                        'native_name_official': native_name_official,
                        'flags_png': flags_png,
                        'flags_svg': flags_svg,
                        'flags_alt': flags_alt,
                        'capital': capital,
                        'latitude': latitude,
                        'longitude': longitude,
                        'area': area,
                        'population': population,
                        'timezone': timezone,
                        'continent': continent
                    }
                )

    except requests.RequestException as e:
        logger.error(f"Error al obtener los datos: {e}")
        raise self.retry(exc=e)  # Reintentar en caso de error de solicitud
    except Exception as e:
        logger.error(f"Error durante el procesamiento de datos: {e}")
        raise self.retry(exc=e)  # Reintentar en caso de otros errores
