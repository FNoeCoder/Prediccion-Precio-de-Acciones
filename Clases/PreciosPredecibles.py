from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from Clases.PreciosAccion import PreciosAccion
import io
import base64
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

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
        # cambiar el nombre de self.etapa a Precio
        datos = datos.rename(columns={self.etapa: 'Precio'})

        return datos
    
    def graficar_predicciones_base64(self):
        predicciones = self.predecir()
        predicciones = pd.DataFrame(predicciones)
        predicciones.columns = ['PredicciónCierre']
        predicciones.index = pd.date_range(start=self.DataFrameDatosObtenidos.index[-1], periods=self.pasos+1, freq='D')[1:]
        
        plt.figure(figsize=(20, 5))
        self.DataFrameDatosObtenidos[self.etapa].plot()
        predicciones['PredicciónCierre'].plot()
        plt.legend(["Datos reales", "Predicciones"])
        plt.title(f'Predicción {self.etapa} de precios de {self.pasos} días')
        plt.ylabel('Precio')
        plt.xlabel('Fecha')
        plt.grid()

        # Guardar la imagen en un buffer en memoria
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Convertir la imagen a base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        # Cerrar el buffer y la figura
        buf.close()
        plt.close()

        return img_base64
    def graficar_eda_base64(self):
        # Crear una figura con dos subgráficos
        fig, axs = plt.subplots(1, 2, figsize=(20, 10))
        
        # Gráfico de distribución de datos
        sns.histplot(self.DataFrameDatosObtenidos[self.etapa], ax=axs[0])
        axs[0].set_title('Distribución de Datos')

        # Gráfico de correlación entre variables
        sns.heatmap(self.DataFrameDatosObtenidos.corr(), annot=True, ax=axs[1], cmap='coolwarm')
        axs[1].set_title('Mapa de Calor de Correlaciones')
        
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        buf.close()
        plt.close(fig)

        return img_base64
    
    def evaluar_modelo(self):
        # Obtener datos verdaderos y predicciones
        datos_verdaderos = self.DataFrameDatosObtenidos[self.etapa].iloc[-self.pasos:].values
        predicciones = self.predecir()
        
        # Comparar predicciones con los datos verdaderos
        predicciones = predicciones.values
        
        # Calcular RMSE y MAE
        rmse = np.sqrt(mean_squared_error(datos_verdaderos, predicciones))
        mae = mean_absolute_error(datos_verdaderos, predicciones)
        
        return {
            # rmse y mae son los valores de error
            # rmse se refiere a la raíz cuadrada del error cuadrático medio
            # mae se refiere al error absoluto medio
            'rmse': rmse,
            'mae': mae
        }

if __name__ == "__main__":
    prueba = PreciosAccion('AAPL', '1')
    prueba2 = PreciosPredecibles(prueba.getDataFrame(), 'Cierre')
    print(prueba2.getDataFrame())