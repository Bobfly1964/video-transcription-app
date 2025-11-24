# Development Notes

## Setup Session - 2024-11-24

### Initial Setup

- Created project structure with proper directory layout
- Created MVP prototype `simple_prototype.py`
- Set up configuration files
- Created comprehensive documentation

### Python Version Issue

**Problem:** Initially attempted to use Python 3.14 (alpha), which caused compatibility issues:
- numpy 2.2.6+ fails to build on Python 3.14 due to stdalign.h missing
- scikit-image requires compilation which fails on Python 3.14
- EasyOCR dependencies not available for Python 3.14

**Solution:** Switched to Python 3.13.7 which has prebuilt wheels for all dependencies

### Dependencies Installed

Successfully installed all required packages:
- opencv-python 4.12.0.88
- numpy 2.2.6
- pillow 12.0.0
- pyyaml 6.0.3
- easyocr 1.7.2 (with torch 2.9.1, torchvision 0.24.1)
- python-dateutil, tqdm, colorama

### Camera Check

- Camera 0 is available and working

### Next Steps

1. Test run `simple_prototype.py` with actual camera
2. Test OCR with handwritten text samples
3. Measure performance (FPS, OCR speed)
4. Document issues and improvements needed

### Known Limitations (MVP v0.1.0)

1. **OCR Speed**: EasyOCR without GPU is ~5-10 sec per frame
2. **Change Detection**: Simple threshold-based (2%), may need tuning
3. **Camera Merge**: Simple weighted average, not optimal for stereo
4. **No Calibration**: Camera calibration not implemented yet

### Recommendations for Week 1

1. Add GPU support check and enable if available
2. Implement better change detection (motion detection)
3. Add logging to file
4. Create unit tests for core functions
5. Measure and optimize performance

### File Structure

```
stereo-recognition/
├── .gitignore              ✓ Created
├── README.md               ✓ Created
├── requirements-minimal.txt ✓ Created
├── simple_prototype.py     ✓ Created
├── config.yaml             ✓ Created
├── NOTES.md                ✓ Created
├── venv/                   ✓ Created (Python 3.13.7)
├── src/                    ✓ Created (empty, for future)
├── tests/                  ✓ Created (empty, for future)
├── config/                 ✓ Created
├── scripts/                ✓ Created
├── docs/                   ✓ Created
├── examples/               ✓ Created
├── data/                   ✓ Created
└── output/                 ✓ Created (gitignored)
```

### Git Status

Ready for initial commit with all MVP files.
