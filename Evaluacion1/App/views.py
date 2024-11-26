from django.shortcuts import render
from datetime import datetime
from App import DAOComunaImplement
from App.DAOSensorParticulaImplement import SensorParticulaService
from App.DAOComuna import ComunaDAO
from App.DAOParticulas import ParticulasDAO
from App.DAOComunaImplement import ComunaServiceDAO
from django.db import connection


def IndexView(request):
    comunas_dto = ComunaDAO.obtener_todas_las_comunas()
    comunas = [{'id': comuna.id_comuna, 'nombre': comuna.nombre_comuna} for comuna in comunas_dto]
    return render(request, 'index.html', {'comunas': comunas})


def mostrar_niveles(request):
    """
    Vista que muestra los niveles de calidad del aire y el mensaje general.
    """
    comuna_id = request.GET.get('comuna_id')
    if not comuna_id:
        return render(request, 'error.html', {'mensaje': 'Comuna no especificada.'})

    try:
        comuna_id = int(comuna_id)
    except ValueError:
        return render(request, 'error.html', {'mensaje': 'ID de comuna no válido.'})

    # Obtener la comuna a través del DAO
    comuna = ComunaDAO.obtener_comuna_por_id(comuna_id)
    if not comuna:
        return render(request, 'error.html', {'mensaje': 'Comuna no encontrada.'})

    # Obtener la fecha de la consulta
    fecha = request.GET.get('fecha')
    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d")

    # Obtener las partículas a través del DAO y calcular niveles
    particulas_dto = ParticulasDAO.obtener_todas_las_particulas()
    particulas = {}
    for particula in particulas_dto:
        try:
            # Obtener el estado del aire usando el servicio
            estado = SensorParticulaService.obtener_estado_aire(comuna_id, particula.id_particula, fecha)
            particulas[particula.nombre_particula] = {
                'estado': estado,
                'descripcion': particula.descripcion,
            }
        except SensorParticulaService.SensorParticulaNoEncontrada:
            particulas[particula.nombre_particula] = {
                'estado': 'Sin datos',
                'descripcion': particula.descripcion,
            }

    # Obtener el mensaje de calidad del aire para la fecha y comuna
    mensaje_calidad_aire = obtener_mensaje_calidad_aire(fecha, comuna_id)

    # Renderizar la plantilla con los datos
    return render(request, 'semaforos.html', {
        'comuna': comuna,
        'air_quality_data': particulas,
        'fecha': fecha,
        'mensaje_calidad_aire': mensaje_calidad_aire,
    })


def obtener_mensaje_calidad_aire(fecha, comuna_id):
    """
    Llama al procedimiento almacenado para obtener el mensaje de calidad del aire para una comuna específica.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            DECLARE @Resultado NVARCHAR(MAX);
            EXEC sp_CalcularCalidadAire @Fecha = %s, @ComunaID = %s, @Resultado = @Resultado OUTPUT;
            SELECT @Resultado;
        """, [fecha, comuna_id])
        resultado = cursor.fetchone()
    return resultado[0] if resultado else "Sin datos disponibles"

def login_view(request):
    return render(request, 'login.html')