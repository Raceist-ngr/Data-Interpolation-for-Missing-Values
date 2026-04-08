# Data-Interpolation-for-Missing-Values# 📈 DataFill — Interpolation Studio
### Numerical Methods College Project

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
.
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── sample_weather_data.csv  # Sample dataset for testing
└── README.md
```

---

## 🎯 How to Use

1. **Upload CSV** — Click the file uploader and select your CSV file  
   *(or download the included sample CSV to try immediately)*

2. **Review the dataset** — Missing values are highlighted in **rose/red**

3. **Choose a method** from the sidebar:
   - **Linear** — straight-line interpolation between known values
   - **Polynomial (order=2)** — smooth parabolic curve fit

4. **Select column** — interpolate a single column or all at once

5. **Run Interpolation** — click the button to apply

6. **View results** — filled cells highlighted in **teal**, plus Before/After charts

7. **Export** — download the cleaned CSV

---

## ⚙️ Interpolation Methods

| Method | Description | Best For |
|--------|-------------|----------|
| Linear | Connects neighboring known values with a straight line | Gradual, monotonic data |
| Polynomial (n=2) | Fits a smooth parabola through surrounding points | Curved trends, sensor data |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `pandas` | Data loading and interpolation |
| `numpy` | Numeric operations |
| `plotly` | Interactive before/after charts |

---

## 💡 Tips

- Your CSV should use **blank cells** or the text `NaN` to represent missing values
- Interpolation only works on **numeric columns**
- Edge-case NaNs (at the very start/end of a column) are filled by extending the nearest known value
- The polynomial method may diverge on very sparse data — linear is safer in that case
