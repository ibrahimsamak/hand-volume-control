import math
import subprocess
import time

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

detector = vision.HandLandmarker.create_from_options(
    vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
    )
)



cap = cv2.VideoCapture(0)
last_volume = -1

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect_for_video(image, int(time.time() * 1000))

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]

        x1, y1 = int(hand[4].x * w), int(hand[4].y * h)
        x2, y2 = int(hand[8].x * w), int(hand[8].y * h)

        cv2.circle(frame, (x1, y1), 25, (0, 0, 255), -1)
        cv2.circle(frame, (x2, y2), 25, (0, 0, 255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

        distance = math.hypot(x2 - x1, y2 - y1)
        volume = int(min(max((distance - 30) / 170 * 100, 0), 100))

        if abs(volume - last_volume) >= 2:
            subprocess.Popen(["osascript", "-e", f"set volume output volume {volume}"])
            last_volume = volume

        # cv2.putText(frame, f"Volume: {volume}%", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Hand Volume Control (press q to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
