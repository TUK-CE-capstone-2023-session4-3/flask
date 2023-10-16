# 라이브러리 설정
import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt

# mediapipe pose class를 초기화 한다.
mp_pose = mp.solutions.pose
# pose detect function에 image detect=True, 최소감지신뢰도 = 0.3, 모델 복잡도 =2를 준다.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
# mediapipe의 drawing class를 초기화한다.
mp_drawing = mp.solutions.drawing_utils

def detectPose(image, pose, display=True):
    # 예시이미지 copy하기
    output_image = image.copy()

    # 컬러 이미지 BGR TO RGB 변환
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # pose detection 수행
    results = pose.process(imageRGB)

    # input image의 너비&높이 탐색
    height, width, _ = image.shape

    # detection landmarks를 저장할 빈 list 초기화
    landmarks = []

    # landmark가 감지 되었는지 확인
    if results.pose_landmarks:

      # landmark 그리기
      mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)

      # 감지된 landmark 반복
      for landmark in results.pose_landmarks.landmark:

        # landmark를 list에 추가하기
        landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

    # 오리지널 image와 pose detect된 image 비교
    if display:

      # 오리지널 & 아웃풋 이미지 그리기
      plt.figure(figsize=[22,22])
      plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
      plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');

      # 3D 랜드마크 나타내기
      mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    # 그렇지 않다면, output_image 와 landmark return한다
    else:
      return output_image, landmarks
    
# 앵글 계산 함수
def calculateAngle(landmark1, landmark2, landmark3):

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle

#쓰러짐 계산 함수
def detect_fall(landmark1, landmark2):
    x1, y1, _ = landmark1 #왼쪽 어깨
    x2, y2, _ = landmark2 #오른쪽 어깨

    if abs(y2-y1) < abs(x2-x1):
        fall = 1
    else:
        fall = 0
    return fall

# 분류 함수
def classifyPose(landmarks, output_image, display=False):
    
    label = 'Unknown Pose'
    color = (0, 0, 255)
    
    #---------------------------------------각도 계산---------------------------------------
    # 11번, 13번, 15번 landmark 
    # 왼쪽 어깨, (왼쪽 팔꿈치), 왼쪽 손목 landmark angle 값 계산 
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    # 12번, 14번, 16번 landmark 
    # 오른쪽 어깨, (오른쪽 팔꿈치), 오른쪽 손목 landmark angle 값 계산 
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
    # 13번, 11번, 23번 landmark 
    # 왼쪽 팔꿈치, (왼쪽 어깨), 왼쪽 엉덩이, landmark angle 값 계산 
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # 14번, 12번, 24번 landmark 
    # 오른쪽 팔꿈치, (오른쪽 어깨), 오른쪽 엉덩이 landmark angle 값 계산  
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    # 23번, 25번, 27번 landmark 
    # 왼쪽 엉덩이, (왼쪽 무릎), 왼쪽 발목 landmark angle 값 계산 
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # 24번, 26번, 28번 landmark 
    # 오른쪽 엉덩이, (오른쪽 무릎), 오른쪽 발목  landmark angle 값 계산 
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    # 11번, 23번, 25번 landmark 
    # 왼쪽 어깨, (왼쪽 골반), 왼쪽 무릎 landmark angle 값 계산 
    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    # 12번, 24번, 26번 landmark 
    # 오른쪽 어깨, (오른쪽 골반), 오른쪽 무릎  landmark angle 값 계산 
    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    #---------------------------------------------------------------------------------------------

    
    #---------------------------------------쓰러짐 계산--------------------------------------------

    # 어깨-골반
    left_sh = detect_fall(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    right_sh = detect_fall(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    # 어깨-무릎
    left_sk = detect_fall(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    right_sk = detect_fall(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    # 어깨-발목
    left_sa = detect_fall(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    right_sa = detect_fall(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    # 골반-무릎
    left_hk = detect_fall(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    right_hk = detect_fall(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    # 골반-발목
    left_ha = detect_fall(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    right_ha = detect_fall(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    # 무릎-발목
    left_ka = detect_fall(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    right_ka = detect_fall(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    #---------------------------------------------------------------------------------------------


    
    #------------------------------------------Stand----------------------------------------------
    # 팔을 펴고 있는지 확인
    if left_elbow_angle > 170 and right_elbow_angle >170 and left_elbow_angle < 190 and right_elbow_angle < 190:

        #다리를 펴고 있는지 확인
        if left_knee_angle > 170 and right_knee_angle > 170 and left_knee_angle < 190 and right_knee_angle < 190:
            
            label = 'Stand'
    #----------------------------------------------------------------------------------------------------------


    
    #------------------------------------------Sit----------------------------------------------
    # 골반 각도 계산
    if (left_hip_angle > 50 and left_hip_angle < 130) or (right_hip_angle > 50 and right_hip_angle < 130) or (left_hip_angle > 230 and left_hip_angle < 310) or (right_hip_angle > 230 and right_hip_angle < 310):

        #무릎 각도 계산
        if (left_knee_angle > 50 and left_knee_angle < 130) or (right_knee_angle > 50 and right_knee_angle < 130) or (left_knee_angle > 230 and left_knee_angle < 310) or (right_knee_angle > 230 and right_knee_angle < 310):
            
            label = 'Sit'
    #----------------------------------------------------------------------------------------------------------



    
    #------------------------------------------Fall----------------------------------------------
    #어깨-발목 위치계산
    if left_sa == 1 or right_sa == 1:
        if left_sh == 1 or right_sh == 1:
            label = 'Falldown'

    # if left_sk == 1 or right_sk == 1:
    #     
    # if left_hk == 1 or right_hk == 1:
    #   
    # if left_ha == 1 or right_ha == 1:
    #    
    # if left_ka == 1 or right_ka == 1:
    #     

    count = 0
    #----------------------------------------------------------------------------------------------------------
    
        
    # 포즈 별 라벨 색깔 구분
    if label != 'Falldown':           #Falldown: 빨강
        if label == 'Unknown Pose':   #Unknown Pose: 노랑
            color = (0, 255, 255) 
        else:                         #나머지: 초록
            color = (0, 255, 0)  
    else:
        color = (0, 0, 255)
        
    # 분류되지 않은 자세라면 Unkwown Pose로 왼쪽 상단에 text 입력
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    
    # 결과 이미지 보여주기
    if display:
        # 결과 이미지를 BGR TO RGB로 matplotlib을 이용해 꺼내준다.
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    else:
        
        # 결과 이미지랑 표시될 label을 return 한다
        return output_image, label

pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

class VideoCamera(object):
    def __init__(self):
      self.video = cv2.VideoCapture(1)
      self.fall_detected = 0

    def __del__(self):
      self.video.release()

    def get_frame(self):
      ret, frame = self.video.read()
      #--------------------------------------
      frame = cv2.flip(frame, 1)
      frame_height, frame_width, _ =  frame.shape
      frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
      frame, landmarks = detectPose(frame, pose_video, display=False)

      label = None

      if landmarks:
          frame, label = classifyPose(landmarks, frame, display=False)

          if label == 'Falldown':
            self.fall_detected = 1
            print(1)
            cv2.putText(frame, "falldown", (500, 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
          else:
            self.fall_detected = 0

      #--------------------------------------
      ret, jpeg = cv2.imencode('.jpg', frame)
      return jpeg.tobytes(), label



