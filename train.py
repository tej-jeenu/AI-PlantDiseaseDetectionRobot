from ultralytics import YOLO
#from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO("yolov8s.pt")
#model = YOLO("best copy.pt")
model.train(data="datasets\yoloplantdataset\data.yaml", epochs=5, imgsz=640, workers=8, batch=16)
#results = model.predict(source="flowervid.mp4", show=True)

#print(results)
