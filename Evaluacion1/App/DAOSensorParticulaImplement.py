from App.DAOSensorParticula import SensorParticulaDAO


class SensorParticulaService:
    class SensorParticulaNoEncontrada(Exception):
        pass

    @staticmethod
    @staticmethod
    def obtener_estado_aire(comuna_id, particula_id, fecha):
        """
        Calcula el estado del aire para una partícula específica en una comuna y fecha.
        """
        # Pasar el `comuna_id` al método DAO
        promedio = SensorParticulaDAO.obtener_promedio_por_particula_y_fecha(particula_id, comuna_id, fecha)

        if promedio is None:
            raise SensorParticulaService.SensorParticulaNoEncontrada

        # Determinar el estado según el promedio
        if promedio <= 50:
            return 'verde'
        elif promedio <= 100:
            return 'amarillo'
        elif promedio <= 150:
            return 'naranja'
        else:
            return 'rojo'

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

        
        






