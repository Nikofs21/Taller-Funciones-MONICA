from App.DAOSensorParticula import SensorParticulaDAO


class SensorParticulaService:
    class SensorParticulaNoEncontrada(Exception):
        pass

    @staticmethod
    def obtener_estado_aire(comuna_id, particula_id, fecha):
        """
        Obtiene el estado del aire para una partícula en una comuna y fecha específica.
        """
        # Intentar obtener promedio de registros para la partícula y fecha
        promedio = SensorParticulaDAO.obtener_promedio_por_particula_y_fecha(particula_id, comuna_id, fecha)

        if promedio is None:
            # Si no hay promedios disponibles, intentamos obtener el registro completo
            registro = SensorParticulaDAO.obtener_registro_por_particula_y_fecha(particula_id, fecha)
            if registro:
                # Priorizar validados, luego preliminares y finalmente no validados
                if registro.registros_validados > 0:
                    return SensorParticulaService._determinar_nivel(registro.registros_validados)
                elif registro.registros_preliminares > 0:
                    return SensorParticulaService._determinar_nivel(registro.registros_preliminares)
                elif registro.registros_no_validados > 0:
                    return SensorParticulaService._determinar_nivel(registro.registros_no_validados)
            raise SensorParticulaService.SensorParticulaNoEncontrada()

        # Determinar el nivel en base al promedio
        return SensorParticulaService._determinar_nivel(promedio)

    @staticmethod
    def determinar_estado_calidad_aire(valor, nom_particula):
        """
        Determina el estado y la descripción de calidad del aire basado en el valor y el tipo de partícula.
        """
        if nom_particula == 'PM10':
            if valor < 50:
                return 'Buena', 'verde'
            elif 50 <= valor <= 80:
                return 'Regular', 'amarillo'
            elif 80 < valor <= 110:
                return 'Alerta', 'naranja'
            elif 110 < valor <= 170:
                return 'Preemergencia', 'rojo'
            elif valor > 170:
                return 'Emergencia', 'rojo'

        elif nom_particula == 'PM25':
            if valor < 25:
                return 'Buena', 'verde'
            elif 25 <= valor <= 37:
                return 'Regular', 'amarillo'
            elif 37 < valor <= 55:
                return 'Alerta', 'naranja'
            elif 55 < valor <= 110:
                return 'Preemergencia', 'rojo'
            elif valor > 110:
                return 'Emergencia', 'rojo'

        elif nom_particula == 'O3':
            if valor < 100:
                return 'Buena', 'verde'
            elif 100 <= valor <= 160:
                return 'Regular', 'amarillo'
            elif 160 < valor <= 200:
                return 'Alerta', 'naranja'
            elif 200 < valor <= 300:
                return 'Preemergencia', 'rojo'
            elif valor > 300:
                return 'Emergencia', 'rojo'

        elif nom_particula == 'NO2':
            if valor < 50:
                return 'Buena', 'verde'
            elif 50 <= valor <= 100:
                return 'Regular', 'amarillo'
            elif 100 < valor <= 200:
                return 'Alerta', 'naranja'
            elif valor > 200:
                return 'Emergencia', 'rojo'

        elif nom_particula == 'SO2':
            if valor < 50:
                return 'Buena', 'verde'
            elif 50 <= valor <= 100:
                return 'Regular', 'amarillo'
            elif 100 < valor <= 250:
                return 'Alerta', 'naranja'
            elif valor > 250:
                return 'Emergencia', 'rojo'

        elif nom_particula == 'CO':
            if valor < 9:
                return 'Buena', 'verde'
            elif 9 <= valor <= 15:
                return 'Regular', 'amarillo'
            elif 15 < valor <= 30:
                return 'Alerta', 'naranja'
            elif valor > 30:
                return 'Emergencia', 'rojo'

        return 'Desconocido', 'gris'  # Valor predeterminado si el tipo de contaminante no es válido


    @staticmethod
    def _determinar_nivel(valor):
        """
        Determina el nivel de calidad del aire basado en el valor numérico.
        """
        if valor <= 50:
            return "verde"  # Bueno
        elif valor <= 100:
            return "amarillo"  # Moderado
        elif valor <= 150:
            return "naranja"  # Pre-emergencia
        else:
            return "rojo"  # Emergencia
        
        






