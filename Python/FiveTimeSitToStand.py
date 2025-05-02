import cv2
import time
import numpy as np
from collections import deque
import winsound            # Windows only!
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont

# ─── PARAMETERS ────────────────────────────────────────────────────────────────
SMOOTH_WINDOW    =   5     # frames for median filter
REP_GOAL         =   5     # 5×STS
STAND_THRESHOLD  = 160     # standing when angle > this
CALIB_DURATION   =   3.0   # seconds to record sitting posture
SIT_MARGIN       =   5.0   # degrees above your seated angle

# ─── AUDIO CUES ────────────────────────────────────────────────────────────────
CUES = [
    ('Ready',  1000, 1000),
    ('3',       800,  400),
    ('2',       800,  400),
    ('1',       800,  400),
    ('Go',     1500,  400),
]

# ─── FONTS ─────────────────────────────────────────────────────────────────────
# TrueType for numbers and degree
TTF_PATH         = "C:/Windows/Fonts/arial.ttf"  # adjust as needed
ANGLE_FONT_SIZE  = 48
UI_FONT_SIZE     = 24

angle_font_ttf = ImageFont.truetype(TTF_PATH, ANGLE_FONT_SIZE)
ui_font_ttf    = ImageFont.truetype(TTF_PATH, UI_FONT_SIZE)

# OpenCV fonts for other UI
UI_FONT   = cv2.FONT_HERSHEY_COMPLEX
UI_SCALE  = 1.0
UI_THICK  = 3

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def calculate_angle(a, b, c):
    a, b, c = map(np.array, (a, b, c))
    rad = ( np.arctan2(c[1]-b[1], c[0]-b[0])
          - np.arctan2(a[1]-b[1], a[0]-b[0]) )
    deg = abs(rad * 180.0 / np.pi)
    return 360 - deg if deg > 180 else deg

def play_countdown(win, shape):
    h, w = shape
    blank = np.zeros((h, w, 3), np.uint8)
    for text, freq, dur in CUES:
        winsound.Beep(freq, dur)
        t0 = time.time()
        while time.time() - t0 < dur/1000.0:
            frame = blank.copy()
            ts, _ = cv2.getTextSize(text, UI_FONT, 4.0, 8)
            org = ((w - ts[0])//2, (h + ts[1])//2)
            cv2.putText(frame, text, org, UI_FONT, 4.0, (255,255,255), 8, cv2.LINE_AA)
            cv2.imshow(win, frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                return

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    mp_drawing  = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic
    mp_pose     = mp.solutions.pose

    angle_buf     = deque(maxlen=SMOOTH_WINDOW)
    state         = None
    test_on       = False
    reps          = 0
    t_start       = None
    finish_pending= False

    # calibration flags
    calibrated               = False
    calibrating              = False
    calibration_requested    = False
    calibration_request_time = None
    calib_buf                = deque(maxlen=int(CALIB_DURATION*30))
    calib_start              = None
    SIT_THRESHOLD            = None

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    ret, tmp = cap.read()
    h, w = tmp.shape[:2]
    win = "5×STS Test"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)

    with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hol:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 2s delay before calibration actually starts
            if calibration_requested and not calibrating:
                if time.time() - calibration_request_time >= 2.0:
                    calibrating           = True
                    calibration_requested = False
                    calib_buf.clear()
                    calib_start           = time.time()
                    print("Calibration started…")

            # pose processing
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            res = hol.process(rgb)
            rgb.flags.writeable = True
            vis = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            # draw skeleton
            if res.pose_landmarks:
                mp_drawing.draw_landmarks(
                    vis, res.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

            # compute hip angle
            smooth = None
            hip_pt = (0,0)
            try:
                lm = res.pose_landmarks.landmark
                A = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                     lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
                B = [lm[mp_pose.PoseLandmark.LEFT_HIP].x,
                     lm[mp_pose.PoseLandmark.LEFT_HIP].y]
                C = [lm[mp_pose.PoseLandmark.LEFT_KNEE].x,
                     lm[mp_pose.PoseLandmark.LEFT_KNEE].y]

                ang = calculate_angle(A, B, C)
                angle_buf.append(ang)
                smooth = float(np.median(angle_buf))
                hip_pt = (int(B[0]*w), int(B[1]*h))

                # handle calibration collection
                if calibrating:
                    calib_buf.append(smooth)
                    elapsed = time.time() - calib_start
                    cv2.putText(vis,
                        f"Calibrating {elapsed:.1f}/{CALIB_DURATION}s",
                        (10, h-20),
                        UI_FONT, UI_SCALE, (0,255,255),
                        UI_THICK, cv2.LINE_AA)
                    if elapsed >= CALIB_DURATION:
                        default = float(np.median(calib_buf))
                        SIT_THRESHOLD = default + SIT_MARGIN
                        calibrating  = False
                        calibrated   = True
                        print(f"Calibrated sit: {default:.1f}°, SIT_THRESHOLD={SIT_THRESHOLD:.1f}°")

                # rep counting
                if calibrated and not calibrating:
                    if smooth > STAND_THRESHOLD and state != 'stand':
                        state = 'stand'
                        if test_on:
                            reps += 1
                            if reps == 1:
                                t_start = time.time()
                            if reps == REP_GOAL:
                                finish_pending = True

                    elif smooth < SIT_THRESHOLD and state != 'sit':
                        state = 'sit'
                        if finish_pending and test_on:
                            total = time.time() - t_start
                            print(f"5×STS complete in {total:.2f}s")
                            test_on        = False
                            finish_pending = False

            except:
                pass

            # draw UI background
            cv2.rectangle(vis, (0,0), (400,130), (0,0,0), -1)

            # convert to PIL for angle + SIT_THRESHOLD
            pil = Image.fromarray(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil)

            if smooth is not None:
                angle_text = f"{int(smooth)}°"
                draw.text(hip_pt, angle_text, font=angle_font_ttf, fill=(255,255,255))

            if calibrated:
                th_text = f"SIT_THRESH: {SIT_THRESHOLD:.1f}°"
                draw.text((10,10), th_text, font=ui_font_ttf, fill=(200,200,200))

            # back to OpenCV
            vis = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)

            # remaining UI overlays
            if not calibrated:
                msg = "Calibration in 2s" if calibration_requested else "Press 'c' to calibrate"
                cv2.putText(vis, msg, (10,65),
                            UI_FONT, UI_SCALE, (255,255,255),
                            UI_THICK, cv2.LINE_AA)
            else:
                cv2.putText(vis, "Press 's' to start", (10,65),
                            UI_FONT, UI_SCALE, (255,255,255),
                            UI_THICK, cv2.LINE_AA)
                cv2.putText(vis, f"Reps: {reps}/{REP_GOAL}", (10,100),
                            UI_FONT, UI_SCALE, (255,255,255),
                            UI_THICK, cv2.LINE_AA)
                if test_on:
                    cv2.putText(vis, "Test ACTIVE", (250,65),
                                UI_FONT, UI_SCALE, (0,255,0),
                                UI_THICK, cv2.LINE_AA)

            cv2.imshow(win, vis)
            key = cv2.waitKey(10) & 0xFF

            if key == ord('c') and not calibrating and not calibration_requested:
                calibration_requested    = True
                calibration_request_time = time.time()
                calibrated               = False
                print("Calibration will start in 2 s…")

            if key == ord('s') and calibrated and not test_on:
                play_countdown(win, (h, w))
                test_on        = True
                reps           = 0
                finish_pending = False
                print("5×STS test started")

            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
