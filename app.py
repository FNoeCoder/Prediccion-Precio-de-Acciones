from flask import Flask, request, jsonify
from Clases.PreciosPredecibles import PreciosAccion, PreciosPredecibles
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['GET'])
def predict():
    ticker = request.args.get('ticker')
    years = request.args.get('time', '1')
    # tipo puede ser Cierre, Apertura, Alto, Bajo
    tipo = request.args.get('tipo', 'Cierre')
    try:
        historial = PreciosAccion(ticker, years)
        preciosConPredicciones = PreciosPredecibles(historial.getDataFrame(), tipo)
        datos = preciosConPredicciones.getDataFrame()

        return jsonify(
            {
                'ticker': ticker,
                'years': years,
                'tipo': tipo,
                'data': datos.to_dict(orient='records')
            }
            )
    except Exception as e:
        return jsonify({'error': str(e)})
    
# URL : http://localhost:5000/predict?ticker=MSFT&time=inicioA%C3%B1o&tipo=Cierre
# Ejecute el archivo app.py y luego abra un navegador web y escriba la URL anterior.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)