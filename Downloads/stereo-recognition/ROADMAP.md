# Stereo Recognition System - Roadmap & Development Plan

## Проблема текущего MVP (v0.1.0)

**Обнаруженные issues:**
1. ❌ Система распознает ВСЕ в кадре, а не только лист бумаги
2. ❌ Нет автоматического выделения листа по углам
3. ❌ Отсутствует классификация контента (текст/код/рисунок)
4. ❌ Рукописный текст распознается плохо
5. ❌ Нет перспективной коррекции (если лист под углом)

## Цель доработки

**Создать систему, которая:**
1. ✅ Автоматически находит лист бумаги в кадре (по углам)
2. ✅ Выделяет только область листа для обработки
3. ✅ Применяет перспективную коррекцию
4. ✅ Классифицирует контент на типы:
   - Рукописный текст
   - Печатный текст (или код)
   - Рисунки/графика
5. ✅ Распознает ВСЕ элементы на листе с высокой точностью

---

# Phase 2: Document Detection & Segmentation

**Цель:** Автоматическое выделение листа и классификация контента

## Week 1-2: Document Detection (Выделение листа)

### Milestone 2.1: Детекция углов листа бумаги

**Задачи:**

1. **Детекция контуров (Edge Detection)**
   - Использовать Canny edge detection
   - Морфологические операции для улучшения контуров
   - Реализовать `detect_paper_contours(image) -> contours`

2. **Поиск четырехугольника (Quad Detection)**
   - Аппроксимация контуров полигонами
   - Фильтрация по площади (лист должен занимать 20-80% кадра)
   - Поиск четырехугольника с наибольшей площадью
   - Реализовать `find_paper_quad(contours) -> corners[4]`

3. **Валидация углов**
   - Проверка что углы образуют выпуклый четырехугольник
   - Проверка минимальной/максимальной площади
   - Проверка соотношения сторон (A4: 1.414)
   - Реализовать `validate_paper_corners(corners) -> bool`

4. **Визуализация для отладки**
   - Рисование найденных контуров
   - Отметка углов листа
   - Отображение в реальном времени
   - Реализовать `visualize_detection(image, corners) -> annotated_image`

**Технологии:**
- OpenCV: `cv2.Canny()`, `cv2.findContours()`, `cv2.approxPolyDP()`
- NumPy для геометрических вычислений

**Файлы для создания:**
- `src/recognition_system/processing/document_detector.py`
- `src/recognition_system/processing/geometry_utils.py`
- `tests/unit/test_document_detection.py`

**Критерии успеха:**
- Детекция белого листа A4 на столе: 95%+ точность
- Работа при различном освещении
- Обработка листа под углом до 45°

---

### Milestone 2.2: Перспективная трансформация (Perspective Transform)

**Задачи:**

1. **Вычисление матрицы трансформации**
   - Определение целевых координат (прямоугольный лист)
   - Вычисление матрицы гомографии
   - Реализовать `calculate_transform_matrix(src_corners, target_size) -> matrix`

2. **Применение трансформации**
   - Warp perspective для получения "сверху вниз"
   - Коррекция искажений от камеры
   - Стандартизация размера (например 2480x3508 для A4 300dpi)
   - Реализовать `apply_perspective_transform(image, matrix) -> warped_image`

3. **Улучшение качества**
   - Автоматическая коррекция яркости/контраста
   - Удаление теней
   - Бинаризация при необходимости
   - Реализовать `enhance_document(image) -> enhanced_image`

**Технологии:**
- OpenCV: `cv2.getPerspectiveTransform()`, `cv2.warpPerspective()`
- Adaptive histogram equalization (CLAHE)

**Файлы для создания:**
- `src/recognition_system/processing/perspective_transform.py`
- `src/recognition_system/processing/image_enhancement.py`

**Критерии успеха:**
- Прямоугольный лист из любого угла обзора
- Сохранение пропорций A4 (1:1.414)
- Четкое изображение без искажений

---

### Milestone 2.3: Интеграция в систему

**Задачи:**

1. **Модуль DocumentProcessor**
   ```python
   class DocumentProcessor:
       def process_frame(self, frame):
           corners = self.detect_corners(frame)
           if corners is not None:
               warped = self.apply_transform(frame, corners)
               enhanced = self.enhance(warped)
               return enhanced, corners
           return None, None
   ```

2. **Обновление main pipeline**
   - Добавить шаг детекции перед OCR
   - Сохранять координаты углов
   - Визуализация найденного листа
   - Кэширование углов между кадрами

