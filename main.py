import os
import glob
import cv2
import time
from threading import Thread
import logging
from emailing import send_email

# Configure logging
logging.basicConfig(
    filename="motion_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1
image_with_object = None  # safe default


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    logging.info("🗑️ Cleaned up images folder")


while True:
    status = 0
    check, frame = video.read()
    if not check:
        logging.warning("⚠️ Camera frame not read correctly")
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau
        continue

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        status = 1
        image_path = f"images/{count}.png"
        cv2.imwrite(image_path, frame)
        count += 1
        all_images = glob.glob("images/*.png")
        index = int(len(all_images) / 2)
        image_with_object = all_images[index]
        logging.info(f"📸 Motion detected, saved {image_path}")

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0 and image_with_object:
        logging.info(f"📧 Triggering email with {image_with_object}")
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        email_thread.start()

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        clean_thread.start()

    cv2.imshow("My video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        logging.info("🛑 Program exited by user")
        break

video.release()
cv2.destroyAllWindows()
