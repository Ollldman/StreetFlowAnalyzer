# StreetFlow Analyzer 🚗🚚

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1-red)](https://pytorch.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-8.0.196-green)](https://ultralytics.com)
[![Poetry](https://img.shields.io/badge/Poetry-Managed-orange)](https://python-poetry.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**StreetFlow Analyzer** — An intelligent traffic analysis system powered by computer vision. Uses YOLOv8 for vehicle detection and generates comprehensive traffic analysis reports.

## 📋 Features

- 🔍 **Vehicle detection** (cars, trucks) with high accuracy
- 📊 **Traffic density analysis** across image zones
- ⚠️ **Congestion identification** and anomaly detection
- 📈 **Professional PDF report generation**
- 🧪 **Experiment mode** for testing and parameter tuning
- 📸 **Batch processing** of urban camera images
- 🚀 **GPU acceleration** support via PyTorch

## 🏗️ Project Structure

```
yolo_project/
├── data/                    # Input images directory
├── experiments/             # Experiment results and visualizations
├── report_output/           # Generated PDF reports
├── ttf/                    # Fonts for PDF generation
├── traffic_analyzer.py      # Main application script
├── pyproject.toml          # Poetry configuration
└── README.md               # Project documentation
```

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Poetry (dependency manager)
- CUDA-capable GPU (optional, for faster inference)

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/streetflow-analyzer.git
cd streetflow-analyzer
```

2. **Install Poetry (if not installed):**
```bash
curl -sSL https://install.python-poetry.org | python3 -
# or
pip install poetry
```

3. **Install dependencies with Poetry:**
```bash
poetry install
```

4. **Activate the virtual environment:**
```bash
poetry shell
```

### Alternative: Manual Installation

If you prefer not to use Poetry:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install torch==2.5.1 torchvision==0.20.1
pip install ultralytics==8.0.196 opencv-python==4.8.1.78
pip install tqdm==4.66.1 numpy==1.26.0 fpdf2==2.7.6
```

## 📦 Dependencies

Managed by Poetry in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = "^3.8"
torch = "2.5.1"
torchvision = "0.20.1"
ultralytics = "8.0.196"
opencv-python = "4.8.1.78"
tqdm = "4.66.1"
numpy = "1.26.0"
fpdf2 = "2.7.6"
Pillow = "^10.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"
flake8 = "^6.0.0"
jupyter = "^1.0.0"
```

## 🚀 Usage

### Basic Usage

```bash
# Generate traffic analysis report
poetry run python traffic_analyzer.py --mode report --input data/ --output report_output/
```

### Experiment Mode (Debug & Testing)

```bash
# Run in experiment mode to visualize detections
poetry run python traffic_analyzer.py --mode experiment --input data/ --exp experiments/
```

### Advanced Options

```bash
poetry run python traffic_analyzer.py \
  --mode report \
  --input data/images/ \
  --output reports/ \
  --model yolov8n.pt \
  --confidence 0.5 \
  --zones 3 \
  --iou 0.45 \
  --device cuda:0
```

## 📊 Command Line Arguments

| Argument | Description | Default | Options |
|----------|-------------|---------|---------|
| `--mode` | Operation mode | `report` | `experiment`, `report` |
| `--input` | Input images directory | `data/` | Path string |
| `--output` | Output directory for reports | `report_output/` | Path string |
| `--exp` | Experiment results directory | `experiments/` | Path string |
| `--model` | YOLO model to use | `yolov8n.pt` | Model path or name |
| `--confidence` | Detection confidence threshold | `0.5` | 0.0-1.0 |
| `--iou` | IOU threshold for NMS | `0.45` | 0.0-1.0 |
| `--zones` | Number of analysis zones | `4` | Integer |
| `--device` | Computation device | `cpu` | `cpu`, `cuda`, `cuda:0` |
| `--batch` | Batch size for processing | `8` | Integer |
| `--anomaly_threshold` | Vehicle count for anomaly detection | `10` | Integer |

## 🔧 Operation Modes

### 1. **Experiment Mode**
Perfect for development, testing, and visualization:
- Visual detection overlays
- Performance metrics
- Parameter tuning
- Debug visualizations

```bash
poetry run python traffic_analyzer.py --mode experiment --input test_images/
```

### 2. **Report Mode**
Production-ready batch processing:
- Batch image processing
- Statistical analysis
- PDF report generation
- Traffic pattern identification

```bash
poetry run python traffic_analyzer.py --mode report --input camera_feed/ --output daily_reports/
```

## 📈 Report Contents

Generated PDF reports include:

- **Executive Summary**: Key findings and alerts
- **Traffic Statistics**: Vehicle counts by type and zone
- **Density Heatmaps**: Visual representation of traffic density
- **Time-based Analysis**: Traffic patterns over time
- **Anomaly Detection**: Identified congestion points
- **Recommendations**: Traffic management suggestions
- **Technical Details**: Processing parameters and metrics

## 🧪 Technical Implementation

### Core Features

- **Adaptive Preprocessing**: Handles various lighting and weather conditions
- **Zone-based Analysis**: Divides images into regions for localized analysis
- **False Positive Filtering**: Spatial relationship analysis to reduce errors
- **Performance Optimization**: Batch processing and GPU acceleration
- **Modular Architecture**: Easy to extend and customize

### Model Configuration

```python
# Example model configuration
model = YOLO('yolov8n.pt')  # nano version for speed
# Alternatives: yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
```

## 🚀 Performance Tips

1. **Use GPU acceleration** when available:
   ```bash
   --device cuda:0
   ```

2. **Adjust batch size** based on available memory:
   ```bash
   --batch 16  # Increase for faster processing
   ```

3. **Choose appropriate model**:
   - `yolov8n.pt`: Fastest, lower accuracy
   - `yolov8x.pt`: Slowest, highest accuracy

4. **Optimize confidence threshold**:
   ```bash
   --confidence 0.3  # Lower for more detections
   --confidence 0.7  # Higher for fewer but more confident detections
   ```

## 🧪 Development

### Setting Up Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Code formatting
poetry run black traffic_analyzer.py

# Linting
poetry run flake8 traffic_analyzer.py
```

### Adding New Features

1. Create a feature branch:
   ```bash
   git checkout -b feature/new-detection-method
   ```

2. Install in development mode:
   ```bash
   poetry install
   ```

3. Test your changes:
   ```bash
   poetry run python -m pytest tests/
   ```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed reproduction steps
2. **Suggest Features**: Share your ideas for improvements
3. **Submit Pull Requests**:
   - Fork the repository
   - Create a feature branch
   - Add tests for new functionality
   - Ensure code follows PEP 8 guidelines
   - Update documentation as needed

### Contribution Guidelines

- Write clear, commented code
- Add tests for new features
- Update documentation
- Follow existing code style
- Keep pull requests focused on single features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Authors

- **[Ollldman]** - Lead Developer & Researcher
- **Ultralytics Team** - YOLOv8 framework
- **Contributors** - Everyone who helped improve this project

## 🙏 Acknowledgments

- **Ultralytics** for the amazing YOLOv8 framework
- **PyTorch Team** for the deep learning framework
- **OpenCV Community** for computer vision tools
- **All Open-Source Contributors** who made this possible

## 📚 Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)

## 🔗 Related Projects

- [YOLOv8 Official Repository](https://github.com/ultralytics/ultralytics)
- [Traffic Monitoring Systems](https://github.com/topics/traffic-analysis)
- [Computer Vision Utilities](https://github.com/topics/computer-vision)

---

⭐ **If you find this project useful, please give it a star on GitHub!**

---

**Need Help?** Open an issue or start a discussion in the repository. We're here to help!

**Found a Bug?** Please report it with detailed steps to reproduce.

**Want to Collaborate?** Check out the open issues or propose new features!
