class ErrorDatosNoDisponibles(Exception):
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.mensaje = f'Los datos para el ticker {self.ticker_symbol} no están disponibles'
    def __str__(self):
        return self.mensaje

class ErrorRangoAñosInvalido(Exception):
    def __init__(self, años):
        self.años = años
        self.mensaje = f'El rango de años {self.años} no es válido'
    def __str__(self):
        return self.mensaje