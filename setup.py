# import face_recognition
import cv2
import pickle
import os
import numpy as np


from pathlib import Path
import glob
img_store_path = "data/saved_images/"
rgb_cam_device = 2
inf_cam_device = 0


        

def register(name):
	#Create images folder
	if not os.path.exists(img_store_path):
		os.makedirs(img_store_path)
	#Create folder of person (IF NOT EXISTS) in the images folder
	Path(img_store_path+name).mkdir(parents=True, exist_ok=True)
	#Obtain the number of photos already in the folder
	numberOfFile = len([filename for filename in os.listdir(img_store_path + name)
						if os.path.isfile(os.path.join(img_store_path + name, filename))])
	#Add 1 because we start at 1
	numberOfFile+=1
	#Take a photo code
	cam1 = cv2.VideoCapture(rgb_cam_device)
	cam2 = cv2.VideoCapture(inf_cam_device)
	cv2.namedWindow("rgb_cam")
	cv2.namedWindow("inf_cam")


	while True:
		#Read rgb and infra camera frames
		ret1, frame1 = cam1.read()
		ret2, frame2 = cam2.read()
		cv2.imshow("rgb_cam", frame1)
		cv2.imshow("inf_cam", frame2)
		if not ret1:
			break
		k = cv2.waitKey(1)
		
		if k % 256 == 27:
			# ESC pressed
			print("Escape hit, closing...")
			cam1.release()
			cam2.release()
			cv2.destroyAllWindows()
			break
		elif k % 256 == 32:
            #  Hit SPACE
			img_name = str(numberOfFile)+"_rgb.png"
			img_name_inf = str(numberOfFile)+"_inf.png"
			cv2.imwrite(img_name, frame1)
			cv2.imwrite(img_name_inf,frame2)
			print("{} and {} was written".format(img_name,img_name_inf))
			#move files to user path
			os.replace(img_name, img_store_path+name.lower()+"/"+img_name)
			os.replace(img_name_inf, img_store_path+name.lower()+"/"+img_name_inf)
			cam1.release()
			cam2.release()
			cv2.destroyAllWindows()
			break


    



def identify():
    #TODO: reload data after new registers
    
    
    



# register("Test_ID")