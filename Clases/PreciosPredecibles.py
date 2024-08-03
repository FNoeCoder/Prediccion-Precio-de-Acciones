from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from PreciosAccion import PreciosAccion

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
        predicciones.index = pd.date_range(start=self.DataFrameDatosObtenidos.index[-1], periods=self.pasos+1, freq='B')[1:]
        self.DataFrameDatosObtenidos[self.etapa].plot()
        predicciones['PredicciónCierre'].plot()
        plt.legend(["Datos reales", "Predicciones"])
        plt.rcParams["figure.figsize"] = (20, 5)
        plt.title(f'Predicción {self.etapa} de precios de {self.pasos} días')
        plt.ylabel('Precio')
        plt.xlabel('Fecha')
        plt.grid()
        plt.show()

if __name__ == "__main__":
    prueba = PreciosAccion('AAPL', '1')
    prueba2 = PreciosPredecibles(prueba.getDataFrame(), 'Cierre')
    prueba2.graficar_predicciones()