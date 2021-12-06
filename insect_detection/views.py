from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import random
from django.contrib.staticfiles.storage import staticfiles_storage

confThreshold = 0.01
nmsThreshold = 0.01 
cfg = staticfiles_storage.path("yolov4-custom.cfg") 
weights = staticfiles_storage.path("yolov4-custom_1400.weights")
net = cv2.dnn.readNetFromDarknet(cfg, weights)
classes = ['aphides','catepillars','mealy_bug', 'mites', 'stem_borer', 'thrips']


# Create your views here.
def index(request):

    if request.method == 'POST':
        form = InsectImageForm(request.POST, request.FILES)
        # img_file = form.cleaned_data['name']
        # print(img_file)
        if form.is_valid():
            form.save()
            # query = "select max(id) from insect_detection_insect_images where 1 = 1"
            predict_insects(request)
            img = Insect_Images.objects.all()
            img = img[len(img) - 1]
            return redirect("display_prediction")
    else:
        form = InsectImageForm()
    return render(request, 'index.html', {'form' : form, 'btn' : 'PREDICT'})

def display_prediction(request):
    img = Insect_Images.objects.all()
    img = img[len(img) - 1]
    return render(request, 'display_prediction.html', {'image' : img})

def predict_insects(request):
    counts = [0 for i in range(len(classes))]
    db_img = Insect_Images.objects.all()
    db_img = db_img[len(db_img) - 1]
    path = os.path.join("media", db_img.insect_input_img.name)
    img = cv2.imread(path,cv2.IMREAD_COLOR)
    print(path)
    if img is None:
        print("Gandal")
        return
    img = cv2.resize(img,(1280,720))
    hight,width,_ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255,(608,608),(0,0,0),swapRB = True,crop= False)

    net.setInput(blob)

    output_layers_name = net.getUnconnectedOutLayersNames()

    layerOutputs = net.forward(output_layers_name)

    boxes =[]
    confidences = []
    class_ids = []


    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > confThreshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes,confidences,confThreshold,nmsThreshold)

    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > confThreshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)

                x = int(center_x - w/2)
                y = int(center_y - h/2)



                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,confThreshold,nmsThreshold)
    font = cv2.FONT_HERSHEY_PLAIN
    # colors = np.random.uniform(0,255,size =(len(boxes),3))
    colors = [random.randint(255) for i in range(len(classes))]


    if  len(indexes)>0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[class_ids[i]]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,label + " " + confidence, (x,y+50),font,2,color,2)
            counts[class_ids[i]]  += 1

    # cv2.imshow('img',img)
    path = "./media/detected_images/predicted_" + str(db_img.insect_input_img.name.split('/')[1])
    cv2.imwrite(path, img)

    str_cnt = ""
    for i in counts:
        str_cnt += str(i) + " "

    db_img.counts = str_cnt
    db_img.insect_detected_img = "detected_images/predicted_" + str(db_img.insect_input_img.name.split('/')[1])
    db_img.save()

    cv2.waitKey(0)
    print(counts)
    cv2.destroyAllWindows()
