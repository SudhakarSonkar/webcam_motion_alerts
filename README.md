# 🎥 Motion Detector with Email Alerts

This project uses **OpenCV** and **Python threading** to detect motion from your webcam.  
When motion is detected, the app **saves an image** of the frame and (optionally) **sends an email alert** with the image attached.  

---

## 🚀 Features
- Detects motion in real-time using your webcam.
- Draws bounding boxes around detected objects.
- Saves snapshot images whenever motion is detected.
- Sends email alerts with the snapshot attached (configurable).
- `DEBUG` mode to test without sending real emails.
- Logs all activity in `motion_log.txt`.

---

## 🛠 Tech Stack
- [OpenCV](https://opencv.org/) – motion detection and video processing.
- [Threading](https://docs.python.org/3/library/threading.html) – background email sending & cleanup.
- [smtplib](https://docs.python.org/3/library/smtplib.html) – for email sending.
- [logging](https://docs.python.org/3/library/logging.html) – activity logging.

---
