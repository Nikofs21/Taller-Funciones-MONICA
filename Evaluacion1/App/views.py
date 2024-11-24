from django.shortcuts import render
from datetime import datetime
from App import DAOComunaImplement
from App.DAOSensorParticulaImplement import SensorParticulaService
from App.DAOComuna import ComunaDAO
from App.DAOParticulas import ParticulasDAO
from App.DAOComunaImplement import ComunaServiceDAO



def IndexView(request):
    
    comunas=ComunaDAO.obtener_todas_las_comunas()
    comunas_dto = ComunaDAO.obtener_todas_las_comunas()
    comunas = [{'id': comuna.id_comuna, 'nombre': comuna.nombre_comuna} for comuna in comunas_dto]

    return render(request, 'index.html', {'comunas': comunas})



def mostrar_niveles(request):
    # Obtener el ID de la comuna desde los parámetros de la solicitud
    comuna_id = request.GET.get('comuna_id')
    if not comuna_id:
        return render(request, 'error.html', {'mensaje': 'Comuna no especificada.'})

    # Convertir comuna_id a entero
    try:
        comuna_id = int(comuna_id)
    except ValueError:
        return render(request, 'error.html', {'mensaje': 'ID de comuna no válido.'})

    # Obtener la comuna utilizando el DAO correspondiente
    comuna = ComunaServiceDAO.obtener_comuna(comuna_id)
    if not comuna:
        return render(request, 'error.html', {'mensaje': 'Comuna no encontrada.'})

    # Obtener la fecha desde los parámetros de la solicitud
    fecha = request.GET.get('fecha')
    if fecha:
        try:
            # Convertir fecha a `datetime` y luego formatear a `YYYY-MM-DD`
            fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return render(request, 'error.html', {'mensaje': 'Fecha no válida.'})
    else:
        # Usar la fecha actual si no se proporciona en los parámetros
        fecha = datetime.now().strftime("%Y-%m-%d")

    # Obtener todas las partículas utilizando el DAO correspondiente
    particulas_dto = ParticulasDAO.obtener_todas_las_particulas()
    if not particulas_dto:
        return render(request, 'error.html', {'mensaje': 'No se encontraron partículas.'})

    # Crear un diccionario para almacenar los datos de las partículas
    particulas = {}
    for particula in particulas_dto:
        particula_id = particula.id_particula
        nombre_particula = particula.nombre_particula
        descripcion = particula.descripcion

        # Obtener el estado del aire para la partícula y la comuna en la fecha especificada
        try:
            estado_aire = SensorParticulaService.obtener_estado_aire(comuna_id, particula_id, fecha)
            particulas[nombre_particula] = {'estado': estado_aire, 'descripcion': descripcion}
        except SensorParticulaService.SensorParticulaNoEncontrada:
            particulas[nombre_particula] = {'estado': 'No hay datos', 'descripcion': descripcion}

    # Renderizar la plantilla con los datos obtenidos
    return render(request, 'semaforos.html', {'comuna': comuna, 'air_quality_data': particulas})