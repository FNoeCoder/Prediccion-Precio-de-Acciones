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
        grafico_base64 = preciosConPredicciones.graficar_predicciones_base64()
        grafico_base64_EDA = preciosConPredicciones.graficar_eda_base64()
        evaluacion = preciosConPredicciones.evaluar_modelo()


        return jsonify(
            {
                'ticker': ticker,
                'years': years,
                'tipo': tipo,
                'data': datos.to_dict(orient='records'),
                'grafico': grafico_base64,
                'graficoEDA': grafico_base64_EDA,
                'evaluacion': evaluacion
            }
            )
    except Exception as e:
        return jsonify({'error': str(e)})
    
# URL : http://localhost:5000/predict?ticker=MSFT&time=inicioA%C3%B1o&tipo=Cierre
# Ejecute el archivo app.py y luego abra un navegador web y escriba la URL anterior.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)