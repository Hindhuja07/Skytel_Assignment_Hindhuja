import cv2

# ----------- Load Video and Grab a Frame -----------
video_path = "traffic_video.mp4"  # Replace with your downloaded video path
cap = cv2.VideoCapture(video_path)

frame_number = 100  # Choose which frame to pause on (adjust as needed)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from video.")
    cap.release()
    exit()

img = frame.copy()
clone = img.copy()

points = []

# ----------- Mouse Callback Function -----------
def click_event(event, x, y, flags, param):
    global points, img

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point: ({x}, {y})")
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        # Draw line connecting points
        if len(points) > 1:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 2)

        cv2.imshow("Select Points", img)

cv2.imshow("Select Points", img)
cv2.setMouseCallback("Select Points", click_event)

print("Click on points for each lane (in order).")
print("Press 'r' to reset, 'q' to quit and print all points.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        img = clone.copy()
        points = []
        cv2.imshow("Select Points", img)
        print("Reset points.")
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

print("\n✅ Final selected points:")
for p in points:
    print(p)
