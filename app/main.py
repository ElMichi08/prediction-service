from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.model import predict  # Asegúrate de que tu función predict esté adaptada
import pandas as pd

app = FastAPI()

@app.get("/predict-all/")
def predict_all():
    try:
        # Cargar datos desde el CSV
        df = pd.read_csv("/app/data.csv")
        
        # Lista para almacenar todas las predicciones
        predictions = []
        
        # Iterar sobre cada fila del DataFrame
        for _, row in df.iterrows():
            # Crear el input_data en el formato que espera tu modelo
            input_data = [
                row["pais_origen_China"], 
                row["pais_origen_México"], 
                row["producto_Producto_A"], 
                row["producto_Producto_B"], 
                row["producto_Producto_C"], 
                row["cantidad_pedida"], 
                row["tiempo_llegada"]
            ]
            
            # Obtener la predicción
            prediction = predict(input_data)
            
            # Guardar resultado
            predictions.append({
                "id": _,
                "predicted_cantidad_a_pedir": round(prediction, 2)
            })
        
        return JSONResponse(content={"predictions": predictions})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)