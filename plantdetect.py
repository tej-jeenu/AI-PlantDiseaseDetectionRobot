from ultralytics import YOLO
#from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

#model = YOLO("yolov8s.pt")
model = YOLO("50epochplantmodel.pt")
#model.train(data="coco128.yaml", epochs=100, imgsz=640)

def extractclasses(word):
    identifiedclasses = []
    word = str(word)
    newword = ""
    classes = ['Apple Scab', 'Apple', 'Apple rust', 'Bell_pepper spot', 'Bell_pepper', 'Blueberry', 'Cherry', 'Corn Gray spot', 'Corn blight', 'Corn rust', 'Peach', 'Potato early blight', 'Potato late blight', 'Potato', 'Raspberry', 'Soyabean', 'Soybean', 'Squash Powdery mildew', 'Strawberry', 'Tomato Early blight', 'Tomato Septoria spot', 'Tomato bacterial spot', 'Tomato late blight', 'Tomato mosaic virus', 'Tomato yellow virus', 'Tomato', 'Tomato mold', 'Tomato two spotted spider mites', 'grape black rot', 'grape']
    newword = word.replace("tensor([","")
    newwordone = newword.replace("])","")
    newwordtwo = newwordone.replace(".","")
    numclasses = newwordtwo.split(",")
    for n in numclasses:
        n = int(n)
        identifiedclasses.append(classes[n])
    identifiedclasses = list(dict.fromkeys(identifiedclasses))
    return identifiedclasses

def sentimentanalysis(classes):
    classes = list(classes)
    sentimentlist = []
    diseases = ['Apple Scab', 'Apple rust', 'Bell_pepper spot', 'Corn Gray spot', 'Corn blight', 'Corn rust', 'Potato early blight', 'Potato late blight', 'Squash Powdery mildew', 'Tomato Early blight', 'Tomato Septoria spot', 'Tomato bacterial spot', 'Tomato late blight', 'Tomato mosaic virus', 'Tomato yellow virus', 'Tomato mold', 'Tomato two spotted spider mites', 'grape black rot']
    for c in classes:
        if(c in diseases):
            sentimentlist.append('Disease')
        else:
            sentimentlist.append('Healthy')
    return sentimentlist
    


classlist = []

while 1:
    result = model.predict(source="soyabean.jpg", show=True, conf=0.4)
    print(str(result[0].boxes.cls))
    classlist.extend(extractclasses(str(result[0].boxes.cls)))
    sentimentlist = sentimentanalysis(classlist)
    print(str(classlist))
    print(str(sentimentlist))
#print(model.model.names)



    
