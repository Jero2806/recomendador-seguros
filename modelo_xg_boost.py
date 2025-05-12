import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Cargar dataset
df = pd.read_csv("dataset_usuarios_seguros.csv")

# 2. Separar features y etiqueta
X = df.drop("seguro_recomendado", axis=1)
y = df["seguro_recomendado"]

# 3. Codificar etiquetas (seguros)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Separar datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 5. Identificar columnas
numericas = ["edad", "ingresos_mensuales"]
categoricas = [col for col in X.columns if col not in numericas]

# 6. Crear preprocesador
preprocesador = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numericas),
    ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categoricas)
])

# 7. Crear pipeline de XGBoost
modelo = Pipeline(steps=[
    ("preprocesamiento", preprocesador),
    ("clasificador", XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", max_depth=6, n_estimators=100))
])

# 8. Entrenar modelo
modelo.fit(X_train, y_train)

# 9. Evaluar
y_pred = modelo.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy en test: {acc:.2%}")
print("\n📊 Reporte por clase:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# 10. Guardar modelo y codificador
joblib.dump(modelo, "modelo_xgboost.pkl")
joblib.dump(le, "label_encoder_xgb.pkl")
print("\n💾 Modelo XGBoost y LabelEncoder guardados exitosamente.")
