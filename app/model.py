import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import os

# Cargar componentes una sola vez al iniciar la aplicación
MODEL_PATH = '/app/model.pkl'
SCALER_PATH = '/app/scaler.pkl'
COLUMNS_PATH = '/app/expected_columns.pkl'

# Verificar existencia de archivos pre-entrenados
if not all(os.path.exists(path) for path in [MODEL_PATH, SCALER_PATH, COLUMNS_PATH]):
    # Entrenar y guardar modelo si no existe
    df = pd.read_csv('/app/data.csv')
    df = pd.get_dummies(df, columns=['pais_origen', 'producto'])
    
    expected_columns = df.drop('cantidad_a_pedir', axis=1).columns.tolist()
    X = df.drop('cantidad_a_pedir', axis=1)
    y = df['cantidad_a_pedir']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    # Guardar artefactos
    joblib.dump(expected_columns, COLUMNS_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(model, MODEL_PATH)

# Cargar componentes desde archivos
try:
    scaler = joblib.load(SCALER_PATH)
    model = joblib.load(MODEL_PATH)
    expected_columns = joblib.load(COLUMNS_PATH)
except Exception as e:
    raise RuntimeError(f"Error cargando modelos: {str(e)}")

def predict(input_data: list):
    """Función de predicción optimizada"""
    try:
        input_df = pd.DataFrame([input_data], columns=expected_columns)
        input_scaled = scaler.transform(input_df)
        return float(model.predict(input_scaled)[0])
    except Exception as e:
        raise ValueError(f"Error en predicción: {str(e)}")