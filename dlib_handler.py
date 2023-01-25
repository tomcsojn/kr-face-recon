# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 23:36:16 2023

@author: tomcs
"""
import dlib
import cv2
import pickle
import os
import numpy as np


from pathlib import Path
import glob



class Dlib_handler:
    
    
    def __init__(self,rgb_cam_device,inf_cam_device):
        self.img_store_path = "data/saved_images/"
        self.label_file_path = "data/known_faces.pickle"
        self.rgb_cam_device=rgb_cam_device
        self.inf_cam_device=inf_cam_device
        
        self.known_faces = {}
        
        
        self.face_rec_model_path = "data/models/dlib_face_recognition_resnet_model_v1.dat"
        self.predictor_path = "data/models/shape_predictor_5_face_landmarks.dat"
        #models
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)
        
        
        try:
            with open("/"+self.label_file_path,"rb") as f:
                self.labels = pickle.load(f)
                print(self.labels)
        except FileNotFoundError:
            print("No labels file found, creating new")
            


    def registerFaces(self,resampling):
        for folder in glob.glob(self.img_store_path+"/*"):
            # check folders
            for file in glob.glob(folder+"/*_rgb.png"):
                #extract foldername as ID
                img = dlib.load_rgb_image(file)
                #detect faces, upsample by 1
                detections = self.detector(img, 1)
                print("Number of faces detected: {}".format(len(detections)))
                if len(detections) > 1:
                    print("skipping image more than 1 face detected")
                    continue
                # enumerate for all faces, use first face now as only allow pictures with one face.
                d = detections[0]
                shape = self.sp(img, d)
                # compute face descriptor embeddings with given resampling number, and fixed padding
                embedding = self.facerec.compute_face_descriptor(img, shape, resampling, 0.25)
                
                #save embedding with id pair
                
                
                #break after first sucessful face we don't need multiple embeddings now
                break
                
                
    def ID(self):
        cam = cv2.VideoCapture(self.rgb_cam_device)
        self.running = True
        self.recognized = []
        while self.running:
            ret,frame = cam.read()
            #resize
            small_frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
            # change to black and white
            small_frame = small_frame[:,:,::-1]
            if self.running:
                #search faces
                locations = face_recognition.face_locations(frame)

                #encode face
                embeddings = face_recognition.face_encodings(frame,locations)
                #looping through encodings
                for embedding in embeddings:
                    #loop through known faces
                    for face in self.known_faces:
                        #COMPARE
                        matches = face_recognition.compare_faces([face[1]],embedding)


                
# %% Main
if __name__ == "__main__":
    handler = Dlib_handler(2,0)