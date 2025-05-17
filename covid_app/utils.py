import os
import torch
import torch.nn.functional as F
import joblib
from PIL import Image, ImageOps
from torchvision import transforms

# Paths to models
joblib_model_path = "D:/SARS/symptoms.joblib"
pth_model_path = "D:/SARS/CovidTest.pth"

# Load the Joblib model
try:
    joblib_model = joblib.load(joblib_model_path)
    print("[INFO] Joblib model loaded successfully.")
except Exception as e:
    raise ValueError(f"[ERROR] Loading Joblib model failed: {e}")

# Define the PyTorch CNN model
class SimplifiedCNN(torch.nn.Module):
    def __init__(self):
        super(SimplifiedCNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 32, 3, 1, 1)
        self.conv2 = torch.nn.Conv2d(32, 64, 3, 1, 1)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.fc1 = torch.nn.Linear(64 * 56 * 56, 128)
        self.fc2 = torch.nn.Linear(128, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 56 * 56)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Setup device and load PyTorch model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pth_model = SimplifiedCNN().to(device)
try:
    pth_model.load_state_dict(torch.load(pth_model_path, map_location=device))
    pth_model.eval()
    print("[INFO] PyTorch model loaded successfully.")
except Exception as e:
    raise ValueError(f"[ERROR] Loading PyTorch model failed: {e}")

# Image preprocessing
def image_pre(path):
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image file not found: {path}")

        size = (224, 224)
        image = Image.open(path).convert("RGB")
        print("[INFO] Image opened.")

        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        print("[INFO] Image resized to 224x224.")

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        image_tensor = transform(image).unsqueeze(0)
        print(f"[INFO] Image transformed to tensor with shape {image_tensor.shape}")
        return image_tensor
    except FileNotFoundError as fnf:
        raise ValueError(f"[ERROR] {fnf}")
    except OSError as ose:
        raise ValueError(f"[ERROR] Image file error: {ose}")
    except Exception as e:
        raise ValueError(f"[ERROR] Unexpected error processing image: {e}")

# Prepare features correctly for your joblib model
def prepare_features(prediction_data):
    # Map your user input keys to the exact model keys & order
    gender_map = {'male': 0, 'female': 1, 'other': 2}
    
    features = {
        "Fever": int(prediction_data.get("fever", 0)),
        "Tiredness": int(prediction_data.get("tiredness", 0)),
        "Dry-Cough": int(prediction_data.get("dry_cough", 0)),
        "Difficulty-in-Breathing": int(prediction_data.get("difficulty_breathing", 0)),
        "Sore-Throat": int(prediction_data.get("sore_throat", 0)),
        "Pains": int(prediction_data.get("body_pain", 0)),
        "Nasal-Congestion": int(prediction_data.get("nasal_congestion", 0)),
        "Runny-Nose": int(prediction_data.get("runny_nose", 0)),
        "Diarrhea": int(prediction_data.get("diarrhea", 0)),
        "Severity": int(prediction_data.get("severity", 1)),  # default Mild=1
        "Gender": gender_map.get(prediction_data.get("gender", "other").lower(), 2),
        "Age": int(prediction_data.get("age", 30)),           # default age 30
        "Oxygen Level": float(prediction_data.get("oxygen_level", 98.0))  # default 98%
    }
    return features

# Joblib prediction
def predict_with_joblib(prediction_data):
    try:
        features = prepare_features(prediction_data)
        # Ensure ordering matches model input exactly:
        ordered_features = [features[f] for f in [
            "Fever", "Tiredness", "Dry-Cough", "Difficulty-in-Breathing", "Sore-Throat",
            "Pains", "Nasal-Congestion", "Runny-Nose", "Diarrhea",
            "Severity", "Gender", "Age", "Oxygen Level"
        ]]
        probabilities = joblib_model.predict_proba([ordered_features])
        print("[INFO] Joblib prediction successful.")
        return probabilities[0][1] * 100
    except Exception as e:
        raise ValueError(f"[ERROR] Joblib prediction failed: {e}")

# PyTorch prediction
def predict_with_pth(image_tensor):
    try:
        with torch.no_grad():
            image_tensor = image_tensor.to(device)
            logits = pth_model(image_tensor)
            probabilities = F.softmax(logits, dim=1)
            print("[INFO] PyTorch prediction successful.")
            return probabilities[0, 1].item() * 100
    except Exception as e:
        raise ValueError(f"[ERROR] PyTorch prediction failed: {e}")

# Combine predictions
def compare_models(image_path, prediction_data):
    try:
        image_tensor = image_pre(image_path)
        joblib_pct = predict_with_joblib(prediction_data)
        pth_pct = predict_with_pth(image_tensor)
        avg_pct = (joblib_pct + pth_pct) / 2
        print(f"[INFO] Combined prediction percentage: {avg_pct:.2f}%")
        return avg_pct
    except Exception as e:
        raise ValueError(f"[ERROR] Model comparison failed: {e}")

# Example usage
if __name__ == "__main__":
    test_image = "D:/SARS/test_image.jpg"  # Replace with your image path
    test_data = {
        "gender": "female",
        "fever": 1,
        "tiredness": 0,
        "dry_cough": 1,
        "difficulty_breathing": 0,
        "sore_throat": 0,
        "body_pain": 0,
        "nasal_congestion": 1,
        "runny_nose": 1,
        "diarrhea": 0,
        "severity": 2,        # Moderate
        "age": 29,
        "oxygen_level": 96.5
    }

    try:
        result = compare_models(test_image, test_data)
        print(f"Final averaged prediction: {result:.2f}%")
    except ValueError as e:
        print(e)
