
from django.shortcuts import render
from datetime import datetime
from App import DAOComunaImplement
from App.DAOSensorParticulaImplement import SensorParticulaService
from App.DAOComuna import ComunaDAO
from App.DAOParticulas import ParticulasDAO



def IndexView(request):
    
    comunas=ComunaDAO.obtener_todas_las_comunas()
    comunas_dto = ComunaDAO.obtener_todas_las_comunas()
    comunas = [{'id': comuna.id_comuna, 'nombre': comuna.nombre_comuna} for comuna in comunas_dto]

    return render(request, 'index.html', {'comunas': comunas})



def mostrar_niveles(request):
    comuna_id = request.GET.get('comuna_id')
        # Convertir comuna_id a entero
    comuna_id = int(comuna_id)
    comuna = DAOComunaImplement.ComunaServiceDAO.obtener_comuna(comuna_id)
    
    fecha = request.GET.get('fecha')
    if fecha:
        try:
            # Convertir fecha a `datetime` y luego formatear a `yymmdd`
            fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%y%m%d")
        except ValueError:
            # Manejo en caso de que el formato de la fecha no sea válido
            return render(request, 'error.html', {'mensaje': 'Fecha no válida.'})
    else:
        # Usa la fecha actual si no se proporciona en los parámetros
        fecha = datetime.now().strftime("%y%m%d")
        
    particulas_dto= ParticulasDAO.obtener_todas_las_particulas()  
        
    particulas = {}
  
    particulas_dict = {particula.nombre_particula: (particula.id_particula, particula.descripcion) for particula in particulas_dto}

    
    for nombre, (particula_id, descripcion) in particulas_dict.items():
        try:
            estado_aire = SensorParticulaService.obtener_estado_aire(particula_id, nombre, fecha)
            particulas[nombre] = {'estado': estado_aire, 'descripcion': descripcion}
            
        except SensorParticulaService.SensorParticulaNoEncontrada:
            particulas[nombre] = {'estado': 'No hay datos', 'descripcion': descripcion}

    return render(request, 'semaforos.html', {'comuna': comuna, 'air_quality_data': particulas})