3. **Обработка edge cases**
   - Лист не найден → использовать весь кадр (fallback)
   - Несколько листов → выбрать наибольший
   - Частичное перекрытие → работать с видимой частью

**Файлы для модификации:**
- `simple_prototype.py` → добавить DocumentProcessor
- `config.yaml` → добавить параметры детекции

---

## Week 3-4: Content Segmentation & Classification

### Milestone 2.4: Сегментация контента на листе

**Задачи:**

1. **Детекция регионов (Region Detection)**
   - Connected Components Analysis для поиска регионов
   - Контурный анализ
   - Группировка близких элементов
   - Реализовать `detect_content_regions(image) -> List[Region]`

2. **Классификация регионов по типу**

   **a) Текст vs Не-текст:**
   - Анализ текстуры (variance, edges density)
   - Соотношение сторон bbox
   - Плотность пикселей

   **b) Рукописный vs Печатный:**
   - Вариативность толщины линий
   - Неровность baseline
   - Расстояние между символами

   **c) Код (моноширинный текст):**
   - Регулярное расстояние между символами
   - Специальные символы ({}, [], ;, =)
   - Отступы/выравнивание

   **d) Рисунок/графика:**
   - Отсутствие текстовых паттернов
   - Сложные контуры
   - Наличие замкнутых фигур

3. **ML классификатор**
   - Легковесная CNN для классификации региона
   - Или: использовать готовую модель (EfficientNet-lite)
   - Классы: `handwritten_text`, `printed_text`, `code`, `drawing`
   - Реализовать `ContentClassifier.classify(region) -> ContentType`

**Технологии:**
- OpenCV для feature extraction
- scikit-learn или TensorFlow Lite для классификации
- Возможно использовать EAST text detector как baseline

**Файлы для создания:**
- `src/recognition_system/ai/content_classifier.py`
- `src/recognition_system/processing/region_detector.py`
- `data/samples/` - датасет для обучения классификатора

**Критерии успеха:**
- Точность классификации >90%
- Скорость <500ms на всю страницу
- Работа с mixed content (текст + рисунки)

---

### Milestone 2.5: Специализированное распознавание

**Задачи:**

1. **Pipeline для каждого типа контента:**

   **a) Рукописный текст:**
   - EasyOCR с дополнительной постобработкой
   - Или использовать специализированную модель (TrOCR, GoogleVision API)
   - Реализовать `HandwritingRecognizer.recognize(region)`

   **b) Печатный текст / Код:**
   - Tesseract OCR (быстрее чем EasyOCR)
   - EasyOCR для кириллицы
   - Особая обработка для code (сохранение отступов)
   - Реализовать `TextRecognizer.recognize(region)`

   **c) Рисунки:**
   - Сохранение как image crop
   - Опционально: векторизация (potrace)
   - Извлечение метаданных (размер, позиция)
   - Реализовать `DrawingProcessor.process(region)`

2. **Unified recognition pipeline**
   ```python
   class ContentRecognizer:
       def recognize_document(self, document_image):
           regions = self.detect_regions(document_image)
           results = []
           for region in regions:
               content_type = self.classify(region)
               if content_type == 'handwritten_text':
                   text = self.handwriting_recognizer.recognize(region)
               elif content_type == 'printed_text':
                   text = self.text_recognizer.recognize(region)
               elif content_type == 'code':
                   text = self.code_recognizer.recognize(region)
               elif content_type == 'drawing':
                   data = self.drawing_processor.process(region)
               results.append({
                   'type': content_type,
                   'bbox': region.bbox,
                   'content': text or data,
                   'confidence': confidence
               })
           return results
   ```

**Файлы для создания:**
- `src/recognition_system/ai/handwriting_recognizer.py`
- `src/recognition_system/ai/text_recognizer.py`
- `src/recognition_system/ai/code_recognizer.py`
- `src/recognition_system/ai/drawing_processor.py`
- `src/recognition_system/core/content_recognizer.py`

---

## Week 5-6: ArUco Markers & Calibration

### Milestone 2.6: Улучшенная детекция с ArUco

**Зачем:** Более точная детекция углов листа + калибровка камер

**Задачи:**

1. **Создание ArUco маркеров**
   - Генерация 4 уникальных маркеров для углов
   - Печать на листе (углы A4)
   - Скрипт генерации: `scripts/generate_aruco_markers.py`

2. **Детекция ArUco маркеров**
   - Использовать `cv2.aruco.detectMarkers()`
   - Идентификация углов по ID маркера
   - Fallback на contour detection если маркеры не видны
   - Реализовать `ArUcoDetector.detect(image) -> corners`

