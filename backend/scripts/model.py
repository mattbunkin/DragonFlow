import json
import os
import subprocess
import numpy as np
from dotenv import load_dotenv
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report

load_dotenv()
DATA_FILE = os.getenv("DATA_FILE")
# DATA_FILE = os.getenv("/scripts/course_data.json")

# # Load the course data
with open(DATA_FILE, 'r') as f:
    data = json.load(f)

# data = pd.read_json('scripts/course_data.json')

def fetchProfRating(professor_name):
    """
    Fetches the rating of a professor from RateMyProfessors using a Node.js script.
    """
    # Ensure the Node.js script is in the correct path
    try:
        js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rmp", "rmp-api","rmp-data", "getRating.js"))
        
        #runs the Node.js script with the professor name as an argument
        result = subprocess.run(
            ["node", js_path, professor_name],
            capture_output=True,
            text=True
        )
        #returns the output of the script as a JSON object
        output = json.loads(result.stdout)
        return output.get("rating")
    
    #throws an error if the script fails to run or if the output is not valid JSON
    except Exception as e:
        # print(f"Error fetching RMP rating: {e}")
        return None

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
for crn, details in data.items():
    course_number = details.get('course_number', '')
    course_level = extract_course_level(course_number)
    credits = extract_credits(details.get('credits', '0'))
    has_prereqs = 1 if details.get('prereqs', '').strip() else 0
    instruction_type = details.get('instruction_type', 'Other').split('/')[0].strip()
    max_enroll = details.get('max_enroll', '0')
    enrollment = int(max_enroll) if max_enroll.isdigit() else 0

    # Fetch instructor names
    instructors = details.get('instructors', [])
    instructor_name = instructors[0]['name'] if instructors else 'Unknown'

    proffesor_rating = fetchProfRating(instructor_name)
    normalized_rating = proffesor_rating if proffesor_rating else 0

    # Calculate course difficulty based on level, credits, and prerequisites
    course_difficulty = (credits * 0.5) + (has_prereqs * 0.3) + (normalized_rating * 0.2)

    course_features.append({
        'crn': str(crn),
        'course_level': course_level,
        'credits': credits,
        'has_prereqs': has_prereqs,
        'instruction_type': instruction_type,
        'enrollment': enrollment,
        'course_difficulty': course_difficulty,
        'instructor': instructor_name
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
        success_score = (0.65 * gpa  # GPA has a strong positive impact
            - 0.8 * course['course_difficulty']  # Higher difficulty reduces success
            - 0.4 * course['has_prereqs']  # Prerequisites add some difficulty
            + np.random.normal(scale=0.25)  # Add some randomness
        )

        # Convert success_score to probability using logistic function
        success_prob = 1 / (1 + np.exp(-40 * success_score))
        success_prob = np.clip(success_prob, 0, 1)  # Ensure probability is between 0 and 1
        success = 1 if success_prob > 0.5 else 0

        synthetic_data.append({
            'gpa': gpa,
            'course_level': course['course_level'],
            'credits': course['credits'],
            'has_prereqs': course['has_prereqs'],
            'instruction_type': course['instruction_type'],
            'course_difficulty': course['course_difficulty'],
            'enrollment': course['enrollment'],
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
        'course_difficulty': course_info['course_difficulty'],
        'enrollment': course_info['enrollment']
    }
    
    # Store input data in a dataframe so it can be processed smoothly
    input_df = pd.DataFrame([input_data])
    input_transformed = preprocessor.transform(input_df)
    success_probability = model.predict_proba(input_transformed)[0][1]

        # Fetch professor's name and rating
    professor_name = course_info['instructor']
    professor_rating = fetchProfRating(professor_name)

    if professor_rating:
        print(f"Professor Rating for {professor_name}: {professor_rating}")
    else:
        print(f"Professor Rating for {professor_name}: Rating not available.")

    return success_probability

# User input of GPA and CRN to be calculated and predicted
if __name__ == "__main__":
    print(f"Model Accuracy: {test_accuracy:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred))
    try:
        user_gpa = float(input("Enter your GPA: "))
        user_crn = input("Enter the CRN: ")
        probability = predict_success_probability(user_gpa, user_crn)
        if isinstance(probability, float):
            print(f"Probability of success: {probability * 100:.2f}%")
        else:
            print(probability)
    except ValueError:
        print("Invalid input. Please enter a valid GPA.")

