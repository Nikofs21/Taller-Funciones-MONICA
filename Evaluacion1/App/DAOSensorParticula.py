from App.models import SensorParticula
from django.db.models import Avg


class SensorParticulaDAO:
    @staticmethod
    def obtener_registro_por_particula_y_fecha(particula_id, fecha):
        """
        Recupera el registro de `SensorParticula` con el particula_id y la fecha especificados.
        """
        return SensorParticula.objects.filter(particula_id=particula_id, fecha=fecha).first()

    @staticmethod
    def obtener_promedio_por_particula_y_fecha(particula_id, fecha):
        """
        Calcula el promedio de registros validados para una partícula en una fecha específica.
        """
        registros = SensorParticula.objects.filter(particula_id=particula_id, fecha=fecha)
        return registros.aggregate(promedio=Avg('registros_validados'))['promedio']