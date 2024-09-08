import glob
import cv2 
import os
import tkinter as tk
from tkinter import simpledialog

def Annotator(image):
    flag = False
    ix = -1
    iy = -1
    # prevx = -1
    # prevy = -1
    boxes = []
    def draw(event, x, y, flags, params):
        global flag,ix, iy #, prevx, prevy
        nonlocal img, img_copy
        if event == 1:
            flag = True
            ix = x
            iy = y
            prevx = x
            prevy = y
        elif event == 0:
            if flag:
                img = img_copy.copy()
                # cv2.rectangle(img, pt1=(ix,iy), pt2=(prevx,prevy),color=(0,0,0), thickness=2)
                cv2.rectangle(img, pt1=(ix,iy), pt2=(x,y),color=(0,0,225), thickness=2)
                # prevx = x
                # prevy = y
        elif event== 4:
            if flag:
                flag = False
                boxes.append([ix,iy,x,y])
                for box in boxes:
                    cv2.rectangle(img, pt1=(box[0],box[1]), pt2=(box[2],box[3]),color=(0,0,225), thickness=2)
                img_copy = img.copy()
                img_name = os.path.basename(file).split('.')[0]
                # label = int(input('Enter the Label:'))
                w,h,_ = img.shape
                label = simpledialog.askstring(title="Test", prompt="Label:")
                with open(f'./Annotations/{img_name}.txt','a+') as f:
                    f.write(f'{label} {(x+ix)/(2*w)} {(y+iy)/(2*h)} {abs(x-ix)/w} {abs(y-iy)/h}\n')
            
    # img = np.zeros((512,512,3))
    img = cv2.resize(cv2.imread(image),(700,700))
    img_copy = img.copy()

    cv2.namedWindow(winname='window')
    cv2.setMouseCallback('window', draw)

    while True:
        cv2.imshow('window', img)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    ROOT = tk.Tk()
    ROOT.withdraw()
    for file in glob.glob("./images/*.jpeg"):
        Annotator(file)
