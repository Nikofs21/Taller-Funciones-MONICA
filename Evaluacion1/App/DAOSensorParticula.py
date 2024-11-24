from App.models import SensorParticula
from django.db.models import Avg
from App.models import ComunaSensor


class SensorParticulaDAO:
    @staticmethod
    def obtener_registro_por_particula_y_fecha(particula_id, fecha):
        """
        Recupera el registro de `SensorParticula` con el particula_id y la fecha especificados.
        """
        return SensorParticula.objects.filter(particula_id=particula_id, fecha=fecha).first()

    @staticmethod
    def obtener_promedio_por_particula_y_fecha(particula_id, comuna_id, fecha):
        """
        Calcula el promedio de registros validados para una partícula específica en una comuna y fecha.
        Incluye un filtro para asegurarse de que los registros correspondan a la comuna seleccionada.
        """
        # Filtrar sensores asociados a la comuna
        sensores_comuna = ComunaSensor.objects.filter(comuna_id=comuna_id).values_list('sensor_id', flat=True)
        
        # Filtrar registros de los sensores de esa comuna
        registros = SensorParticula.objects.filter(
            particula_id=particula_id,
            sensor_id__in=sensores_comuna,
            fecha=fecha
        )
        
        # Calcular promedio validado
        promedio_validado = registros.aggregate(promedio=Avg('registros_validados'))['promedio']
        
        if promedio_validado is not None and promedio_validado > 0:
            return promedio_validado
        
        # Calcular promedio preliminar si no hay validados
        promedio_preliminar = registros.aggregate(promedio=Avg('registros_preliminares'))['promedio']
        
        if promedio_preliminar is not None and promedio_preliminar > 0:
            return promedio_preliminar
        
        # Si no hay datos
        return None