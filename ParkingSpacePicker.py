import cv2
import pickle
from pathlib import Path

width, height = 107, 48

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
PARKING_POS_PATH = BASE_DIR / "CarParkPos"
IMAGE_PATH = PROJECT_DIR / "OUTPUT_IMAGES" / "Marking Spaces image.png"

try:
    with open(PARKING_POS_PATH, 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break

    with open(PARKING_POS_PATH, 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread(str(IMAGE_PATH))
    if img is None:
        raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
