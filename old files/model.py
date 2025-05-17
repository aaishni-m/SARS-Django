import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image, ImageOps
import joblib
from torchvision import transforms

# Paths to models
joblib_model_path = "D:/SARS/covid_app/models/symptoms.joblib"
pth_model_path = "D:/SARS/CovidTest.pth"


# Load the Joblib model
joblib_model = joblib.load(joblib_model_path)

# Define a PyTorch model architecture that matches the `.pth` file
class SimplifiedCNN(torch.nn.Module):
    def __init__(self):
        super(SimplifiedCNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv2 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = torch.nn.Linear(64 * 56 * 56, 128)
        self.fc2 = torch.nn.Linear(128, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 56 * 56)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load the `.pth` model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pth_model = SimplifiedCNN().to(device)
pth_model.load_state_dict(torch.load(pth_model_path, map_location=device))
pth_model.eval()

# Image preprocessing function for PyTorch model
def image_pre(path):
    try:
        size = (224, 224)  # Correct target size for model input
        image = Image.open(path)  # Open the image
        image = ImageOps.grayscale(image)  # Convert to grayscale

        # Convert grayscale to RGB by duplicating the single channel
        image = ImageOps.grayscale(image).convert("RGB")

        # Resize the image to 224x224 as required by the model
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)  # Resize to 224x224

        # Apply the transformations directly
        transform = transforms.Compose([
            transforms.ToTensor(),  # Convert to tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
        ])

        # Apply transformations to image
        image_tensor = transform(image)

        # Add a batch dimension (model expects [batch_size, channels, height, width])
        image_tensor = image_tensor.unsqueeze(0)  # Shape becomes [1, 3, 224, 224]

        return image_tensor

    except Exception as e:
        print(f"Error in processing image: {e}")
        raise e

# Joblib model prediction function (takes structured symptom data)
def predict_with_joblib(prediction_data):
    """Predict COVID probability using the joblib model with symptom data."""
    features = [
        prediction_data['fever'],
        prediction_data['tiredness'],
        prediction_data['dry_cough'],
        prediction_data['difficulty_breathing'],
        prediction_data['sore_throat'],
        prediction_data['no_other_symptoms'],
        prediction_data['body_pain'],
        prediction_data['nasal_congestion'],
        prediction_data['runny_nose'],
        prediction_data['diarrhea'],
        prediction_data['severity'],
        prediction_data['oxygen_level']
    ]
    
    # Get probabilities from joblib model
    probabilities = joblib_model.predict_proba([features])  # Predict with joblib model
    covid_probability = probabilities[0][1] * 100  # Class 1 (COVID) probability
    return covid_probability

# PyTorch model prediction function (takes image tensor)
def predict_with_pth(image_tensor):
    """Predict COVID probability using the PyTorch model."""
    with torch.no_grad():
        logits = pth_model(image_tensor)  # Get raw outputs
        probabilities = F.softmax(logits, dim=1)  # Apply softmax to get probabilities
        covid_probability = probabilities[0, 1].item() * 100  # Class 1 (COVID) probability
    return covid_probability

# Comparison function (compares both models' predictions)
def compare_models(image_path,prediction_data):
    """Compare predictions from both models."""
    # Get preprocessed image tensor for PyTorch model
    image_tensor = image_pre(image_path)

    # Get predictions from both models
    joblib_percentage = predict_with_joblib(prediction_data)  # Joblib model uses structured symptom data
    pth_percentage = predict_with_pth(image_tensor)  # PyTorch model uses image data

    # Print individual predictions
    # print(f"Joblib Model Prediction: {joblib_percentage:.2f}% chance of COVID")
    # print(f"PyTorch Model Prediction: {pth_percentage:.2f}% chance of COVID")

    # Calculate and print the average of both predictions
    avg_percentage = (joblib_percentage + pth_percentage) / 2
    print(f"Average COVID Probability: {avg_percentage:.2f}%")

    return avg_percentage

