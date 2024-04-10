import cv2
import time
import tkinter as tk

face_cascade = cv2.CascadeClassifier('real.xml')

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
frame_height, frame_width, _ = frame.shape

midline_y = int(frame_height / 2)
start_time = None
head_position_history = []

# Function to create the popup window
def show_popup():
  popup = tk.Tk()
  popup.title("Notice :")
  label = tk.Label(popup, text="You are down!", font=("Arial", 20))
  label.pack(padx=20, pady=20)
  popup.geometry("300x100")
  popup.wm_attributes('-topmost', True)
  popup.after(3000, popup.destroy) # Close popup after 2 seconds
  popup.mainloop()

while True:
  ret, frame = cap.read()
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

  consecutive_downs = sum(head_position_history[-3:]) # Check last 3 positions
  if consecutive_downs >= 3:
    print("You are down!")
    head_position_history.clear()
    show_popup() # Trigger the popup when head is down
    import moi

  cv2.line(frame, (0, midline_y), (frame_width, midline_y), (255, 255, 0), 2)
  cv2.imshow('frame', frame)

  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
