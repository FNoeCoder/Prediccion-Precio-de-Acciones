from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import matplotlib.pyplot as plt
from Clases.PreciosAccion import PreciosAccion

class PreciosPredecibles:
    def __init__(self, DataFrameDatosObtenidos, etapa):
        self.DataFrameDatosObtenidos = DataFrameDatosObtenidos
        self.pasos = 20
        # etapa debe ser Cierre, Apertura, Alto, Bajo
        if etapa not in ['Cierre', 'Apertura', 'Alto', 'Bajo']:
            raise ValueError('La etapa debe ser Cierre, Apertura, Alto o Bajo')
        self.etapa = etapa
        self.modelo = self.entrenar_modelo()
        self.ultimoRegistro = self.DataFrameDatosObtenidos['Cierre'].iloc[-1]


    def entrenar_modelo(self):
        modelo = SARIMAX(self.DataFrameDatosObtenidos[self.etapa], order=(1, 1, 1), seasonal_order=(1, 1, 0, 12))
        modelo_entrenado = modelo.fit()
        return modelo_entrenado

    def predecir(self):
        predicciones = self.modelo.forecast(steps=self.pasos)
        return predicciones

    # def guardar_predicciones(self):
    #     predicciones = self.predecir()
    #     predicciones = pd.DataFrame(predicciones)
    #     predicciones.columns = ['PredicciónCierre']
    #     predicciones.index = pd.date_range(start=self.DataFrameDatosObtenidos.index[-1], periods=self.pasos+1, freq='B')[1:]
    #     predicciones.to_csv("./Archivos/CSV/predicciones.csv")

    def graficar_predicciones(self):
        predicciones = self.predecir()
        predicciones = pd.DataFrame(predicciones)
        predicciones.columns = ['PredicciónCierre']
        predicciones.index = pd.date_range(start=self.DataFrameDatosObtenidos.index[-1], periods=self.pasos+1, freq='D')[1:]
        self.DataFrameDatosObtenidos[self.etapa].plot()
        predicciones['PrediccionCierre'].plot()
        plt.legend(["Datos reales", "Predicciones"])
        plt.rcParams["figure.figsize"] = (20, 5)
        plt.title(f'Predicción {self.etapa} de precios de {self.pasos} días')
        plt.ylabel('Precio')
        plt.xlabel('Fecha')
        plt.grid()
        plt.show()

    def getDataFrame(self):
        # obtener datos verdaderos con las fechas y la etapa
        datosVerdaderos = self.DataFrameDatosObtenidos[self.etapa]
        # añadir una columna que tenga de titulo tipo y que sea Verdadero
        datosVerdaderos = pd.DataFrame(datosVerdaderos)
        datosVerdaderos['Tipo'] = 'Verdadero'
        # obtener las predicciones
        predicciones = self.predecir()
        predicciones = pd.DataFrame(predicciones)
        predicciones.columns = [self.etapa]
        predicciones.index = pd.date_range(start=self.DataFrameDatosObtenidos.index[-1], periods=self.pasos+1, freq='D')[1:]
        # añadir una columna que tenga de titulo tipo y que sea Predicción
        predicciones['Tipo'] = 'Prediccion'

        datos = pd.concat([datosVerdaderos, predicciones])

        datos['Fecha'] = datos.index.strftime('%d-%m-%Y')
        # reordenar las columnas
        datos = datos[['Fecha', 'Tipo', self.etapa]]

        return datos

if __name__ == "__main__":
    prueba = PreciosAccion('AAPL', '1')
    prueba2 = PreciosPredecibles(prueba.getDataFrame(), 'Cierre')
    print(prueba2.getDataFrame())