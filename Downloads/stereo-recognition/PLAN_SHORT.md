# План доработки - Краткая версия

## Проблема MVP v0.1.0
- ❌ Распознает весь кадр, а не только лист
- ❌ Нет выделения листа по углам
- ❌ Не различает типы контента (текст/код/рисунок)

## Решение: v0.5.0 (Enhanced MVP)

### 1. Детекция листа (Week 1-2) - PRIORITY 1
**Что делаем:**
- Находим лист бумаги в кадре (по контурам и углам)
- Применяем перспективную коррекцию ("вид сверху")
- Улучшаем качество изображения

**Результат:** Система работает ТОЛЬКО с листом, игнорируя фон

**Технологии:**
- OpenCV Canny edge detection
- Contour detection + approximation
- Perspective transform

**Файлы:**
```python
src/recognition_system/processing/
  ├── document_detector.py       # Поиск листа
  ├── perspective_transform.py   # Коррекция перспективы
  └── geometry_utils.py          # Геометрия
```

---

### 2. Сегментация контента (Week 3-4) - PRIORITY 2
**Что делаем:**
- Делим лист на регионы (блоки текста, рисунки и т.д.)
- Классифицируем каждый регион:
  - 📝 Рукописный текст
  - 🖨️ Печатный текст
  - 💻 Код (моноширинный)
  - 🎨 Рисунок/графика
- Распознаем каждый регион соответствующим способом

**Результат:** Распознается ВСЕ на листе с высокой точностью

**Технологии:**
- Connected Components Analysis
- ML classifier (CNN или готовая модель)
- EasyOCR (рукописный), Tesseract (печатный)

**Файлы:**
```python
src/recognition_system/
  ├── processing/region_detector.py      # Поиск регионов
  ├── ai/content_classifier.py           # Классификация типа
  ├── ai/handwriting_recognizer.py       # Рукописный текст
  ├── ai/text_recognizer.py              # Печатный текст/код
  └── ai/drawing_processor.py            # Рисунки
```

---

### 3. ArUco маркеры (Week 5-6) - PRIORITY 3
**Что делаем:**
- Используем специальные маркеры в углах листа
- Более точная детекция + калибровка камер

**Результат:** Еще выше точность и стабильность

**Опционально:** Можно пропустить если работает без маркеров

---

## Порядок разработки

### Неделя 1-2: Document Detection
```bash
git checkout -b feature/document-detection

# День 1-2: Corner detection
- Реализовать detect_paper_contours()
- Реализовать find_paper_quad()
- Тесты с реальными фото

# День 3-4: Perspective transform
- Реализовать calculate_transform_matrix()
- Реализовать apply_perspective_transform()
- Улучшение качества изображения

# День 5: Интеграция
- Добавить в simple_prototype.py
- Тестирование
- Commit v0.2.0
```

### Неделя 3-4: Content Segmentation
```bash
git checkout -b feature/content-segmentation

# День 1-2: Region detection
- Детекция регионов на листе
- Группировка близких элементов

# День 3-4: Classification
- Собрать датасет (фото примеров)
- Обучить/интегрировать классификатор

# День 5-7: Specialized recognizers
- Handwriting recognizer
- Text/Code recognizer
- Drawing processor

# День 8: Integration
- Полный pipeline
- Тестирование
- Commit v0.3.0
```

---

## Быстрый старт разработки

### 1. Создать базовую структуру
```bash
cd C:\Users\user\Downloads\stereo-recognition
venv\Scripts\activate

mkdir -p src/recognition_system/processing
mkdir -p src/recognition_system/ai
mkdir -p tests/unit
mkdir -p data/samples
```

### 2. Первый модуль: DocumentDetector
```python
# src/recognition_system/processing/document_detector.py

import cv2
import numpy as np

class DocumentDetector:
    def __init__(self, min_area_ratio=0.2, max_area_ratio=0.8):
        self.min_area = min_area_ratio
        self.max_area = max_area_ratio

    def detect(self, image):
        """Находит лист бумаги в кадре"""
        # 1. Preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 2. Edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # 3. Find contours
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # 4. Find largest quad
        corners = self._find_paper_quad(contours, image.shape)

        return corners

    def _find_paper_quad(self, contours, image_shape):
        """Ищет четырехугольник листа"""
        # TODO: Implement
        pass
```

### 3. Первый тест
```python
# tests/unit/test_document_detection.py

import pytest
import cv2
from src.recognition_system.processing.document_detector import DocumentDetector

def test_detect_paper():
    # Load test image
    image = cv2.imread('data/samples/paper_on_desk.jpg')

    detector = DocumentDetector()
    corners = detector.detect(image)

    assert corners is not None
    assert len(corners) == 4
```

---

## Output формат (v0.5.0)

```json
{
  "document": {
    "corners": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],
    "size": {"width": 2480, "height": 3508},
    "detected": true
  },
  "regions": [
    {
      "id": 1,
      "type": "handwritten_text",
      "bbox": {"x": 100, "y": 200, "w": 500, "h": 50},
      "content": "Привет, это рукописный текст",
      "confidence": 0.87,
      "color": {"r": 0, "g": 0, "b": 255}
    },
    {
      "id": 2,
      "type": "code",
      "bbox": {"x": 100, "y": 300, "w": 600, "h": 200},
      "content": "def hello():\n    print('world')",
      "confidence": 0.95,
      "language": "python"
    },
    {
      "id": 3,
      "type": "drawing",
      "bbox": {"x": 100, "y": 600, "w": 400, "h": 300},
      "image_path": "output/cycle_0001/region_3.png",
      "description": "Hand-drawn diagram"
    }
  ],
  "metadata": {
    "timestamp": "2024-11-24T15:30:00",
    "version": "0.5.0",
    "processing_time": 2.8
  }
}
```

---

## Производительность

**Target v0.5.0:**
- Document detection: <100ms
- Perspective transform: <50ms
- Region segmentation: <200ms
- OCR all regions: ~2-3 sec
- **Total: <3 секунды**

**Оптимизации:**
- GPU для OCR
- Параллельное распознавание регионов
- Кэширование углов листа

---

## Вопросы для уточнения

1. **Цветные листы?** Только белые или нужна поддержка цветной бумаги?
2. **Языки?** Достаточно RU/EN или нужны другие?
3. **Формулы?** Нужно распознавание математических формул (LaTeX)?
4. **Рисунки?** Векторизация или растр достаточно?
5. **Скорость?** Критично <3 сек или можно медленнее но точнее?

---

## Следующий шаг

**Начать с Week 1-2 (Document Detection):**

```bash
# Создать ветку
git checkout -b feature/document-detection

# Создать структуру
mkdir -p src/recognition_system/processing
touch src/recognition_system/processing/document_detector.py

# Начать разработку
code src/recognition_system/processing/document_detector.py
```

**Или хотите, чтобы я сразу начал реализацию?**
