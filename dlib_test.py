from dlib_handler import Dlib_handler
import cv2

handler = Dlib_handler(2,0)

cam1 = cv2.VideoCapture(2)
cam2 = cv2.VideoCapture(0)
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
        #pressed esc
        print("Escape hit, closing...")
        cam1.release()
        cam2.release()
        cv2.destroyAllWindows()
        break
    elif k % 256 == 32:
        # cv2.imwrite(img_name, frame1)
        #move files to user path
        identity =  handler.ID(frame1)
        if identity:
            print("identified as {}".format(identity))
        else:
            print("no user identified")
            