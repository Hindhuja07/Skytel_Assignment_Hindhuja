import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from sort import Sort  # Ensure you have SORT implementation
import yt_dlp

# ---------------- Video Download ----------------
url = "https://www.youtube.com/watch?v=MNn9qKG2UFI"
output_path = "traffic_video.mp4"

ydl_opts = {
    'format': 'mp4',
    'outtmpl': output_path,
    'noplaylist': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# ---------------- Load Detector & Tracker ----------------
model = YOLO('yolov8n.pt')  # YOLOv8 nano for speed
tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)

# ---------------- Define Lanes as Multiple Points ----------------
lanes = [
    # Lane 1: Multiple points
    [(7, 355), (213, 353),(246, 217), (250, 125), (227, 56), (211, 14),(182, 15),(168, 91),(113, 176),(6, 309),(7, 355)],

    # Lane 2: Middle lane
    [(248, 355), (371, 358),(362, 259), (342, 180), (321, 120),(296, 87),(272, 53),(236, 16),(220, 20),(232, 46),(247, 75),(269, 110), (277, 192),(271, 280),(248, 355)],

    # Lane 3: Rightmost merging lane
    [(387, 357), (540, 358), (561, 280),(582, 239), (616, 208),(637, 189),(617, 145),(560, 170),(513, 196),(466, 232),(416, 293),(387, 357)]
]

# ---------------- Function to Check if Point is Near Lane Line ----------------
def point_near_lane(point, lane_points, threshold=30):
    # Check distance from point to each segment in the lane polyline
    for i in range(len(lane_points) - 1):
        p1 = lane_points[i]
        p2 = lane_points[i + 1]
        dist = cv2.pointPolygonTest(np.array([p1, p2]), point, True)
        if abs(dist) <= threshold:  # Close enough to the lane line
            return True
    return False

# ---------------- Initialize Variables ----------------
vehicle_lane = {}  # vehicle_id -> lane
vehicle_count = [0, 0, 0]
output_data = []

cap = cv2.VideoCapture(output_path)
frame_id = 0
fps = cap.get(cv2.CAP_PROP_FPS)

# COCO class IDs for vehicles
vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_id += 1

    # Detect vehicles
    results = model(frame)[0]
    dets = []
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        if int(cls) in vehicle_classes:  # Only vehicle classes
            x1, y1, x2, y2 = box
            dets.append([x1, y1, x2, y2, 1.0])  # SORT requires score

    if len(dets) > 0:
        dets = np.array(dets)
        tracked_objects = tracker.update(dets)
    else:
        tracked_objects = []

    # Assign lanes and counts
    for x1, y1, x2, y2, track_id in tracked_objects:
        cx, cy = int((x1 + x2)/2), int((y1 + y2)/2)
        lane_assigned = None
        for idx, lane in enumerate(lanes):
            if point_near_lane((cx, cy), lane):
                lane_assigned = idx
                break
        if lane_assigned is not None:
            if track_id not in vehicle_lane:
                vehicle_lane[track_id] = lane_assigned
                vehicle_count[lane_assigned] += 1
            timestamp = frame_id / fps
            output_data.append([int(track_id), lane_assigned+1, frame_id, round(timestamp, 2)])

        # Draw bounding boxes
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'ID:{int(track_id)}', (int(x1), int(y1)-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Draw lane polylines and counts
    for idx, lane in enumerate(lanes):
        cv2.polylines(frame, [np.array(lane, np.int32)], False, (255, 0, 0), 3)
        cv2.putText(frame, f'Lane {idx+1}: {vehicle_count[idx]}', lane[0],
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Traffic Analysis", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# ---------------- Save CSV ----------------
df = pd.DataFrame(output_data, columns=['Vehicle_ID', 'Lane', 'Frame', 'Timestamp'])
df.to_csv('vehicle_counts.csv', index=False)

# ---------------- Print Summary ----------------
for i, count in enumerate(vehicle_count):
    print(f"Total vehicles in Lane {i+1}: {count}")
