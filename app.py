import os
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

# --- DEBUGGING STEP 1 ---
print("Application script is starting...")

os.environ['TORCH_HOME'] = '/tmp/torch_cache'

app = FastAPI(title="YOLOv8 Car Damage Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO('best.pt')


@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Damage Detection API!"}


@app.post("/detect")
async def detect_damage(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    results = model(image)

    output = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            if confidence > 0.5:
                output.append({'name': class_name, 'confidence': confidence})

    return {"detections": output}


# --- DEBUGGING STEP 2 ---
# This will print all routes that FastAPI has successfully registered.
print("\n--- Registered Routes ---")
for route in app.routes:
    print(f"Path: {route.path}, Methods: {', '.join(route.methods)}")
print("-------------------------\n")