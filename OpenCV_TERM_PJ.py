import cv2
import tkinter
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import random
import numpy as np


def mouse_event_handler(event, x, y, flags, param):
# Change 'mouse_state' (given as 'param') according to the mouse 'event'
 if event == cv2.EVENT_LBUTTONDOWN:
  param[0] = True
  param[1] = (x, y)
 elif event == cv2.EVENT_LBUTTONUP:
  param[0] = False
 elif event == cv2.EVENT_MOUSEMOVE and param[0]:
  param[1] = (x, y)

def cartoon_filter(img):
    h, w = img.shape[:2]
    img2 = cv2.resize(img, (w//2, h//2))

    blr = cv2.bilateralFilter(img2, -1, 20, 7)
    edge = 255 - cv2.Canny(img2, 80, 120)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    dst = cv2.bitwise_and(blr, edge) 
    dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)
                                                                  
    return dst

def convert_to_binary():
    global src, x, y, w, h 

    imgd = src[y:y+h, x:x+w]
    gray = cv2.cvtColor(imgd, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    dvdimg = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    src[y:y+h, x:x+w] = dvdimg
    
    img = src.copy()
    if switch == 1:
        img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
def convert_color():
    global src, x, y, w, h, switch

    imgd = src[y:y+h, x:x+w]
    img_nega = 255 - imgd
    src[y:y+h, x:x+w] = img_nega
    
    img = src.copy()
    if switch == 1:
        img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
def intensity_control():
    global src, x, y, w, h, switch
    contrast = 1.6
    contrast_step = 0.1
    brightness = -40
    brightness_step = 1
    
    contrast += contrast_step * random.randrange(-10,10)
    brightness += brightness_step * random.randrange(-10,10)
    
    imgd = src[y:y+h, x:x+w]
    img_tran = contrast * imgd + brightness 
    img_tran[img_tran < 0] = 0
    img_tran[img_tran > 255] = 255
    src[y:y+h, x:x+w] = img_tran
    
    img = src.copy()
    if switch == 1:
        img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
    
def apply_mosaic():
    global src, x, y, w, h, switch
     
    imgd = src[y:y+h, x:x+w]
    mosaic = cv2.resize(imgd, (w//15, h//15))
    mosaic = cv2.resize(mosaic, (w,h), interpolation=cv2.INTER_AREA)  
    src[y:y+h, x:x+w] = mosaic
    
    img = src.copy()
    if switch == 1:
        img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
def convert_grayscale():
    global src, x, y, w, h, switch
     
    imgd = src[y:y+h, x:x+w]
    gray = cv2.cvtColor(imgd, cv2.COLOR_BGR2GRAY)
    dvdimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    src[y:y+h, x:x+w] = dvdimg
    
    img = src.copy()
    if switch == 1:
        img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
    
def designate_image_range():
    global src, x, y, w, h, switch
    
    x, y, w, h = cv2.selectROI("Select a range with the mouse and press the space bar", src, False)
    cv2.destroyAllWindows()
    switch = 1
    img = src.copy()
    img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
def cancel_designate_image_range():
    global src, x, y, w, h, switch
    
    x, y, w, h = 0, 0, 900, 650 #범위 지정 좌표와 길이
    switch = 0 #범위 지정 온오프
    img = src.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
def convert_cartoon_style():
    global src, x, y, w, h, switch
     
    imgd = src[y:y+h, x:x+w]
    cart = cartoon_filter(imgd)
    src[y:y+h, x:x+w] = cart
    
    img = src.copy()
    if switch == 1:
        img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
def return_origin():
    global src, x, y, w, h, switch
     
    x, y, w, h = 0, 0, 900, 650 #범위 지정 좌표와 길이
    switch = 0 #범위 지정 온오프
    
    src = cv2.imread("C:/Users/kirby_sleep.png")
    src = cv2.resize(src, (900, 650))
    img = src.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk
    
    
def free_drawing(canvas_width=900, canvas_height=650, init_brush_radius=3):
    global src, x, y, w, h, switch
    
    # Prepare a canvas and palette
    img = src.copy()
    canvas = img
    b = g = r = 0
    palette = (b % 255 , g % 255, r % 255)

    # Initialize drawing states
    mouse_state = [False, (-1, -1)] # Note) [mouse_left_button_click, mouse_xy]
    brush_color = 0
    color_state = 'r'
    game_mode = "free_drawing"
    brush_radius = init_brush_radius


    # Instantiate a window and register the mouse callback function
    cv2.namedWindow('Free Drawing (save : esc)')
    cv2.setMouseCallback('Free Drawing (save : esc)', mouse_event_handler, mouse_state)

    while True:
        # Draw a point if necessary
        mouse_left_button_click, mouse_xy = mouse_state
        if mouse_left_button_click:
            if game_mode == 'circle':
                cv2.circle(canvas, mouse_xy, 60+brush_radius, (b % 255 , g % 255, r % 255), 5)
            elif game_mode == 'rectangle':
                pt1, pt2 = (mouse_xy[0]-60-brush_radius, mouse_xy[1]-50-brush_radius), (mouse_xy[0]+60+brush_radius, mouse_xy[1]+50+brush_radius)
                cv2.rectangle(canvas, pt1, pt2, color=(b % 255 , g % 255, r % 255), thickness=5)
            elif game_mode == 'triangle':
                pts = np.array([(mouse_xy[0], mouse_xy[1]-50-brush_radius), (mouse_xy[0]-55-brush_radius, mouse_xy[1]+50+brush_radius), (mouse_xy[0]+55+brush_radius, mouse_xy[1]+50+brush_radius)], dtype=np.int32).reshape(-1,1,2)
                cv2.polylines(canvas, [pts], True, color=(b % 255 , g % 255, r % 255), thickness=5)
            elif game_mode == 'star':
                pts = np.array([(mouse_xy[0], mouse_xy[1]-53-brush_radius), (mouse_xy[0]-11.9-brush_radius*0.22, mouse_xy[1]-16.4-brush_radius*0.31), 
                                (mouse_xy[0]-50.4-brush_radius*0.95, mouse_xy[1]-16.4-brush_radius*0.31), (mouse_xy[0]-16.4-brush_radius*0.38, mouse_xy[1]+3.9+brush_radius*0.12), 
                                (mouse_xy[0]-31.2-brush_radius*0.59, mouse_xy[1]+42.9+brush_radius*0.81), (mouse_xy[0], mouse_xy[1]+20.3+brush_radius*0.38), 
                                (mouse_xy[0]+31.2+brush_radius*0.59, mouse_xy[1]+42.9+brush_radius*0.81), (mouse_xy[0]+16.4+brush_radius*0.38, mouse_xy[1]+3.9+brush_radius*0.12),
                                (mouse_xy[0]+50.4+brush_radius*0.95, mouse_xy[1]-16.4-brush_radius*0.31), (mouse_xy[0]+11.9+brush_radius*0.22, mouse_xy[1]-16.4-brush_radius*0.31)], dtype=np.int32).reshape(-1,1,2)
                cv2.polylines(canvas, [pts], True, color=(b % 255 , g % 255, r % 255), thickness=5)
            else:
                cv2.circle(canvas, mouse_xy, brush_radius, (b % 255 , g % 255, r % 255), -1)
        # Show the canvas
        canvas_copy = canvas.copy()
        info = f'Brush Radius: {brush_radius}'
        cv2.putText(canvas_copy, info, (10, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv2.putText(canvas_copy, info, (10, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv2.putText(canvas_copy, 'r', (190, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0 , 0, r % 255), thickness=2)
        cv2.putText(canvas_copy, 'r', (190, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0 , 0, r % 255))
        cv2.putText(canvas_copy, '+', (210, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv2.putText(canvas_copy, '+', (210, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv2.putText(canvas_copy, 'g', (230, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0 , g % 255, 0), thickness=2)
        cv2.putText(canvas_copy, 'g', (230, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0 , g % 255, 0))
        cv2.putText(canvas_copy, '+', (250, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv2.putText(canvas_copy, '+', (250, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv2.putText(canvas_copy, 'b', (270, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , 0, 0), thickness=2)
        cv2.putText(canvas_copy, 'b', (270, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , 0, 0))
        cv2.putText(canvas_copy, '=', (290, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv2.putText(canvas_copy, '=', (290, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv2.putText(canvas_copy, "color", (310, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , g % 255, r % 255), thickness=2)
        cv2.putText(canvas_copy, "color", (310, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , g % 255, r % 255))
        cv2.putText(canvas_copy, "mode = ", (380, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv2.putText(canvas_copy, "mode = ", (380, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv2.putText(canvas_copy, game_mode, (470, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv2.putText(canvas_copy, game_mode, (470, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        
        
        cv2.imshow('Free Drawing (save : esc)', canvas_copy)
        # Process the key event
        key = cv2.waitKey(1)
        if key == 27: # ESC
          src = img.copy()
          if switch == 1:
              img = cv2.rectangle(img , (x, y), (x+w, y+h), color=(0, 0, 0), thickness=2)
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          img = Image.fromarray(img)
          imgtk = ImageTk.PhotoImage(image=img)

          label.config(image=imgtk)
          label.image = imgtk
          break
        elif key == ord(' '):
            if color_state == 'b':
                b += 1
            elif color_state == 'g':
                g += 1
            else:
                r += 1
        elif key == ord('u'): #up
            if color_state == 'r':
                color_state = 'b'
            elif color_state == 'g':
                color_state = 'r'
            else:
                color_state = 'g'
        elif key == ord('d'): #down
            if color_state == 'r':
                color_state = 'g'
            elif color_state == 'g':
                color_state = 'b'
            else:
                color_state = 'r'        
        elif key == ord('c'):
            game_mode = "circle"
        elif key == ord('r'):
            game_mode = "rectangle"  
        elif key == ord('t'):
            game_mode = "triangle"
        elif key == ord('s'):
            game_mode = "star"
        elif key == ord('f'):
            game_mode = "free_drawing"
        elif key == ord('+') or key == ord('='):
          brush_radius += 1
        elif key == ord('-') or key == ord('_'):
          brush_radius = max(brush_radius - 1, 1)
        elif key == ord('e'):
             img = src.copy()
             canvas = img
    cv2.destroyAllWindows()
    
def save_image():
    global src
    img = src.copy()
    cv2.imwrite("C:/Users/kirby_sleep_edit.png", img)
    messagebox.showinfo("저장 완료" , "저장이 완료되었습니다")
    
    

    
    
x, y, w, h = 0, 0, 900, 650 
switch = 0
window=tkinter.Tk()

window.title("Simple Painter")
window.geometry("900x730+100+100")
window.resizable(False, False)


#src = cv2.imread("C:/Users/kirby_sleep.png")
src = cv2.imread("kirby_sleep.png")
src = cv2.resize(src, (900, 650))

img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)


label=tkinter.Label(window, image=imgtk)
label.pack(side="top")


button1 = tkinter.Button(window, text="범위 지정", overrelief="solid",relief = "groove", background = "white" , command=designate_image_range)
button1.place(x=5, y=660)

button2 = tkinter.Button(window, text="범위 지정 해제(전체화면)", overrelief="solid",relief = "groove", background = "white" , command=cancel_designate_image_range)
button2.place(x=75, y=660)

button3 = tkinter.Button(window, text="이진화 처리", overrelief="solid",relief = "groove", background = "white" , command=convert_to_binary)
button3.place(x=225, y=660)

button4 = tkinter.Button(window, text="색상 반전", overrelief="solid",relief = "groove", background = "white" , command=convert_color)
button4.place(x=305, y=660)

button4 = tkinter.Button(window, text="밝기 변환(변환값은 랜덤입니다)", overrelief="solid",relief = "groove", background = "white" , command=intensity_control)
button4.place(x=375, y=660)

button5 = tkinter.Button(window, text="모자이크 적용", overrelief="solid",relief = "groove", background = "white" , command=apply_mosaic)
button5.place(x=565, y=660)

button6 = tkinter.Button(window, text="그레이 스케일 변환", overrelief="solid",relief = "groove", background = "white" , command=convert_grayscale)
button6.place(x=660, y=660)

button7 = tkinter.Button(window, text="카툰 효과", overrelief="solid",relief = "groove", background = "white" , command=convert_cartoon_style)
button7.place(x=785, y=660)

button8 = tkinter.Button(window, text="이미지에 그림 그리기", overrelief="solid",relief = "groove", background = "white" , command=free_drawing)
button8.place(x=5, y=695)

button9 = tkinter.Button(window, text="이미지를 원래대로 되돌리기", overrelief="solid",relief = "groove", background = "white" , command=return_origin)
button9.place(x=140, y=695)

button10 = tkinter.Button(window, text="이미지 저장", overrelief="solid",relief = "groove", background = "white" , command=save_image)
button10.place(x=310, y=695)



window.mainloop()