from re import I
from unrealcv import client
import cv2
import time
import numpy as np
import os
import time
import getpass

colour = np.zeros((7,3))
USER = getpass.getuser()

Path =  'C:\\Users\\' + USER + '\\Desktop\\UnrealGenerator\\'
height  = 640
width = 480  

def init():

  global colour
  global USER
  global Path
  global height,width

  for k in range(1,7):

    client.request('vget /camera/'+str(k)+'/object_mask '+ Path + 'init\\' + str(k) + '.png')

    img = cv2.imread(Path + 'init\\' + str(k) + '.png')

    tmp = GetColorCenter(img,2)

    colour[k][0] = tmp[0]
    colour[k][1] = tmp[1]
    colour[k][2] = tmp[2]




def GetCameraImages(nbr):

  for i in range(1,nbr):


    for k in range(1,6):

      client.request('vget /camera/'+str(k)+'/object_mask '+ Path + str(k) + '_' + str(i) + 'mask' +'.png')
      client.request('vget /camera/'+str(k)+'/lit '+ Path + str(k) + '_' + str(i) +'.png')


      img = cv2.imread(Path + str(k) + '_' + str(i) + 'mask' +'.png')

      thr   = Threshold(img,colour[k])
      
      drw, xmin, ymin, xmax, ymax = contouring(thr)

      labeling(i,k,xmin,ymin,xmax,ymax)

      
      #cv2.imshow("draw",drw)
      #cv2.imwrite(Path + str(k) + '\\label'+ str(i) +'.png',drw)
      #cv2.waitKey(0)
      os.remove(Path + str(k) + '_' + str(i) + 'mask' +'.png')

      time.sleep(0.1)

    
    print(str(round(100*(i/nbr) + (k/7) -1)) + "%")
      



def GetColorCenter(img,n):
  

  b = img[int(img.shape[0]/2),int(img.shape[1]/2), 0]
  g = img[int(img.shape[0]/2),int(img.shape[1]/2), 1]
  r = img[int(img.shape[0]/2),int(img.shape[1]/2), 2]

  return b,g,r



def Threshold(frame,color):

  # Retrive frame and success of the reading

  lower_Blue = np.array([color[0], color[1], color[2]])
  upper_Blue = np.array([color[0], color[2], color[2]])

  mask = cv2.inRange(frame, lower_Blue, upper_Blue) 
  res = cv2.bitwise_and(frame,frame, mask= mask)


  #cv2.imshow("draw",mask)
  #cv2.waitKey(0)


  return mask





def contouring(img):

  contours,hierarchy = cv2.findContours(img, 1, 2)
  thr = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
  drw = cv2.drawContours(thr, contours, -1, (0,255,0), 3)

  contours = np.squeeze(np.asarray(contours))

      
  listx = list(contours[:,0])
  listy = list(contours[:,1])

  max_x = int(max(listx))
  max_y = int(max(listy))

  min_x = int(min(listx))
  min_y = int(min(listy))

  drw = cv2.circle(drw, (min_x,min_y), radius=5, color=(0, 0, 255), thickness=-1)
  drw = cv2.circle(drw, (max_x,max_y), radius=5, color=(0, 0, 255), thickness=-1)

  return drw, min_x, min_y, max_x, max_y


def labeling(i,k,xmin,ymin,xmax,ymax):

  center_x = xmin + abs(xmax - xmin)/2
  center_y = ymin + abs(ymax - ymin)/2

  bounding_height = abs(xmax - xmin)
  bounding_width = abs(ymax - ymin)

  f= open(Path + str(k) + '_'+ str(i) +'.txt',"w+")
  f.write(str(k-1) + " " + str(center_x/width) + " " + str(center_y/height) + " " + str(bounding_width/width) + " " + str(bounding_height/height))
  f.close()


if __name__ == "__main__":


  client.connect() # Connect to the game


  if not client.isconnected(): # Check if the connection is successfully established


    print ('UnrealCV server is not running. Run the game from http://unrealcv.github.io first.')


  else:


    try:




      print("\n ######### UE4 Generator #########")

      nbr = int(input("\nEnter the number of images of each signals you want :"))

      init()

      print("\n ######### Init done #########")
      input("\nhit [ENTER] to continue")

      GetCameraImages(nbr)

      #os.remove(Path + 'init')

      print("\n ######### Finished  #########")
        



    except KeyboardInterrupt:
      
      exit()

