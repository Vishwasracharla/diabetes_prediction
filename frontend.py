import pickle
import numpy as np
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the trained model
try:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    print(Fore.MAGENTA + Style.BRIGHT + "[ERROR]" + Fore.WHITE + " model.pkl not found. Please make sure the trained model is saved.")
    exit()

def display_banner():
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 55)
    print(Fore.MAGENTA + Style.BRIGHT + "        🩺 Diabetes Prediction - Terminal UI")
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 55)

def get_user_input():
    print(Fore.WHITE + Style.BRIGHT + "\nPlease enter the following details:\n")
    Pregnancies = int(input(Fore.WHITE + "🔹 Number of Pregnancies: "))
    Glucose = float(input("🔹 Glucose Level: "))
    BloodPressure = float(input("🔹 Blood Pressure: "))
    SkinThickness = float(input("🔹 Skin Thickness: "))
    Insulin = float(input("🔹 Insulin Level: "))
    BMI = float(input("🔹 BMI: "))
    DiabetesPedigreeFunction = float(input("🔹 Diabetes Pedigree Function: "))
    Age = int(input("🔹 Age: "))

    return np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

def predict_diabetes(user_data):
    prediction = model.predict(user_data)
    print("\n" + Fore.MAGENTA + "=" * 55)
    if prediction[0] == 1:
        print(Fore.MAGENTA + Style.BRIGHT + "⚠️  Prediction:" + Fore.WHITE + " The person is likely to have diabetes.")
    else:
        print(Fore.MAGENTA + Style.BRIGHT + "✅ Prediction:" + Fore.WHITE + " The person is NOT likely to have diabetes.")
    print(Fore.MAGENTA + "=" * 55)

if __name__ == "__main__":
    display_banner()
    user_data = get_user_input()
    predict_diabetes(user_data)
