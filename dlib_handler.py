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
from scipy.spatial import distance

from pathlib import Path
import glob



class Dlib_handler:
    
    def __init__(self,rgb_cam_device,inf_cam_device):
        self.img_store_path = "data/saved_images/"
        self.known_faces_path = "data/known_faces.pickle"
        self.rgb_cam_device=rgb_cam_device
        self.inf_cam_device=inf_cam_device
        
        self.known_faces = {}
        
        
        self.face_rec_model_path = "data/models/dlib_face_recognition_resnet_model_v1.dat"
        self.predictor_path = "data/models/shape_predictor_5_face_landmarks.dat"
        #models
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)
        
        self._load_face_embeddings()
            


    def registerFaces(self,resampling:int = 50,re_register :bool =False):
        for folder in glob.glob(self.img_store_path+"/*"):
            user_id = os.path.basename(os.path.normpath(folder))
            if(not re_register):
                #if not full re_register initiated, skip already existing users
                if(user_id in self.known_faces):
                    continue
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
                #add embedding with id pair
                self.known_faces[user_id] = embedding
                #break after first sucessful face we don't need multiple embeddings now
                break
        self._save_face_embeddings(self.known_faces)
    def _save_face_embeddings(self,faces:dict):
        #TODO should change up pickle if reaches 2 GB
        if(len(faces)):
            pickle.dump(faces,open(self.known_faces_path,"wb"))
            
    def _load_face_embeddings(self):
        try:
            faces = pickle.load(open(self.known_faces_path,"rb"))
            self.known_faces = faces
        except FileNotFoundError:
            print("known faces not found please register faces")
                
    
    
    
    
    
    def ID(self,frame):
        # cam = cv2.VideoCapture(self.rgb_cam_device)
        # self.running = True
        # self.recognized = []
        # while self.running:
        #     ret,frame = cam.read()
        #     #resize
        #     small_frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
        #     # change to black and white
        #     small_frame = small_frame[:,:,::-1]
  
            #detect faces, upsample by 1
            detections = self.detector(frame, 1)
            print("Number of faces detected: {}".format(len(detections)))
            for k, d in enumerate(detections):
                #get face landmarks
                shape = self.sp(frame, d)
                # compute face descriptor embeddings with given resampling number, and fixed padding
                embedding = self.facerec.compute_face_descriptor(frame, shape, 1, 0.25)
                #loop through known faces
                #Early abortion on first match instead of findig best
                for k,face in self.known_faces.items():
                    #COMPARE
                    validated = distance.euclidean(embedding,face) < 0.6
                    if validated:
                        print("validated with id {}".format(k))
                        # self.running = False
                        return k
            return False


                
# %% Main
if __name__ == "__main__":
    handler = Dlib_handler(2,0)
    faces = handler.known_faces.keys()
