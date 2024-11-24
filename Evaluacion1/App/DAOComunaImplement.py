
from App import DAOComuna
from App.DTOComuna import ComunaDTO
from App.models import Comuna

class ComunaServiceDAO:
    
    @staticmethod
    def listar_comunas():
        return DAOComuna.ComunaDAO.obtener_todas_las_comunas()

    @staticmethod
    def obtener_comuna(comuna_id):
        """
        Recupera una comuna por su ID.
        """
        try:
            comuna = Comuna.objects.get(id_comuna=comuna_id)
            return ComunaDTO(comuna.id_comuna, comuna.nombre_comuna)
        except Comuna.DoesNotExist:
            return None
