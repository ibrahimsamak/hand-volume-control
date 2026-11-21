# Hand Volume Control

Control your Mac's volume by pinching your thumb and index finger in front of the webcam.

- Fingers close together to volume down
- Fingers far apart to volume up

## Run

```bash
cd ~/hand-volume-control
.venv/bin/python main.py
```

Press `q` to quit. The first time, macOS will ask for camera permission for your terminal — allow it.

## Setup from scratch

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
curl -L -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```
