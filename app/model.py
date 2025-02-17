import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import os

# Ruta donde se almacenarán los artefactos
MODEL_PATH = '/app/model.pkl'
SCALER_PATH = '/app/scaler.pkl'
COLUMNS_PATH = '/app/expected_columns.pkl'

# Función para cargar o entrenar el modelo
def load_or_train_model():
    if not all(os.path.exists(path) for path in [MODEL_PATH, SCALER_PATH, COLUMNS_PATH]):
        # Entrenamiento solo si no existen los archivos
        df = pd.read_csv('/app/data.csv')
        df = pd.get_dummies(df, columns=['pais_origen', 'producto'])

        expected_columns = df.drop('cantidad_a_pedir', axis=1).columns.tolist()
        X = df.drop('cantidad_a_pedir', axis=1)
        y = df['cantidad_a_pedir']

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)

        # Guardar los artefactos
        joblib.dump(expected_columns, COLUMNS_PATH)
        joblib.dump(scaler, SCALER_PATH)
        joblib.dump(model, MODEL_PATH)
    else:
        # Cargar modelo si ya existe
        scaler = joblib.load(SCALER_PATH)
        model = joblib.load(MODEL_PATH)
        expected_columns = joblib.load(COLUMNS_PATH)

    return model, scaler, expected_columns

# Función de predicción
def predict(input_data: list):
    """Función de predicción optimizada"""
    model, scaler, expected_columns = load_or_train_model()
    
    try:
        input_df = pd.DataFrame([input_data], columns=expected_columns)
        input_scaled = scaler.transform(input_df)
        return float(model.predict(input_scaled)[0])
    except Exception as e:
        raise ValueError(f"Error en predicción: {str(e)}")
