# 5×STS Test (Sit‑to‑Stand) using Computer Vision

A cross‑platform sit‑to‑stand (5×STS) test application using MediaPipe and OpenCV (Python) or MediaPipe.js (HTML/JavaScript). It allows you to:

* **Calibrate** a user’s seated hip angle (2 s delay + 3 s recording)
* **Count** full sit‑to‑stand cycles (stand → sit) exactly 5 times
* **Time** from the start of the “Go” cue to the completion of the 5th sit
* **Provide** an audio‑visual countdown (Ready → 3,2,1 → Go) with customizable timing
* **Display** live hip angle, thresholds, rep count, and final time overlay

---

## Features

### Python Desktop Version

* Uses **OpenCV** & **MediaPipe Holistic** for pose detection
* Supports camera sources by index or device name (e.g. `video=My Camera`)
* Calibration routine with 2 s prep + 3 s sampling of seated hip angle
* Audio cues via **winsound** (Windows) or **playsound** cross‑platform
* High‑resolution font overlays for crisp text

### Browser Version (HTML/JS)

* Uses **MediaPipe Pose JS SDK** & WebRTC for camera
* Runs in any modern browser (Chrome, Edge, Safari) over **HTTPS**
* Camera selection dropdown for multiple inputs
* Audio via Web Audio API; canvas UI renders angle & results

---

## Repository Layout

```
/               # root
├── README.md    # this file
├── index.html   # HTML file for running in the web browser
├── Python/      # Python desktop version
│   ├── sit_to_stand.py
│   ├── list_cameras.py
└── html/        # Browser version
    ├── 5TSTS.html
    └── assets/  # optional styles or scripts
```

---

## Python Version

### Setup

```bash
cd python
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Usage

1. *(Optional)* List cameras:

   ```bash
   python list_cameras.py
   ```

   Copy the exact device name or index.

2. Edit `sit_to_stand.py` parameters:

   * `VIDEO_SOURCE`: camera index or `"video=Device Name"`
   * `SMOOTH_WINDOW`, `CALIB_DURATION`, `SIT_MARGIN`

3. Run:

   ```bash
   python sit_to_stand.py
   ```

4. Controls:

   * **C**: hip joint angle calibration in sitting position (wait 2 s prep + 3 s sit)
   * **S**: start countdown and begin timing at Go onset
   * **Q**: quit

---

## Browser Version

### Hosting on GitHub Pages (HTTPS)

1. Move `index.html` and `assets/` into the repository root (or `/docs`).
2. In GitHub **Settings > Pages**, set **Source** to `main` branch and folder `/ (root)` or `/docs`.
3. Visit `https://<username>.github.io/<repo>/` to run the test in-browser.

### Usage

* Allow camera access in the browser prompt.
* Press **C** (or tap) to begin calibration for the hip joint angle in sitting position after 2 s delay.
* Press **S** (or tap) to trigger countdown and start test immediately at “Go.”

---

## 5×STS Test Procedure

Follow these steps to administer the 5‑times sit‑to‑stand test:

1. **Setup**

   * Use a standard armless chair (seat height \~43‑46 cm) placed against a wall to prevent slipping.
   * Ask the participant to sit in the middle of the chair with feet flat on the floor, shoulder‑width apart.
   * Cross arms over chest (avoid using hands to push off).
   * Position the camera to capture the **LEFT SIDE** of the body for optimal hip and knee angle measurement.

2. **Calibration**

   * Press **C** to begin calibration.
   * Remain seated for 2 s (prep), then hold seated position for 3 s.
   * The system records your natural hip angle to set the sit threshold.

3. **Countdown**

   * Press **S** to start the audio‑visual countdown (Ready → 3 → 2 → 1 → Go).
   * Timing begins immediately when “Go” appears.

4. **Perform Test**

   * On the “Go” cue, stand up fully and then sit down completely.
   * Repeat this stand‑sit cycle **5** times as quickly as possible.

5. **Completion**

   * Test ends when participant sits after the 5th stand.
   * Elapsed time from “Go” to final sit is displayed as “Last Time.”

6. **Repeat**

   * To rerun, press **C** to re‑calibrate, then **S** to start a new trial.

---

## Troubleshooting

* **Black or frozen frames**: ensure no other app locks the camera; try opening by device name:

  ```python
  cv2.VideoCapture("video=Your Camera Name", cv2.CAP_DSHOW)
  ```
* **Camera permission denied**: serve HTML over **HTTPS** and enable camera in browser settings.
* **Angle jitter**: increase `SMOOTH_WINDOW` or filter by consecutive frames.
* **Cue display too brief**: adjust timing values in `cues` array or pause duration in `playCountdown()`.

---

## License

Copyright (c) 2025 Bokkyu Kim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to use, copy, modify, and distribute the Software for **non-commercial purposes only**. Commercial sale or distribution of the Software, in whole or in part, is strictly prohibited without prior written permission from the copyright holder.
