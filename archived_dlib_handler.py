# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 23:36:16 2023

@author: tomcs
"""
import face_recognition
import cv2
import pickle
import os
import numpy as np


from pathlib import Path
import glob



class Dlib_handler:
    
    
    def __init__(self,rgb_cam_device,inf_cam_device):
        self.img_store_path = "data/saved_images/"
        self.label_file_path = "data/labels.pickle"
        self.rgb_cam_device
        self.inf_cam_device
        
        try:
            with open("/"+self.label_file_path,"rb") as f:
                self.labels = pickle.load(f)
                print(self.labels)
        except FileNotFoundError:
            print("No labels file found, creating new")
        
        
        


    def loadFaces(self):
        for folder in glob.glob(self.img_store_path+"/*"):
            # check folders
            for file in glob.glob(folder+"/*_rgb.png"):
                #extract foldername as ID
                pass
        # for root,dirs,files in os.walk(self.img_store_path):
        #     # check folder
        #     for file in files:
        #         # 
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