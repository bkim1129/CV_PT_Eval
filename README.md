# 5×STS Test (Sit‑to‑Stand)

A cross‑platform sit‑to‑stand (5×STS) test application using MediaPipe and OpenCV (Python) or MediaPipe.js (HTML/JavaScript). It allows you to:

* **Calibrate** a user’s seated hip angle
* **Count** full sit‑to‑stand cycles (stand then sit) exactly 5 times
* **Time** the interval between the first stand and the fifth sit
* **Provide** an audio‑visual countdown (Ready → 3,2,1 → Go)
* **Display** live hip angle, thresholds, rep count, and result on screen

---

## Features

* **Python Desktop Version** (Windows, macOS, Linux)

  * Uses OpenCV & MediaPipe Holistic
  * Supports multiple camera sources via index or device name
  * Calibration routine with 2 s prep + 3 s recording
  * Audio cues via `winsound` or `playsound`
  * High‑resolution font overlays

* **Browser Version** (HTML/JS)

  * Uses MediaPipe Pose JS SDK & WebRTC API
  * Runs in any modern browser (Chrome, Edge, Safari)
  * HTTPS required for camera access
  * Camera selection dropdown
  * Audio cues via Web Audio API

---

## Repository Structure

```
├── sit_to_stand.py       # Main Python script
├── index.html            # Browser version
└── README.md             # Project README
```

---

## Python Version

### Requirements

* Python 3.7+
* OpenCV (`pip install opencv-python`)
* MediaPipe (`pip install mediapipe`)
* PyGrabber (for camera enumeration) (`pip install pygrabber`)
* (Windows) `winsound` is built‑in; on other platforms use `playsound`

### Installation

```bash
cd python
pip install -r requirements.txt
```

### Usage

1. **Enumerate cameras** (optional):

   ```bash
   python list_cameras.py
   ```

   Copy the exact device name or note the numeric index.

2. **Configure** `sit_to_stand.py`:

   * Set `VIDEO_SOURCE = 0` (or `"video=Your Device Name"` for named devices)
   * Adjust `SMOOTH_WINDOW`, `CALIB_DURATION`, `SIT_MARGIN` as needed

3. **Run**:

   ```bash
   python sit_to_stand.py
   ```

4. **Controls**:

   * Press `c` to start calibration (2 s prep + 3 s sitting)
   * Press `s` to play countdown and begin 5×STS test
   * Watch on‑screen reps, thresholds, and final time
   * Press `q` to quit

---

## Browser Version

### Prerequisites

* Host `html/index.html` over **HTTPS** (e.g. GitHub Pages, Netlify)
* Modern browser on desktop or mobile

### Usage

1. Deploy the `html/` folder to your HTTPS‑enabled web server.
2. Open the page (e.g. `https://<your-domain>/index.html`) in your browser.
3. Grant camera permission when prompted.
4. **Controls**:

   * Press **C** (or tap) to start calibration
   * Press **S** (or tap) for countdown + 5×STS
   * View live angle, rep count, and final result overlay

---

## Troubleshooting

* **Black or noisy frames**:

  * Ensure no other app is locking the camera
  * On Windows, consider opening by device name:

    ```python
    cap = cv2.VideoCapture("video=Your Device Name", cv2.CAP_DSHOW)
    ```

* **Camera permission denied**:

  * Serve HTML page over **HTTPS** and enable camera access
  * In Windows Settings → Privacy → Camera, allow access for desktop apps

* **Angle jitter**:

  * Increase `SMOOTH_WINDOW` or require multiple frames before state changes

---

## License

This project is open‑source under the MIT License.

---

## Acknowledgments

* [MediaPipe](https://mediapipe.dev) — Pose & Holistic tracking
* [OpenCV](https://opencv.org) — Real‑time computer vision
* Web Audio API & WebRTC for the browser version
