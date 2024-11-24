from django.shortcuts import get_object_or_404
from App.models import Particula
from App import DTOParticulas
from App.DTOParticulas import ParticulaDTO
from App.models import Particula

class ParticulasDAO:
    @staticmethod
    def obtener_todas_las_particulas():
        """
        Recupera todas las partículas de la base de datos.
        """
        particulas = Particula.objects.all()
        return [ParticulaDTO(particula.id_particula, particula.nombre_particula, particula.descripcion) for particula in particulas]
    
    
    @staticmethod
    def obtener_particula_por_id(id_particula):
        particula = get_object_or_404(Particula, id_particula=id_particula)
        return DTOParticulas.ParticulaDTO(particula.id_particula,particula.nombre_particula,particula.descripcion)