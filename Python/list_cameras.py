import cv2

def list_cameras(max_index=10):
    """
    Attempts to open camera indices 0..max_index-1.
    Returns a list of indices that worked.
    """
    found = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # on Windows, use CAP_DSHOW
        if cap is None or not cap.isOpened():
            continue
        # Optional: grab a frame to be extra sure
        ret, _ = cap.read()
        if ret:
            found.append(i)
        cap.release()
    return found

if __name__ == "__main__":
    cams = list_cameras(8)
    if cams:
        print(f"Available camera indices: {cams}")
    else:
        print("No cameras detected.")

