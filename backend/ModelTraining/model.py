import json
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report

# Load the course data
file_path = "/Users/rikhilamacpro/DragonFlow/Backend/ModelTraining/data.json"
with open(file_path, 'r') as f:
    courses = json.load(f)

# Feature extraction functions
def extract_course_level(course_number):
    for char in course_number:
        if char.isdigit():
            return int(char)
    return 0

def extract_credits(credit_str):
    try:
        return float(credit_str.split()[0])
    except ValueError:
        return 0.0

# Parse course features
course_features = []
for crn, details in courses.items():
    course_number = details.get('course_number', '')
    course_level = extract_course_level(course_number)
    credits = extract_credits(details.get('credits', '0'))
    has_prereqs = 1 if details.get('prereqs', '').strip() else 0
    instruction_type = details.get('instruction_type', 'Other').split('/')[0].strip()

    # Calculate course difficulty based on level, credits, and prerequisites
    course_difficulty = (course_level * 0.4) + (credits * 0.3) + (has_prereqs * 0.3)

    course_features.append({
        'crn': str(crn),
        'course_level': course_level,
        'credits': credits,
        'has_prereqs': has_prereqs,
        'instruction_type': instruction_type,
        'course_difficulty': course_difficulty  # Realistic difficulty score
    })

# Convert to DataFrame
courses_df = pd.DataFrame(course_features)

# Generate synthetic data
np.random.seed(42)
synthetic_data = []
for _, course in courses_df.iterrows():
    for _ in range(500):  # 100 students per course
        gpa = np.random.normal(loc=2.5, scale=1.0)
        gpa = np.clip(gpa, 0.0, 4.0)

        # Improved success_score formula
        success_score = (0.3 * gpa  # GPA has a strong positive impact
            - 0.9 * course['course_difficulty']  # Higher difficulty reduces success
            - 0.2 * course['has_prereqs']  # Prerequisites add some difficulty
            + np.random.normal(scale=0.25)  # Add some randomness
        )

        # Convert success_score to probability using logistic function
        success_prob = 1 / (1 + np.exp(-success_score))
        success_prob = np.clip(success_prob, 0, 1)  # Ensure probability is between 0 and 1
        success = 1 if success_prob > 0.5 else 0

        synthetic_data.append({
            'gpa': gpa,
            'course_level': course['course_level'],
            'credits': course['credits'],
            'has_prereqs': course['has_prereqs'],
            'instruction_type': course['instruction_type'],
            'course_difficulty': course['course_difficulty'],
            'success': success
        })

# Create dataframe with the fake student data
df = pd.DataFrame(synthetic_data)

# Preprocess the data
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), ['instruction_type'])],
    remainder='passthrough'
)

# Choose which features will be trained and predicted for X and y
X = preprocessor.fit_transform(df.drop('success', axis=1))
y = df['success']

# Split data into sizes for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Hyperparameter tuning
best_params = {
    'n_estimators': 80,
    'learning_rate': 0.09,
    'max_depth': 3,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'subsample': 0.8,
    'max_features': 'sqrt'
}

# Train model with best parameters and selected features
model = GradientBoostingClassifier(**best_params, random_state=42)
model.fit(X_train, y_train)

# Evaluate model based on accuracy and F1-score
y_test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred) * 100
print(f"Model Accuracy: {test_accuracy:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

# Function to predict success probability
def predict_success_probability(gpa, crn):
    if crn not in courses_df['crn'].values:
        return "CRN not found in the dataset."
    
    course_info = courses_df[courses_df['crn'] == crn].iloc[0]
    input_data = {
        'gpa': gpa,
        'course_level': course_info['course_level'],
        'credits': course_info['credits'],
        'has_prereqs': course_info['has_prereqs'],
        'instruction_type': course_info['instruction_type'],
        'course_difficulty': course_info['course_difficulty']
    }
    
    # Store input data in a dataframe so it can be processed smoothly
    input_df = pd.DataFrame([input_data])
    input_transformed = preprocessor.transform(input_df)
    success_probability = model.predict_proba(input_transformed)[0][1]
    return success_probability

# User input of GPA and CRN to be calculated and predicted
try:
    user_gpa = float(input("Enter your GPA (Grade Point Average): "))
    user_crn = input("Enter the CRN (Course Number): ")
    probability = predict_success_probability(user_gpa, user_crn)
    if isinstance(probability, float):
        print(f"Probability of success: {probability * 100:.2f}%")
    else:
        print(probability)
except ValueError:
    print("Invalid input. Please enter a valid GPA.")



