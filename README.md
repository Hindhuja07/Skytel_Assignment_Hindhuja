Markdown

# 🚦 Smart Traffic Lane Counter

An AI-powered system for **lane-wise vehicle detection and counting** using **YOLOv8** for object detection and **SORT** for object tracking.  
This project automatically downloads a YouTube traffic video, detects cars, motorcycles, buses, and trucks, assigns them to lanes, and logs counts over time.

---

## 📌 Features
- **Automatic video download** from YouTube
- **Vehicle detection** using YOLOv8
- **Object tracking** using SORT algorithm
- **Lane assignment** based on polygon regions
- **CSV export** for vehicle counts with timestamps
- **Real-time display** with lane overlays and counts

---

## 📂 Project Structure

.
├── sort.py                # SORT tracker implementation
├── main.py                # Main script for video processing
├── requirements.txt       # Python dependencies
├── vehicle\_counts.csv     # Output CSV with results
└── README.md              # Documentation


---

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smart-traffic-lane-counter.git
cd smart-traffic-lane-counter

2. Create a virtual environment (recommended)

p
Bash

ython -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
3. Install dependencies

p
Bash

ip install -r requirements.txt
---

## 📦 Requirements

Add these to requirements.txt:

u
ltralytics
opencv-python
numpy
pandas
yt-dlp
filterpy
scikit-image
---

## ▶️ Usage

1. Run the main script

py
Bash

thon main.py

2. The script will:

   * Download the video from the given YouTube link
   * Detect and track vehicles
   * Assign vehicles to lanes
   * Display live processed video
   * Save results to vehicle_counts.csv

---

## 📊 Output Example

vehicle_counts.csv contains:

Ve
hicle_ID,Lane,Frame,Timestamp
1,1,15,0.50
2,2,20,0.67
3,3,35,1.17
...

---

## 🎯 Lane Configuration

Modify the lanes variable in main.py to match your road layout:

lan
Python

es = [
    [(x1,y1), (x2,y2), (x3,y3), (x4,y4)],  # Lane 1
    [(...), (...), (...), (...)],          # Lane 2
    [(...), (...), (...), (...)]           # Lane 3
]

-
--

## 📹 Example

!Traffic Analysis Example

---

## 🧠 How it Works

1. YOLOv8 detects vehicles frame-by-frame.
2. SORT tracker assigns consistent IDs to moving vehicles.
3. Polygon lane mapping checks which lane each vehicle is in.
4. Counts are updated only when a new vehicle ID is detected in a lane.
5. Data is saved for further analysis.

---

## 🚀 Future Improvements

* Support for multiple camera angles
* Lane auto-detection
* Speed estimation per vehicle
* Real-time traffic density prediction

---

## 📝 License

This project is licensed under the MIT License.


