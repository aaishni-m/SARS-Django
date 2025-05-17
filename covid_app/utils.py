import torch
import torch.nn.functional as F
import joblib
from PIL import Image, ImageOps
from torchvision import transforms

# Paths to models
joblib_model_path = "D:/SARS/symptoms.joblib"
pth_model_path = "D:/SARS/CovidTest.pth"

# Load the Joblib model
joblib_model = joblib.load(joblib_model_path)

# Define the PyTorch model architecture
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

# Load the PyTorch model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pth_model = SimplifiedCNN().to(device)
pth_model.load_state_dict(torch.load(pth_model_path, map_location=device))
pth_model.eval()

# Preprocessing function
def image_pre(path):
    try:
        size = (224, 224)
        image = Image.open(path).convert("RGB")
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        image_tensor = transform(image).unsqueeze(0)
        return image_tensor
    except Exception as e: 
        raise ValueError(f"Error processing image: {e}")

# Joblib model prediction
def predict_with_joblib(prediction_data):
    features = list(prediction_data.values())
    probabilities = joblib_model.predict_proba([features])
    return probabilities[0][1] * 100

# PyTorch model prediction
def predict_with_pth(image_tensor):
    with torch.no_grad():
        logits = pth_model(image_tensor)
        probabilities = F.softmax(logits, dim=1)
        return probabilities[0, 1].item() * 100

# Compare models
def compare_models(image_path, prediction_data):
    image_tensor = image_pre(image_path).to(device)
    joblib_percentage = predict_with_joblib(prediction_data)
    pth_percentage = predict_with_pth(image_tensor)
    return (joblib_percentage + pth_percentage) / 2
