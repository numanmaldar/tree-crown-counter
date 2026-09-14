# 🌳 Tree Crown Counter

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tree-crown-counter.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![DeepForest](https://img.shields.io/badge/model-DeepForest-green.svg)](https://deepforest.readthedocs.io/)

A working, accessible tool to detect, count, and estimate the canopy area of individual tree crowns from high-resolution satellite imagery or KML files. Built for transparency and usability in ecological monitoring and carbon market applications.

**🔗 Live Demo:** [tree-crown-counter.streamlit.app](https://tree-crown-counter.streamlit.app/)

## 🚀 Features
- **Automated Detection:** Uses the pre-trained DeepForest model to identify individual tree crowns in RGB satellite imagery.
- **Canopy Area Estimation:** Calculates approximate canopy coverage based on detected bounding boxes.
- **Interactive Visualization:** Overlays detection results directly on the uploaded imagery for visual verification.
- **Exportable Results:** Download counts, area estimates, and geospatial data (GeoJSON/KML) for further analysis.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (for a zero-friction, user-friendly web interface)
- **Core ML:** PyTorch, DeepForest (pre-trained weights)
- **Geospatial Processing:** GDAL, GeoPandas, Rasterio
- **Deployment:** Streamlit Community Cloud

## 💻 Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/numanmaldar/tree-crown-counter.git
   cd tree-crown-counter
2. Create and activate a virtual environment (Python 3.11 recommended):
   ```bash
    python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install system dependencies (Ubuntu/Debian):
   ```bash
    sudo apt-get update
   sudo apt-get install -y $(cat packages.txt)
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   
##⚠️ Known Limitations (Read Before Use)
In carbon markets, a rough tool that admits what it can't do is more valuable than a polished one that invents numbers. This tool has the following limitations:

-**Resolution Dependency**: Accuracy is highly dependent on the Ground Sample Distance (GSD) of the input imagery. Imagery below 10cm/pixel will yield poor results.
-**Area Estimation is Approximate**: Without explicit georeferencing metadata (GSD) in the uploaded image, area calculations are pixel-based estimates, not precise real-world square meters.
-**Occlusion & Overlap**: Dense canopies with heavy overlapping crowns may be undercounted, as the model detects distinct bounding boxes.
-**CPU Inference**: The live demo runs on CPU. Processing large, high-resolution tiles may take 1–3 minutes. For production, GPU acceleration is required.

Built by Numan Maldar
   
