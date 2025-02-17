from fastapi import FastAPI
from pydantic import BaseModel
from app.model import predict

app = FastAPI()

class PredictionInput(BaseModel):
    pais_origen: str
    producto: str
    cantidad_pedida: int
    tiempo_llegada: int

@app.post("/predict/")
def make_prediction(input_data: PredictionInput):
    # Convertir a variables dummy
    data = {
        "pais_origen_China": 1 if input_data.pais_origen == "China" else 0,
        "pais_origen_México": 1 if input_data.pais_origen == "México" else 0,
        "producto_Producto_A": 1 if input_data.producto == "Producto_A" else 0,
        "producto_Producto_B": 1 if input_data.producto == "Producto_B" else 0,
        "producto_Producto_C": 1 if input_data.producto == "Producto_C" else 0,
        "cantidad_pedida": input_data.cantidad_pedida,
        "tiempo_llegada": input_data.tiempo_llegada
    }
    
    # Ordenar según las columnas esperadas por el modelo
    ordered_data = [data[col] for col in predict.expected_columns]
    
    prediction = predict(ordered_data)
    return {"predicted_cantidad_a_pedir": round(prediction, 2)}
