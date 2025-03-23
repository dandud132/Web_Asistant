import cv2
import numpy as np

def recognize_color(image_path):
    """
    Распознает доминирующий цвет в изображении.

    Args:
        image_path: Путь к изображению.

    Returns:
        Строка, представляющая распознанный цвет, или None, если цвет не удалось определить.
    """

    try:
        # 1. Загрузка изображения
        img = cv2.imread(image_path)
        if img is None:
            print(f"Ошибка: Не удалось загрузить изображение по пути {image_path}")
            return None

        # 2. Изменение размера изображения (необязательно, для ускорения анализа)
        resized_img = cv2.resize(img, (100, 100))

        # 3. Преобразование в цветовое пространство HSV
        hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)

        # 4. Определение диапазонов цветов HSV (примеры)
        #    Эти диапазоны нужно настроить под ваши конкретные нужды и условия.
        color_ranges = {
            "red":   ([0, 70, 50], [10, 255, 255]),  # Красный оттенок 1
            "red2":  ([170, 70, 50], [180, 255, 255]), # Красный оттенок 2 (из-за циклической природы hue)
            "green": ([36, 70, 50], [86, 255, 255]),
            "blue":  ([110, 70, 50], [130, 255, 255]),
            "yellow": ([25, 70, 50], [35, 255, 255]),
            "orange": ([11, 70, 50], [24, 255, 255]),
            "purple": ([131, 70, 50], [170, 255, 255]),
            "brown":  ([10, 60, 40], [20, 255, 200]), #пример коричневого, может потребовать настройки
            "gray":  ([0, 0, 40], [180, 30, 200]) #пример серого
        }

        # 5. Анализ пикселей и определение доминирующего цвета
        color_counts = {}
        for color_name, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # Создание маски для выделения пикселей, соответствующих диапазону цвета
            mask = cv2.inRange(hsv_img, lower, upper)

            # Подсчет количества пикселей в маске
            color_counts[color_name] = cv2.countNonZero(mask)

        # 6. Определение доминирующего цвета
        if color_counts:
            dominant_color = max(color_counts, key=color_counts.get)
            return dominant_color
        else:
            return "Не удалось определить цвет"

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# Пример использования
image_path = ""  # Замените на путь к вашему изображению
color = recognize_color(image_path)

if color:
    print(f"Распознанный цвет: {color}")
else:
    print("Не удалось распознать цвет.")