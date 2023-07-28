import requests
import json
import time

URL = 'https://inf-f753c859-5a15-423b-8fd4-f3894505c9f8-no4xvrhsfq-uc.a.run.app/detect' 
FALLBACK_URL = 'https://inf-04ac9252-3e6e-466b-9a0b-73d331bcd6fd-no4xvrhsfq-uc.a.run.app/detect' 
IMAGE_PATH = 'img'

def detect(image_path, url=URL, conf_thres=0.25, iou_thres=0.45, ocr_model='large', ocr_classes='text', ocr_language=None, retries=10, delay=0):
    response = requests.post(url, data={'conf_thres':conf_thres, 'iou_thres':iou_thres, **({'ocr_model':ocr_model, 'ocr_classes':ocr_classes, 'ocr_language':ocr_language} if ocr_model is not None else {})}, files={'image':open(image_path, 'rb')})
    if response.status_code in [200, 500]:
        data = response.json()
        if 'error' in data:
            print('[!]', data['message'])
        else:
            return data  # Return the entire list of detections
    elif response.status_code == 403:
        print("Couldn't extract data.")
    elif retries > 0:
        if delay > 0:
            time.sleep(delay)
        return detect(image_path, url=FALLBACK_URL if FALLBACK_URL else URL, retries=retries-1, delay=2)
    return []

detections = detect(IMAGE_PATH)

if len(detections) > 0:
    for detection in detections:
        text = detection['text']
        print(text)
else:
    print('no objects found.')