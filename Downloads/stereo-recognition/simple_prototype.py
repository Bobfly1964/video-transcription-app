"""
Simple Recognition System - MVP Prototype
Система распознавания рукописного текста с двух веб-камер

Использование:
    python simple_prototype.py --interval 10 --cycles 5
    python simple_prototype.py  # Бесконечный режим
"""

import cv2
import numpy as np
import easyocr
import time
import json
import os
import argparse
from datetime import datetime
from typing import Optional, Tuple, List, Dict

class SimpleRecognitionSystem:
    """
    Простая система распознавания для MVP

    Features:
    - Захват с 1-2 камер
    - Детекция изменений
    - OCR распознавание (EasyOCR)
    - Сохранение цвета
    - Экспорт в JSON + PNG
    """

    def __init__(self, camera_ids: List[int] = [0, 1]):
        """
        Инициализация системы

        Args:
            camera_ids: Список ID камер для использования
        """
        print("🚀 Инициализация Stereo Recognition System...")
        print(f"   Version: 0.1.0 (MVP)")
        print(f"   Camera IDs: {camera_ids}")

        # Инициализация камер
        self._init_cameras(camera_ids)

        # Инициализация OCR
        self._init_ocr()

        # Состояние системы
        self.previous = None
        self.cycle = 0

        # Создание output директории
        os.makedirs('output', exist_ok=True)

        print("✓ Система готова к работе!\n")

    def _init_cameras(self, camera_ids: List[int]):
        """Инициализация камер"""
        print(f"   Открытие камер {camera_ids}...")

        self.cam1 = cv2.VideoCapture(camera_ids[0])
        self.cam2 = None

        if not self.cam1.isOpened():
            raise RuntimeError(f"Не удалось открыть камеру {camera_ids[0]}")

        # Настройка камеры 1
        self.cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # Попытка открыть вторую камеру
        if len(camera_ids) > 1 and camera_ids[1] != camera_ids[0]:
            self.cam2 = cv2.VideoCapture(camera_ids[1])
            if self.cam2.isOpened():
                self.cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                print("   ✓ Две камеры активны (стереорежим)")
            else:
                self.cam2 = None
                print("   ⚠ Только одна камера (монорежим)")
        else:
            print("   ℹ Режим одной камеры")

    def _init_ocr(self):
        """Инициализация OCR"""
        print("   Загрузка OCR моделей...")
        print("   (Первый запуск займет время - скачивание моделей ~100MB)")

        # EasyOCR для русского и английского
        self.reader = easyocr.Reader(
            ['ru', 'en'],
            gpu=False,  # Изменить на True если есть CUDA
            verbose=False
        )

        print("   ✓ OCR готов (русский, английский)")

    def capture_and_merge(self) -> Optional[np.ndarray]:
        """
        Захват кадров с камер и объединение

        Returns:
            Объединенное изображение или None при ошибке
        """
        ret1, frame1 = self.cam1.read()

        if not ret1:
            return None

        # Если есть вторая камера - объединяем
        if self.cam2 is not None:
            ret2, frame2 = self.cam2.read()
            if ret2:
                # Простое усреднение (в будущем - взвешенное объединение)
                merged = cv2.addWeighted(frame1, 0.5, frame2, 0.5, 0)
                return merged

        # Если только одна камера
        return frame1

    def detect_changes(self, current: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Детекция изменений на листе

        Args:
            current: Текущий кадр

        Returns:
            (has_changes, diff_image)
        """
        if self.previous is None:
            self.previous = current.copy()
            return True, current

        # Вычисление разницы
        diff = cv2.absdiff(current, self.previous)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        # Процент измененных пикселей
        changed_pixels = np.sum(thresh > 0)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        change_ratio = changed_pixels / total_pixels

        has_changes = change_ratio > 0.02  # 2% изменений

        if has_changes:
            self.previous = current.copy()

        return has_changes, diff

    def recognize_text(self, image: np.ndarray) -> List[Dict]:
        """
        Распознавание текста на изображении

        Args:
            image: Входное изображение (BGR)

        Returns:
            Список распознанных текстовых элементов
        """
        print("    📝 Распознавание текста...", end='', flush=True)

        # OCR распознавание
        results = self.reader.readtext(image)

        text_items = []
        for bbox, text, conf in results:
            # Координаты bounding box
            x = int(bbox[0][0])
            y = int(bbox[0][1])
            w = int(bbox[1][0] - bbox[0][0])
            h = int(bbox[2][1] - bbox[0][1])

            # Извлечение среднего цвета в регионе
            try:
                y_start = max(0, y)
                y_end = min(image.shape[0], y + h)
                x_start = max(0, x)
                x_end = min(image.shape[1], x + w)

                roi = image[y_start:y_end, x_start:x_end]
                if roi.size > 0:
                    avg_color = cv2.mean(roi)[:3]
                else:
                    avg_color = (0, 0, 0)
            except Exception:
                avg_color = (0, 0, 0)

            # Сохранение результата
            text_items.append({
                'text': text,
                'position': {'x': x, 'y': y},
                'bbox': {'x': x, 'y': y, 'width': w, 'height': h},
                'color': {
                    'r': int(avg_color[2]),  # BGR -> RGB
                    'g': int(avg_color[1]),
                    'b': int(avg_color[0])
                },
                'confidence': float(conf)
            })

        print(f" готово (найдено: {len(text_items)})")
        return text_items

    def save_results(self, text_items: List[Dict], image: np.ndarray) -> str:
        """
        Сохранение результатов в файлы

        Args:
            text_items: Распознанные текстовые элементы
            image: Исходное изображение

        Returns:
            Путь к директории цикла
        """
        self.cycle += 1

        # Создание директории для цикла
        cycle_dir = f'output/cycle_{self.cycle:04d}'
        os.makedirs(cycle_dir, exist_ok=True)

        # JSON с результатами
        output = {
            'cycle': self.cycle,
            'timestamp': datetime.now().isoformat(),
            'total_items': len(text_items),
            'items': text_items,
            'metadata': {
                'system_version': '0.1.0',
                'ocr_engine': 'easyocr',
                'languages': ['ru', 'en']
            }
        }

        # Сохранение JSON
        json_path = f'{cycle_dir}/recognized_text.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        # Создание изображения с аннотациями
        annotated = image.copy()
        for item in text_items:
            bbox = item['bbox']
            color = (0, 255, 0)  # Зеленый для bbox

            # Рисование bounding box
            cv2.rectangle(
                annotated,
                (bbox['x'], bbox['y']),
                (bbox['x'] + bbox['width'], bbox['y'] + bbox['height']),
                color,
                2
            )

            # Добавление текста (первые 20 символов)
            text_preview = item['text'][:20]
            cv2.putText(
                annotated,
                text_preview,
                (bbox['x'], bbox['y'] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
                cv2.LINE_AA
            )

        # Сохранение аннотированного изображения
        image_path = f'{cycle_dir}/annotated_image.png'
        cv2.imwrite(image_path, annotated)

        # Сохранение оригинального изображения
        original_path = f'{cycle_dir}/original_image.png'
        cv2.imwrite(original_path, image)

        print(f"    ✓ Сохранено в {cycle_dir}/")
        return cycle_dir

    def run(self, interval: int = 10, max_cycles: Optional[int] = None):
        """
        Главный цикл распознавания

        Args:
            interval: Интервал между проверками (секунды)
            max_cycles: Максимальное число циклов (None = бесконечно)
        """
        print(f"🚀 Запуск системы распознавания")
        print(f"   Интервал: {interval} сек")
        if max_cycles:
            print(f"   Максимум циклов: {max_cycles}")
        else:
            print(f"   Режим: непрерывный")
        print("   Нажмите Ctrl+C для остановки\n")

        cycles_done = 0

        try:
            while True:
                # Захват изображения
                merged = self.capture_and_merge()
                if merged is None:
                    print("⚠️ Ошибка захвата, пропускаю...", flush=True)
                    time.sleep(1)
                    continue

                # Детекция изменений
                has_changes, diff = self.detect_changes(merged)

                if has_changes:
                    print(f"\n📸 Цикл {self.cycle + 1}: Обнаружены изменения")

                    # Распознавание текста
                    text_items = self.recognize_text(merged)

                    if text_items:
                        print(f"    📊 Распознано элементов: {len(text_items)}")

                        # Вывод первых 3 элементов
                        for i, item in enumerate(text_items[:3], 1):
                            preview = item['text'][:40]
                            conf = item['confidence']
                            print(f"       {i}. {preview}... (уверенность: {conf:.2f})")

                        if len(text_items) > 3:
                            print(f"       ... и еще {len(text_items) - 3} элементов")

                        # Сохранение результатов
                        self.save_results(text_items, merged)
                    else:
                        print("    ℹ️ Текст не обнаружен")

                    cycles_done += 1

                    # Проверка лимита циклов
                    if max_cycles and cycles_done >= max_cycles:
                        print(f"\n✓ Выполнено {max_cycles} циклов, завершение...")
                        break
                else:
                    print(".", end="", flush=True)

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n🛑 Остановка по Ctrl+C")

        finally:
            self._cleanup()

    def _cleanup(self):
        """Очистка ресурсов"""
        print("🧹 Очистка ресурсов...")

        if self.cam1 is not None:
            self.cam1.release()

        if self.cam2 is not None:
            self.cam2.release()

        cv2.destroyAllWindows()

        print("✓ Система остановлена")
        print(f"✓ Всего обработано циклов: {self.cycle}")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Stereo Recognition System - MVP Prototype',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python simple_prototype.py --interval 10 --cycles 5
  python simple_prototype.py --cam1 0 --cam2 1
  python simple_prototype.py  # Бесконечный режим
        """
    )

    parser.add_argument(
        '--cam1',
        type=int,
        default=0,
        help='ID первой камеры (default: 0)'
    )
    parser.add_argument(
        '--cam2',
        type=int,
        default=1,
        help='ID второй камеры (default: 1, use same as cam1 for single camera)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Интервал между проверками в секундах (default: 10)'
    )
    parser.add_argument(
        '--cycles',
        type=int,
        default=None,
        help='Максимальное число циклов (default: None = бесконечно)'
    )

    args = parser.parse_args()

    try:
        # Создание и запуск системы
        system = SimpleRecognitionSystem(camera_ids=[args.cam1, args.cam2])
        system.run(interval=args.interval, max_cycles=args.cycles)

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
