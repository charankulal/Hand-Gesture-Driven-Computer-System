import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=1,trackCon=1):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands()
        self.mpDraw=mp.solutions.drawing_utils
    
    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks :
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        
        return img
    
    def findPosition(self,img, handNo=0,draw=True):
        xList=[]
        yList=[]
        boundingBox=[]
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id,cx,cy])
                # if draw:
                #     cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            xMin,xMax=min(xList),max(xList)
            yMin,yMax=min(yList),max(yList)
            boundingBox=xMin,yMin,xMax,yMax
            
            if draw:
                cv2.rectangle(img,(boundingBox[0]-20,boundingBox[1]-20),(boundingBox[2]+20,boundingBox[3]+20),(0,255,0),2)
        return self.lmList, boundingBox

