import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Cargar los datos de ejemplo
df = pd.read_csv('app/data.csv')

# Preprocesar los datos
df = pd.get_dummies(df, columns=['pais_origen', 'producto'])

# Definir las variables de entrada (X) y la salida (y)
X = df.drop('cantidad_a_pedir', axis=1)
y = df['cantidad_a_pedir']

# Escalar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Crear el modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Entrenar el modelo
model.fit(X_train, y_train)

def predict(data):
    # Preprocesar los datos de entrada
    data_scaled = scaler.transform([data])
    prediction = model.predict(data_scaled)
    return prediction[0]
