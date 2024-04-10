import cv2
import time
import tkinter as tk
import pygame
from threading import Thread


pygame.init()



def play_sound_and_exit(sound_file="phonk.mp3"): # here change the name
    # to play phonk one so just put the sound file in the folder and just change the name 
    
    try:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        while pygame.mixer.get_busy():
            pass
    except Exception as e:  
        print(f"Error playing sound: {e}")
    
        




def show_popup():
    popup = tk.Tk()
    popup.title("Notice :")
    label = tk.Label(popup, text="You are down!", font=("Arial", 20))
    label.pack(padx=20, pady=20)
    popup.geometry("300x100")
    popup.wm_attributes('-topmost', True)
    popup.after(3000, popup.destroy)  
    popup.mainloop()





face_cascade = cv2.CascadeClassifier('real.xml')  

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

if not ret:
    print("Error: Could not capture video from webcam.")
    exit()

frame_height, frame_width, _ = frame.shape

midline_y = int(frame_height / 2)
start_time = None
head_position_history = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    head_is_down = False
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        head_is_down = y < midline_y
        face_position = "Above" if head_is_down else "Below"
        cv2.putText(frame, face_position, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
       
    if start_time is None:
        start_time = time.time()

    elapsed_time = time.time() - start_time
    if elapsed_time > 3:
        head_position_history.append(0 if head_is_down else 1)
        start_time = time.time()  

    consecutive_downs = sum(head_position_history[-3:])  
    if consecutive_downs >= 3:
        print("You are down!")
        head_position_history.clear()
        show_popup()

       
        thread = Thread(target=play_sound_and_exit)
        thread.start()
        

    cv2.line(frame, (0, midline_y), (frame_width, midline_y), (255, 255, 0), 2)
    cv2.imshow("Tracker HHeee not actually don't forgot to sit straight ", frame)

    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
