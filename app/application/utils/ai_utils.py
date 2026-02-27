from ultralytics import YOLO
import os
import shutil
import random
    
base_script_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(base_script_path, "../../../"))

def ai_train():
    print("--------- STARTING AI TRAINING ---------")
    model_path = os.getenv("YOLO_MODEL_PATH")
    model =  YOLO(model_path)
    
    data_yaml = os.path.join(root_path, "data.yaml")
    model.train(
        data=data_yaml,
        epochs=50,
        imgsz=640,
        batch=32,   
        device=0
    )
    print("--------- AI TRAINED WITH SUCCESS ---------")

def organize_ai_train_folders(): 
    print("--------- STARTING ORGANIZE TRAINING FOLDERS ---------")
    dataset_folder_name = "dataset_1"
    image_folder_name = "images"
    label_folder_name = "labels"

    train_image_path = f"{root_path}/{dataset_folder_name}/{image_folder_name}/train"
    val_image_path = f"{root_path}/{dataset_folder_name}/{image_folder_name}/val"

    train_label_path = f"{root_path}/{dataset_folder_name}/{label_folder_name}/train"
    val_label_path = f"{root_path}/{dataset_folder_name}/{label_folder_name}/val"

    image_src_dir = f"{root_path}/{dataset_folder_name}/{image_folder_name}"
    label_src_dir = f"{root_path}/{dataset_folder_name}/{label_folder_name}"

    os.makedirs(train_image_path, exist_ok=True)
    os.makedirs(val_image_path, exist_ok=True)
    os.makedirs(train_label_path, exist_ok=True)
    os.makedirs(val_label_path, exist_ok=True)

    images = [
        f
        for f in os.listdir(f"{root_path}/{dataset_folder_name}/{image_folder_name}")
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]

    random.shuffle(images)
    split_idx = int(len(images) * 0.8)
    train_imgs = images[:split_idx]
    val_imgs = images[split_idx:]

    for img_name in train_imgs:
        src_path = os.path.join(image_src_dir, img_name)
        
        shutil.copy(src_path, os.path.join(train_image_path, img_name))
        
        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_src_path = os.path.join(label_src_dir, label_name)
        
        if os.path.exists(label_src_path):
            shutil.copy(label_src_path, os.path.join(train_label_path, label_name))

    for img_name in val_imgs:
        src_path = os.path.join(image_src_dir, img_name)
        
        shutil.copy(src_path, os.path.join(val_image_path, img_name))
        
        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_src_path = os.path.join(label_src_dir, label_name)
        
        if os.path.exists(label_src_path):
            shutil.copy(label_src_path, os.path.join(val_label_path, label_name))
    
    print("--------- FOLDERS ORGANIZED WITH SUCCESS ---------")
        