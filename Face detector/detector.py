import cv2
import os
import numpy as np
from datetime import datetime
import face_recognition

class FaceDetector:
    def __init__(self):
        

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.known_face_encodings = []
        self.known_face_names = []
        
    def load_known_faces(self, known_faces_dir):
        """Load known faces from a directory for recognition"""
        print(f"Loading known faces from {known_faces_dir}...")
        
        for person_name in os.listdir(known_faces_dir):
            person_dir = os.path.join(known_faces_dir, person_name)
            
            if not os.path.isdir(person_dir):
                continue
                
            for image_file in os.listdir(person_dir):
                if image_file.startswith('.'):
                    continue
                    
                image_path = os.path.join(person_dir, image_file)
                image = face_recognition.load_image_file(image_path)
                
                try:
                    face_encoding = face_recognition.face_encodings(image)[0]
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(person_name)
                    print(f"Loaded {image_path} for {person_name}")
                except IndexError:
                    print(f"No face found in {image_path}")
                    
        print(f"Loaded {len(self.known_face_names)} known faces")
        
    def detect_faces_haar(self, frame):
        """Detect faces using Haar cascade"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
        
    def detect_faces_dnn(self, frame):
        """Detect faces using DNN model (more accurate)"""
        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), 
            (104.0, 177.0, 123.0))
            
        
        model_path = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
        config_path = "models/deploy.prototxt"
        
        if not os.path.exists(model_path) or not os.path.exists(config_path):
            raise FileNotFoundError("DNN model files not found")
            
        net = cv2.dnn.readNetFromCaffe(config_path, model_path)
        net.setInput(blob)
        detections = net.forward()
        
        faces = []
        (h, w) = frame.shape[:2]
        
        for i in range(detections.shape[2]):  
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.7:  
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                faces.append((startX, startY, endX-startX, endY-startY))
                
        return faces
        
    