3. **Калибровка камер**
   - Вычисление intrinsic/extrinsic параметров камеры
   - Устранение радиальных искажений
   - Сохранение calibration matrix
   - Реализовать `CameraCalibrator.calibrate()`

**Технологии:**
- OpenCV ArUco module
- Camera calibration с checkerboard pattern

**Файлы для создания:**
- `src/recognition_system/capture/aruco_detector.py`
- `src/recognition_system/capture/camera_calibrator.py`
- `scripts/generate_aruco_markers.py`
- `scripts/calibrate_cameras.py`

---

## Week 7-8: Stereo Vision & 3D Reconstruction

### Milestone 2.7: Стерео обработка

**Задачи:**

1. **Stereo matching**
   - Выравнивание изображений с двух камер (rectification)
   - Вычисление disparity map
   - Определение глубины для каждой точки

2. **3D реконструкция листа**
   - Построение 3D модели листа
   - Детекция складок/изгибов
   - Коррекция искажений от неровной поверхности

**Технологии:**
- OpenCV stereo matching
- Point cloud processing (Open3D)

**Файлы для создания:**
- `src/recognition_system/processing/stereo_processor.py`
- `src/recognition_system/processing/depth_estimator.py`

---

## Week 9-10: Integration & Optimization

### Milestone 2.8: Полная интеграция и оптимизация

**Задачи:**

1. **Создание v0.5.0 (Enhanced MVP)**
   - Объединить все модули
   - Полный pipeline: detection → transform → segmentation → recognition
   - Конфигурируемые режимы работы

2. **Оптимизация производительности**
   - GPU acceleration для всех этапов
   - Параллельная обработка регионов
   - Кэширование результатов
   - Цель: <3 секунды на полную обработку листа

3. **Улучшенный UI/CLI**
   - Real-time preview с визуализацией
   - Индикация этапов обработки
   - Статистика производительности

4. **Comprehensive testing**
   - Unit tests для всех модулей
   - Integration tests
   - End-to-end тесты с реальными данными

**Файлы для создания:**
- `enhanced_prototype.py` - новая версия с полным pipeline
- `src/recognition_system/core/pipeline.py` - унифицированный pipeline
- `tests/integration/test_full_pipeline.py`

---

# Technology Stack (Updated)

## Computer Vision
- OpenCV 4.x - базовая обработка изображений
- scikit-image - дополнительные алгоритмы

## OCR & Text Recognition
- EasyOCR - рукописный текст (русский, английский)
- Tesseract - печатный текст (быстрее)
- TrOCR (опционально) - улучшенное распознавание рукописного

## Machine Learning
- PyTorch / TensorFlow Lite - классификация контента
- scikit-learn - feature extraction, clustering
- Готовые модели: EfficientNet, MobileNet для классификации

## Geometry & 3D
- Open3D - point cloud processing
- NumPy - геометрические вычисления

## Utilities
- Pillow - image I/O
- matplotlib - визуализация для отладки

---

# Project Structure (Updated)

```
stereo-recognition/
├── simple_prototype.py              # v0.1.0 (current MVP)
├── enhanced_prototype.py            # v0.5.0 (target)
├── config.yaml
├── requirements.txt                 # updated dependencies
│
├── src/
│   └── recognition_system/
│       ├── core/
│       │   ├── pipeline.py          # Main processing pipeline
│       │   └── content_recognizer.py
│       ├── capture/
│       │   ├── camera_manager.py
│       │   ├── aruco_detector.py
│       │   └── camera_calibrator.py
│       ├── processing/
│       │   ├── document_detector.py # NEW: Paper detection
│       │   ├── perspective_transform.py # NEW
│       │   ├── region_detector.py   # NEW: Content segmentation
│       │   ├── image_enhancement.py
│       │   ├── geometry_utils.py
│       │   └── stereo_processor.py  # Future
│       ├── ai/
│       │   ├── content_classifier.py # NEW: Type classification
│       │   ├── handwriting_recognizer.py # NEW
│       │   ├── text_recognizer.py   # NEW
│       │   ├── code_recognizer.py   # NEW
│       │   └── drawing_processor.py # NEW
│       ├── storage/
│       │   └── result_exporter.py
│       └── utils/
│           ├── logger.py
│           └── profiler.py
│
├── tests/
│   ├── unit/
│   │   ├── test_document_detection.py
│   │   ├── test_perspective_transform.py
│   │   └── test_content_classification.py
│   └── integration/
│       └── test_full_pipeline.py
│
├── scripts/
│   ├── generate_aruco_markers.py
│   ├── calibrate_cameras.py
│   └── benchmark_performance.py
│
├── data/
│   ├── samples/                     # Test images
│   │   ├── handwritten/
│   │   ├── printed/
│   │   ├── code/
│   │   └── drawings/
│   ├── calibration/                 # Camera calibration data
│   └── models/                      # ML models (gitignored)
│
└── docs/
    ├── ARCHITECTURE.md
    ├── API.md
    └── PERFORMANCE.md
```

