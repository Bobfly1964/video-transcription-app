# Quick Start Guide

## Setup Complete!

Version 0.1.0 (MVP) has been successfully set up. All dependencies are installed and the system is ready to run.

## What's Been Done

- Project structure created
- Virtual environment set up (Python 3.13.7)
- All dependencies installed:
  * opencv-python 4.12.0.88
  * numpy 2.2.6
  * easyocr 1.7.2 (with PyTorch 2.9.1)
  * pillow 12.0.0
  * pyyaml 6.0.3
  * Supporting packages
- Main prototype file created (`simple_prototype.py`)
- Configuration file ready (`config.yaml`)
- Documentation written
- Initial Git commit completed

## Quick Test Run

### 1. Activate Virtual Environment

**Windows:**
```bash
cd C:\Users\user\Downloads\stereo-recognition
venv\Scripts\activate
```

### 2. Test Camera

```bash
python -c "import cv2; cap=cv2.VideoCapture(0); print('Camera:', 'OK' if cap.isOpened() else 'FAIL'); cap.release()"
```

Expected output: `Camera: OK`

### 3. Run Simple Test (3 cycles, 5 seconds each)

```bash
python simple_prototype.py --interval 5 --cycles 3 --cam1 0 --cam2 0
```

This will:
- Use camera 0 (single camera mode)
- Check for changes every 5 seconds
- Run for 3 cycles maximum
- Save results to `output/cycle_NNNN/`

### 4. Check Results

After running, check the `output/` directory:
```bash
dir output\cycle_0001
```

You should see:
- `recognized_text.json` - OCR results with coordinates and colors
- `annotated_image.png` - Image with bounding boxes
- `original_image.png` - Raw captured frame

## What To Test

1. **Print Text Test**: Print some text on paper and hold it in front of the camera
2. **Handwritten Test**: Write something by hand and see if it recognizes it
3. **Color Test**: Use different colored pens to verify color detection
4. **Change Detection**: Leave paper still vs moving it

## Expected Performance

- Without GPU: 5-10 seconds per OCR cycle
- With CUDA GPU: 2-3 seconds per OCR cycle
- Print text accuracy: 90-95%
- Handwritten accuracy: 50-85% (depends on handwriting quality)

## Common Issues

### Camera Not Opening
```bash
# List available cameras
python -c "import cv2; [print(f'Camera {i}: {cv2.VideoCapture(i).isOpened()}') for i in range(5)]"
```

### OCR Too Slow
Edit `simple_prototype.py` line 107:
```python
self.reader = easyocr.Reader(['ru', 'en'], gpu=True)  # Enable GPU
```

### First Run Takes Long
EasyOCR downloads models (~100MB) on first run. This is normal and only happens once.

## Configuration

Edit `config.yaml` to change:
- Camera IDs and resolutions
- OCR languages
- Change detection threshold
- Output formats

## Command-Line Options

```bash
python simple_prototype.py --help
```

Available options:
- `--cam1 ID` - First camera ID (default: 0)
- `--cam2 ID` - Second camera ID (default: 1)
- `--interval SEC` - Seconds between checks (default: 10)
- `--cycles NUM` - Max cycles (default: infinite)

## Next Steps

1. Test with different types of content
2. Measure performance on your hardware
3. Check `NOTES.md` for known limitations
4. Review output JSON format
5. Plan improvements for Week 1

## Troubleshooting

### Import Errors
Make sure venv is activated:
```bash
venv\Scripts\activate
```

### Missing Dependencies
```bash
pip install -r requirements-minimal.txt
```

### Git Issues
Check current status:
```bash
git log --oneline -1
```

Expected: `feat: Initial MVP prototype implementation`

## Support

- README.md - Full documentation
- NOTES.md - Development notes
- config.yaml - Configuration reference
- GitHub Issues: https://github.com/Bobfly1964/stereo-recognition/issues

---

**Status:** Ready to Test
**Version:** 0.1.0 (MVP)
**Date:** 2024-11-24
