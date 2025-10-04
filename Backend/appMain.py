import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -------------------------
# Step 1: Load the dataset
# -------------------------
df = pd.read_csv("DATA/Temp/student_data_minimal_with_random.csv")

# -------------------------
# Step 2: Compute a combined risk score
# -------------------------
# Normalize factors to 0-100 scale
# Scale Attendance and Avg_Score by 1.5
df['Attendance_Score'] = (100 - df['Attendance%']) * 1.5
df['Avg_Score_Risk'] = (100 - df['Avg_Score']) * 1.5

# Increase Backlogs/Failures impact
df['Backlogs_Score'] = df['Backlogs'] * 30
df['Failures_Score'] = df['failures'] * 30

# Recompute Risk Score
df['Risk_Score'] = (
    0.4 * df['Attendance_Score'] +
    0.4 * df['Avg_Score_Risk'] +
    0.1 * df['Backlogs_Score'] +
    0.1 * df['Failures_Score']
)

# -------------------------
# Step 3: Define 5-level Risk_Label
# -------------------------
def risk_level(score):
    if score >= 80:
        return "Very High"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Low"
    else:
        return "Very Low"

df['Risk_Label_5'] = df['Risk_Score'].apply(risk_level)

# -------------------------
# Step 4: Preprocess for ML
# -------------------------
features_to_keep = ["sex", "age", "absences", "G1", "G2", "failures", "studytime",
                    "famsup", "higher", "Attendance%", "Avg_Score", "Backlogs"]
X = df[features_to_keep].copy()
y = df['Risk_Label_5']

# Encode categorical features
le = LabelEncoder()
for col in ['sex', 'famsup', 'higher']:
    X[col] = le.fit_transform(X[col])

# -------------------------
# Step 5: Split dataset
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------
# Step 6: Train model
# -------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------
# Step 7: Evaluate
# -------------------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# -------------------------
# Step 8: Predict for all students
# -------------------------
df_predict = X.copy()
df['Predicted_Risk_Label_5'] = model.predict(df_predict)

# -------------------------
# Step 9: Save results
# -------------------------
df.to_csv("student_data_with_5level_multifactor_predictions.csv", index=False)
print("5-level multifactor Risk predictions saved to student_data_with_5level_multifactor_predictions.csv")