---

# Implementation Priorities

## Priority 1 (Must Have) - Week 1-2
- ✅ Document detection (corners)
- ✅ Perspective transformation
- ✅ Basic content segmentation

## Priority 2 (Should Have) - Week 3-4
- ✅ Content classification (ML)
- ✅ Specialized recognizers (handwriting, text, code, drawing)
- ✅ Enhanced output format

## Priority 3 (Nice to Have) - Week 5-6
- ArUco markers support
- Camera calibration
- Improved accuracy

## Priority 4 (Future) - Week 7+
- Stereo vision
- 3D reconstruction
- Real-time processing

---

# Performance Targets

## Current (v0.1.0)
- Full cycle: 5-10 seconds (CPU)
- OCR accuracy: 70-85% (handwritten)

## Target (v0.5.0)
- Document detection: <100ms
- Perspective transform: <50ms
- Content segmentation: <200ms
- OCR (per region): 500-1000ms
- **Total: <3 seconds per page**
- OCR accuracy: 90%+ (handwritten), 95%+ (printed)

---

# Success Criteria (v0.5.0)

## Document Detection
- [ ] Detects white A4 paper in 95%+ cases
- [ ] Works with angled paper (up to 45°)
- [ ] Handles various lighting conditions
- [ ] Fallback to full frame if no paper detected

## Content Recognition
- [ ] Classifies content types with 90%+ accuracy
- [ ] Handwritten text: 85%+ recognition accuracy
- [ ] Printed text/code: 95%+ recognition accuracy
- [ ] Preserves code formatting (indentation)
- [ ] Correctly identifies drawings vs text

## Performance
- [ ] Processes full page in <3 seconds
- [ ] Supports real-time preview (>10 FPS)
- [ ] GPU acceleration working
- [ ] Memory usage <2GB

## Usability
- [ ] Clear visual feedback (corners overlay)
- [ ] Detailed JSON output with content types
- [ ] Easy configuration
- [ ] Comprehensive documentation

---

# Development Workflow

## Phase 2.1 (Week 1-2)
1. Create `document_detector.py` with corner detection
2. Implement perspective transformation
3. Test with sample images
4. Integrate into main pipeline
5. Update documentation

## Phase 2.2 (Week 3-4)
1. Collect training data for classifier
2. Implement content segmentation
3. Train/integrate classifier
4. Create specialized recognizers
5. Test end-to-end

## Phase 2.3 (Week 5+)
1. Add ArUco support
2. Implement camera calibration
3. Optimize performance
4. Comprehensive testing
5. Release v0.5.0

---

# Dependencies Update

**New packages needed:**
```txt
# Existing
opencv-python>=4.8.0
numpy>=2.2.0
easyocr>=1.7.0
pillow>=12.0.0
pyyaml>=6.0

# NEW for Phase 2
scikit-image>=0.22.0        # Advanced image processing
scikit-learn>=1.3.0         # ML utilities
pytesseract>=0.3.10         # Fast OCR for printed text
torch>=2.0.0                # ML framework (already installed)
torchvision>=0.15.0         # Vision models (already installed)

# Optional (for advanced features)
open3d>=0.17.0              # 3D processing (future)
transformers>=4.30.0        # TrOCR model (optional)
```

---

# Next Actions

## Immediate (Today/Tomorrow)
1. Review this plan
2. Approve prioritization
3. Setup development branch: `git checkout -b feature/document-detection`
4. Start with Milestone 2.1 (Document Detection)

## This Week
1. Implement corner detection
2. Add perspective transformation
3. Test with real paper samples
4. Create visualization for debugging

## This Month
1. Complete document detection (Week 1-2)
2. Complete content segmentation (Week 3-4)
3. Release v0.2.0 with document detection
4. Release v0.3.0 with content classification

---

**Questions to clarify:**
1. Нужна ли поддержка цветных листов (не только белых)?
2. Какие языки важны для распознавания кроме RU/EN?
3. Нужна ли векторизация рисунков или достаточно растра?
4. Критична ли скорость обработки (<3 сек) или можно больше?
5. Нужна ли поддержка формул (LaTeX OCR)?

---

**Status:** Plan Ready for Review
**Next:** Start implementation of Milestone 2.1
**ETA for v0.5.0:** 8-10 weeks
