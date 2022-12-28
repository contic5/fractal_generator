import numpy as np
from PIL import Image
import time
import cv2

width=1920-500
height=1080-330
filename='spires'
usingfile=True
def getarr():
    myfile=open(filename+'.csv','r',encoding='utf-8-sig')
    arr=[]
    for line in myfile:
        arr.append([])
        line=line.strip()
        parts=line.split(',')
        arr[-1]=parts
    #print2d(arr)
    #print()
    return arr
def showimage(myarr):
    mydict= {
     1: (0, 0, 0), #black
     2: (0, 0, 255), #red
     3: (0, 255, 0), #green
     4: (255, 0, 0), #blue
     5: (255, 255, 255), #white
     6: (128, 128, 128), #gray
     7: (255, 0, 255), #purple
     8: (0, 255, 255), #yellow
     9: (0, 165, 255), #orange
     }
    FILLED = 1  # food key in dict
    BLANK = 5  # player key in dict
    movetime=0.5
    print(myarr.shape[0],myarr.shape[1])
    env = np.zeros((myarr.shape[0], myarr.shape[1], 3), dtype=np.uint8)  # starts an rbg of our size
    textenv = np.zeros((myarr.shape[0], myarr.shape[1]), dtype=str)  # starts an rbg of our size
    for i in range(0,myarr.shape[0]):
        for j in range(0,myarr.shape[1]):
            if(myarr.shape[0]==3):
                print(myarr[i][j])
            if(myarr[i][j]=='0' or myarr[i][j]=='000' or myarr[i][j]==''):
                textenv[i][j]='0'
                env[i][j]=mydict[BLANK]
            else:
                textenv[i][j]='1'
                env[i][j]=mydict[FILLED]
    if(myarr.shape[0]==3):
        print('env=')
        print2d(textenv)
    img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = img.resize((width,height))  # resizing so we can see our agent in all its glory.
    cv2.imshow("Environment (Press n to next)", np.array(img))  # show it
    
    while True:
        k=cv2.waitKey(0)
        if(k == ord('s')):
            print("Image saved")
            img = img.save(filename+".jpg") 
        if(k == ord('n')):
            break
    time.sleep(movetime)

def print2d(a):
    maxlen=-1
    for i in range(len(a)):
        for j in range(len(a[0])):
            if(len(a[i][j])>maxlen):
                maxlen=len(a[i][j])
    for i in range(len(a)):
        for j in range(len(a[0])):
            res=a[i][j]
            while(len(res)<maxlen):
                res=res+' '
            print(res,end=' ')
        print()

def main():
    arr=[]
    
    
    if(usingfile):
        arr=getarr()
    else:
        arr=[
        ['90','V','270'],
        ['0','1','0'],
        ['90','V','270']
        ]
        arr=[
        ['90','V','270'],
        ['H','1','H'],
        ['0','1','0']
        ]
    
    arr=np.array(arr, str)
    print('NP arr=')
    print2d(arr)
    print('Showing image')
    showimage(arr)

    for b in range(3):
        if(arr.shape[0]**2>800):
            break

        #Result array
        res=np.full((arr.shape[0]**2,arr.shape[1]**2),'000')
        print('result')
        
        #Fractal shapes
        ninety=np.rot90(arr)
        oneeighty=np.rot90(arr,2)
        twoseventy=np.rot90(arr,3)
        zerofill=np.full((arr.shape[0],arr.shape[1]),'0')
        horizontal=np.fliplr(arr)
        vertical=np.flipud(arr)
        orig=arr.copy()

        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                if(arr[i][j]=='90'):
                    curnext=ninety
                elif(arr[i][j]=='180'):
                    curnext=oneeighty
                elif(arr[i][j]=='270'):
                    curnext=twoseventy
                elif(arr[i][j]=='H'):
                    curnext=horizontal
                elif(arr[i][j]=='V'):
                    curnext=vertical
                elif(arr[i][j]=='1'):
                    curnext=orig
                else:
                    curnext=zerofill
                #if(b<1):
                    #print(curnext)
                for m in range(arr.shape[0]):
                    for n in range(arr.shape[1]):
                        res[i*arr.shape[0]+m][j*arr.shape[1]+n]=curnext[m][n]
        arr=res.copy()
        #if(b<1):
            #print2d(arr)
        print('done')
        showimage(arr)
main()