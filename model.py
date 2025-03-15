from ultralytics import YOLO
import cv2
import numpy as np
import os

from test import detected_folder  # Импортируем переменную с путем к папке

# Убедимся, что папка для сохранения существует
os.makedirs(detected_folder, exist_ok=True)

# Загрузка модели YOLOv8
model = YOLO('yolov8n.pt')

# Список цветов для различных классов
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]

# Функция для обработки изображения
def process_image(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)
    results = model(image)[0]

    # Получение оригинального изображения и результатов
    image = results.orig_img
    classes_names = results.names
    classes = results.boxes.cls.cpu().numpy()
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

    # Подготовка словаря для группировки результатов по классам
    grouped_objects = {}

    # Рисование рамок и группировка результатов
    for class_id, box in zip(classes, boxes):
        class_name = classes_names[int(class_id)]
        color = colors[int(class_id) % len(colors)]  # Выбор цвета для класса
        if class_name not in grouped_objects:
            grouped_objects[class_name] = []
        grouped_objects[class_name].append(box)

        # Рисование рамок на изображении
        x1, y1, x2, y2 = box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Создание путей для сохранения файлов
    base_filename = os.path.basename(image_path)
    filename_no_ext, ext = os.path.splitext(base_filename)
    new_image_path = os.path.join(detected_folder, f"{filename_no_ext}_yolo{ext}")
    text_file_path = os.path.join(detected_folder, f"{filename_no_ext}_data.txt")

    # Сохранение измененного изображения
    cv2.imwrite(new_image_path, image)

    # Сохранение данных в текстовый файл
    with open(text_file_path, 'w') as f:
        for class_name, details in grouped_objects.items():
            f.write(f"{class_name}:\n")

    print(f"Processed {image_path}:")
    print(f"Saved bounding-box image to {new_image_path}")
    print(f"Saved data to {text_file_path}")
