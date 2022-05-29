import cv2
import mediapipe as mp
import math
import os
import copy
import pickle

pose_val={}
image_angle={'right hip': '', 'left hip': '', 'right knee': '', 'left knee': '', 'right shoulder': '', 
              'left shoulder': '', 'right elbow': '', 'left elbow': ''}
pose_keypoint=[[12,24,26], [11,23,25], [24,26,28], [23,25,27], 
             [14,12,11], [12,11,13], [16,14,12], [11,13,15]]
user_angle={'right hip': '', 'left hip': '', 'right knee': '', 'left knee': '', 'right shoulder': '', 
              'left shoulder': '', 'right elbow': '', 'left elbow': ''}
keypoints=list(image_angle.keys())

mp_drawing = mp.solutions.drawing_utils
mp_pose=mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic=mp.solutions.holistic

pose=mp_holistic.Holistic(min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)


pose_name=os.listdir("Dataset")

print(pose_name)

def FindAngle(frame,id1,id2,id3):
    lmList=[]
    image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    if results.pose_landmarks:
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = frame.shape
            cx,cy = int(lm.x*w),int(lm.y*h)
            lmList.append([id,cx,cy])
        
        y1,x1 = lmList[id1][1:]
        y2,x2 = lmList[id2][1:]
        y3,x3 = lmList[id3][1:]
        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        #print(angle)
        #check if problem solved
        if(abs(angle)<0): #angel used checked here was the issue
            final_angle=abs(360-abs(angle))
        else:
            final_angle=abs(angle)
        
        return round(final_angle,3)
    else:
        return 0

def RecordAngle(frame,dict_ang):
    for i in range(len(dict_ang)):
        dict_ang[keypoints[i]]=FindAngle(frame,pose_keypoint[i][0],pose_keypoint[i][1],pose_keypoint[i][2])
    return dict_ang

for i in pose_name:
    pic=cv2.imread("Dataset\\"+i)
    values=RecordAngle(pic,image_angle)
    pose_val[i]=copy.deepcopy(values)

f=open('pose_dat.dat','wb')
pickle.dump(pose_val,f)


