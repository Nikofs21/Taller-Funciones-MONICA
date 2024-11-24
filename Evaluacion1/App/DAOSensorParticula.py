
from .models import SensorParticula
from django.shortcuts import get_object_or_404
from DAOSensorParticulaImplement import SensorParticulaService
from django.db import models

class SensorParticulaDAO:
    
    @staticmethod
    def obtener_registro_por_particula_y_fecha(particula_id, fecha):
        
        #Recupera el registro de `SensorParticula` con el particula_id y la fecha especificados.
        
        return SensorParticula.objects.filter(particula_id=particula_id, fecha=fecha).first()
    
    def obtener_estado_particula_por_fecha(particula_id, fecha):
        """
        Obtiene el estado de calidad del aire para una partícula en una fecha específica.
        """
        try:
            particula_data = SensorParticula.objects.filter(particula_id=particula_id, fecha=fecha)
            if particula_data.exists():
                promedio = particula_data.aggregate(models.Avg('registros_validados'))['registros_validados__avg']
                return SensorParticulaService.obtener_estado_aire(promedio)  # Usa una función para determinar el estado según el valor promedio
            else:
                return "No hay datos"
        except Exception as e:
            print(f"Error al obtener datos para particula {particula_id} en {fecha}: {e}")
            return "No hay datos"
