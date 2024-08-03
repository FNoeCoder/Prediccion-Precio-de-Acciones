import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import json

from ErroresPerzonalizados import ErrorDatosNoDisponibles, ErrorRangoAñosInvalido

class PreciosAccion:
    def __init__(self, ticker_symbol, años):
        self.años = años
        self.rango_años = ""
        self.comprobar_años()
        self.ticker_symbol = ticker_symbol
        self.df = self.obtener_datos(self.rango_años)

    def obtener_datos(self, rango_años):
        ticker_data = yf.Ticker(self.ticker_symbol)
        df = ticker_data.history(period=rango_años)
        df.dropna(inplace=True)
        df.columns = ['Apertura', 'Alto', 'Bajo', 'Cierre', 'Volumen', 'Dividendos', 'Divisiones de acciones']
        df.index.name = 'Fecha'
        df = df.rename(columns={'Dividendos': 'Dividendos', 'Stock Splits': 'Divisiones de acciones'})
        if df.empty:
            raise ErrorDatosNoDisponibles(self.ticker_symbol)
        return df

    def comprobar_años(self):
        if self.años not in ["1", "2", "5", "10", "20", "inicioAño", "Maximo"]:
            raise ErrorRangoAñosInvalido(self.años)
        if self.años in ["1", "2", "5", "10", "20"]:
            self.rango_años = self.años + "y"
        elif self.años == "inicioAño":
            self.rango_años = "ytd"
        elif self.años == "Maximo":
            self.rango_años = "max"

    # def guardar_datos_CSV(self):
    #     self.df.to_csv("./Archivos/CSV/" + self.ticker_symbol + '_datos_historicos.csv')

    # def guardar_datos_JSON(self):
    #     datos = []
    #     for fecha, fila in self.df.iterrows():
    #         datos.append({
    #             "fecha": fecha.strftime("%Y-%m-%d"),
    #             "apertura": fila['Apertura'],
    #             "alto": fila['Alto'],
    #             "bajo": fila['Bajo'],
    #             "cierre": fila['Cierre'],
    #             "volumen": fila['Volumen'],
    #             "dividendos": fila['Dividendos'],
    #             "divisiones_de_acciones": fila['Divisiones de acciones']
    #         })
    #     with open(f"./Archivos/JSON/{self.ticker_symbol}_datos_historicos.json", 'w') as json_file:
    #         json.dump(datos, json_file, indent=4)

    def getDataFrame(self):
        return self.df

    def getSignificantData(self):
        return self.df.describe()

    def graficar_datos_precios(self):
        textoDeAños = self.getTextoDeAños()
        self.df['Cierre'].plot()
        self.df["Apertura"].plot()
        self.df["Alto"].plot()
        self.df["Bajo"].plot()
        plt.legend(["Cierre", "Apertura", "Alto", "Bajo"])
        plt.rcParams["figure.figsize"] = (20, 5)
        plt.title(f'Precios de {self.ticker_symbol} {textoDeAños}')
        plt.ylabel('Precio')
        plt.xlabel('Fecha')
        plt.grid()
        plt.show()

    def graficar_datos_especifico(self, tipoDato):
        if tipoDato not in ["Cierre", "Apertura", "Alto", "Bajo"]:
            return None
        textoDeAños = self.getTextoDeAños()
        self.df[tipoDato].plot()
        plt.rcParams["figure.figsize"] = (20, 5)
        plt.title(f'Precios de {tipoDato.lower()} de {self.ticker_symbol} {textoDeAños}')
        plt.ylabel('Precio')
        plt.xlabel('Fecha')
        plt.grid()
        plt.show()

    # def guardarGrafico(self, grafico):
    #     if grafico is None:
    #         print("No se puede guardar el gráfico")
    #     grafico.savefig("./Archivos/graficaIMG/" + self.ticker_symbol + '_grafico.png')


    def getTextoDeAños(self):
        if self.años == "1":
            return "1 año"
        elif self.años in ["2", "5", "10", "20"]:
            return self.años + " años"
        elif self.años == "inicioAño":
            return "desde el inicio del año"
        elif self.años == "Maximo":
            return "desde el inicio de la cotización"

if __name__ == "__main__":
    prueba = PreciosAccion('AAPL', '1')
    prueba.graficar_datos_precios()
    prueba.graficar_datos_especifico("Cierre")
    prueba.graficar_datos_especifico("Apertura")
    prueba.graficar_datos_especifico("Alto")
    prueba.graficar_datos_especifico("Bajo")

