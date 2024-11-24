from django.shortcuts import render
from datetime import datetime
from App import DAOComunaImplement
from App.DAOSensorParticulaImplement import SensorParticulaService
from App.DAOComuna import ComunaDAO
from App.DAOParticulas import ParticulasDAO
from App.DAOComunaImplement import ComunaServiceDAO


def IndexView(request):
    comunas_dto = ComunaDAO.obtener_todas_las_comunas()
    comunas = [{'id': comuna.id_comuna, 'nombre': comuna.nombre_comuna} for comuna in comunas_dto]
    return render(request, 'index.html', {'comunas': comunas})


def mostrar_niveles(request):
    """
    Vista que muestra los niveles de calidad del aire para una comuna seleccionada y una fecha específica.
    """
    # Obtener comuna seleccionada
    comuna_id = request.GET.get('comuna_id')
    if not comuna_id:
        return render(request, 'error.html', {'mensaje': 'Comuna no especificada.'})

    try:
        comuna_id = int(comuna_id)
    except ValueError:
        return render(request, 'error.html', {'mensaje': 'ID de comuna no válido.'})

    # Obtener datos de la comuna
    comuna = ComunaDAO.obtener_comuna_por_id(comuna_id)
    if not comuna:
        return render(request, 'error.html', {'mensaje': 'Comuna no encontrada.'})

    # Obtener fecha seleccionada o usar la fecha actual
    fecha = request.GET.get('fecha')
    if fecha:
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return render(request, 'error.html', {'mensaje': 'Fecha no válida.'})
    else:
        fecha = datetime.now().strftime("%Y-%m-%d")

    # Obtener datos de partículas y calcular sus niveles
    particulas_dto = ParticulasDAO.obtener_todas_las_particulas()
    particulas = {}
    for particula in particulas_dto:
        try:
            # Obtener estado del aire para la comuna y la partícula seleccionada
            estado = SensorParticulaService.obtener_estado_aire(comuna_id, particula.id_particula, fecha)
            particulas[particula.nombre_particula] = {'estado': estado, 'descripcion': particula.descripcion}
        except SensorParticulaService.SensorParticulaNoEncontrada:
            particulas[particula.nombre_particula] = {'estado': 'Sin datos', 'descripcion': particula.descripcion}

    # Renderizar la página con los datos
    return render(request, 'semaforos.html', {
        'comuna': comuna,
        'air_quality_data': particulas,
        'fecha': fecha,
    })