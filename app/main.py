from fastapi import FastAPI
from pydantic import BaseModel
from app.model import predict

app = FastAPI()

# Definir el esquema de entrada
class PredictionInput(BaseModel):
    pais_origen_China: int
    pais_origen_México: int
    producto_Producto_A: int
    producto_Producto_B: int
    producto_Producto_C: int
    cantidad_pedida: int
    tiempo_llegada: int

@app.post("/predict/")
def make_prediction(input_data: PredictionInput):
    data = [
        input_data.pais_origen_China,
        input_data.pais_origen_México,
        input_data.producto_Producto_A,
        input_data.producto_Producto_B,
        input_data.producto_Producto_C,
        input_data.cantidad_pedida,
        input_data.tiempo_llegada,
    ]
    prediction = predict(data)
    return {"predicted_cantidad_a_pedir": prediction}
