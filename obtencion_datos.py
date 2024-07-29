import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import json


class ErrorDatosNoDisponibles (Exception):
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.mensaje = f'Los datos para el ticker {self.ticker_symbol} no están disponibles'

    def __str__(self):
        return self.mensaje
class ErrorRangoAñosInvalido (Exception):
    def __init__(self, años):
        self.años = años
        self.mensaje = f'El rango de años {self.años} no es válido'

    def __str__(self):
        return self.mensaje


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
        # limpiar los datos
        df.dropna(inplace=True)
        df.columns = ['Apertura', 'Alto', 'Bajo', 'Cierre', 'Volumen', 'Dividends', 'Stock Splits']
        df.index.name = 'Fecha'
        df = df.rename(columns={'Dividends': 'Dividendos', 'Stock Splits': 'Divisiones de acciones'})
        if df.empty:
            # Lanzar una excepción si no hay datos
            raise ErrorDatosNoDisponibles(self.ticker_symbol)
        return df
    def comprobar_años(self):
        if self.años not in ["1", "2", "5", "10", "20", "inicioAño", "Maximo"]:
            # Lanzar una excepción si el rango de años no es válido
            raise ErrorRangoAñosInvalido(self.años)
        if self.años in ["1", "2", "5", "10", "20"]:
            self.rango_años = self.años + "y"
        elif self.años == "inicioAño":
            self.rango_años = "ytd"
        elif self.años == "Maximo":
            self.rango_años = "max"

        
    def guardar_datos_CSV(self):
        # fechaActual = pd.Timestamp.now().strftime("%d-%m-%Y")
        # horaActual = pd.Timestamp.now().strftime("%H:%M")
        # fechaHoraParaArchivo = fechaActual + "_" + horaActual
        # for simboloComflictivo in ["/", ":", " ",]:
        #     fechaHoraParaArchivo = fechaHoraParaArchivo.replace(simboloComflictivo, "_")
        # fechaHoraParaArchivo = fechaHoraParaArchivo.replace(" ", "_")

        self.df.to_csv("./Archivos/CSV/"+self.ticker_symbol + '_datos_historicos.csv')
    def guardar_datos_JSON(self):
        datos = []
        for fecha, fila in self.df.iterrows():
            datos.append({
                "fecha": fecha.strftime("%Y-%m-%d"),
                "apertura": fila['Apertura'],
                "alto": fila['Alto'],
                "bajo": fila['Bajo'],
                "cierre": fila['Cierre'],
                "volumen": fila['Volumen'],
                "dividendos": fila['Dividendos'],
                "divisiones_de_acciones": fila['Divisiones de acciones']
            })
        with open(f"./Archivos/JSON/{self.ticker_symbol}_datos_historicos.json", 'w') as json_file:
            json.dump(datos, json_file, indent=4)
        
    def getDataFrame(self):
        return self.df
    def getSignificantData(self):
        # Devolver un resumen de los datos
        # count -> número de valores no nulos
        # mean -> media
        # std -> desviación estándar
        # min -> mínimo
        # 25% -> percentil 25
        # 50% -> percentil 50 (mediana)
        # 75% -> percentil 75
        # max -> máximo
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
        return plt

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
        return plt
    def guardarGrafico(self, grafico):
        if grafico is None:
            print("No se puede guardar el gráfico")
        grafico.savefig("./Archivos/graficaIMG/"+self.ticker_symbol + '_grafico.png')

    def obenerIMG(self):
        # devovler la img del grafico en formato base64
        with open("./Archivos/graficaIMG/"+self.ticker_symbol + '_grafico.png', "rb") as img_file:
            img_base64 = img_file.read()
        return img_base64


    def getTextoDeAños(self):
        if self.años == "1":
            return "1 año"
        elif self.años in ["2", "5", "10", "20"]:
            return self.años + " años"
        elif self.años == "inicioAño":
            return "desde el inicio del año"
        elif self.años == "Maximo":
            return "desde el inicio de la cotización"

prueba = PreciosAccion('AAPL', '1')
prueba.guardar_datos_CSV()
prueba.guardar_datos_JSON()
prueba.guardarGrafico(prueba.graficar_datos_especifico("Cierre"))
