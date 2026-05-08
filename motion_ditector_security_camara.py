import cv2
import numpy as np
import csv
from datetime import datetime

# --- SETUP: CSV File Banana ---
# Program start hote hi hum ek CSV file banayenge aur usme Headers likh denge
with open('security_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Status"])

cap = cv2.VideoCapture(0)
subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True)
kernel = np.ones((5, 5), np.uint8)

# Humara Flag Variable!
motion_active = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    mask = subtractor.apply(frame)
    _, thresh = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    clean_mask = cv2.dilate(thresh, kernel, iterations=2)
    
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Is frame mein motion hai ya nahi, usko track karne ke liye ek temporary variable
    motion_in_current_frame = False
    
    for c in contours:
        if cv2.contourArea(c) > 1000:
            motion_in_current_frame = True # Frame mein motion mil gaya!
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Motion Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # --- LOGIC AUR CSV WRITING ---
    
    # Case 1: Naya motion shuru hua hai
    if motion_in_current_frame == True and motion_active == False:
        # CSV ke liye time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Photo ke naam ke liye safe time format (bina colon ke)
        time_for_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        photo_name = f"intruder_{time_for_filename}.jpg"
        
        print(f"Alert! Motion Started at {current_time}. Saving {photo_name}")
        
        # --- NAYA CODE: Screenshot Save Karna ---
        # Hum original 'frame' ko save kar rahe hain, jisme abhi tak green box nahi bana hai (ya agar box chahiye toh bounding box draw hone ke baad save kar sakte ho)
        cv2.imwrite(photo_name, frame)
        # ----------------------------------------
        
        with open('security_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, "Motion Started"])
            
        motion_active = True

    cv2.imshow("Security Camera", frame)
    cv2.imshow("Clean Solid Mask", clean_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()