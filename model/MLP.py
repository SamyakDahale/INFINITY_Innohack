import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report

import pickle

# Load the dataset
file_path = r"E:\MGM UDICT\CSMSS hackathon\model\health_markers_dataset_with_outliers.csv"
df = pd.read_csv(file_path)

# Assuming last column is the target variable
target_column = df.columns[-1]
X = df.drop(columns=[target_column])
y = df[target_column]

# 1. Mean Value Imputation
X_filled = X.fillna(X.mean())

# 2. Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 3. Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_filled)

# 4. Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# 5. Initialize and train MLP model
mlp_model = MLPClassifier(hidden_layer_sizes=(128, 64, 32), activation='relu', solver='adam', max_iter=200)
mlp_model.fit(X_train, y_train)

# 6. Predictions
y_pred = mlp_model.predict(X_test)

# 7. Print results
print("\nModel Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


def predict_new_data(new_data):
    # Apply mean imputation for missing values
    imputed_data = new_data.fillna(X.mean())  # Use the same mean values from training data
    
    # Scale features
    scaled_data = scaler.transform(imputed_data)
    
    # Make prediction
    prediction = mlp_model.predict(scaled_data)
    
    # Convert prediction back to label
    predicted_label = label_encoder.inverse_transform(prediction)
    
    return predicted_label


with open('model.pkl', 'wb') as file:
    pickle.dump(mlp_model, file)
print("Model saved as model.pkl")

# Save both objects
with open('label_encoder.pkl', 'wb') as le_file:
    pickle.dump(label_encoder, le_file)

with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

print("LabelEncoder and Scaler saved successfully!")










