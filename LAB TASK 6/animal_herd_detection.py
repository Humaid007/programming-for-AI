import cv2
import numpy as np
from ultralytics import YOLO
from sklearn.cluster import DBSCAN
import folium
import smtplib
from email.mime.text import MIMEText

latitude = 28.7041
longitude = 77.1025

sender_email = "humaidhussain107@gmail.com"          #use your own mail
receiver_email = "muhammadehsaanijaz@gmail.com"      #your customer mail
app_password = "yrgz vzas dyeq rxxn"                 #your own 16 digit password

model = YOLO("yolov8n.pt") 

img_path = r"C:\Users\pc\Desktop\4.jpg"  
results = model(img_path)

animal_classes = ['cow', 'sheep', 'elephant', 'horse', 'zebra', 'giraffe', 'deer']
animal_positions = []

for box in results[0].boxes:
    cls_id = int(box.cls[0])
    class_name = model.names[cls_id]

    if class_name in animal_classes:
        x_center = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
        y_center = int((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
        animal_positions.append([x_center, y_center])

num_herds = 0
if len(animal_positions) > 0:
    clustering = DBSCAN(eps=50, min_samples=2).fit(animal_positions)
    labels = clustering.labels_
    num_herds = len(set(labels)) - (1 if -1 in labels else 0)
    print(f" Detected {num_herds} herd(s).")
else:
    labels = []

if num_herds > 0:
    m = folium.Map(location=[latitude, longitude], zoom_start=15)

    for herd_id in set(labels):
        if herd_id == -1:
            continue  

        herd_animals = [animal_positions[i] for i in range(len(labels)) if labels[i] == herd_id]

        lat_offset = np.random.uniform(-0.001, 0.001)
        lon_offset = np.random.uniform(-0.001, 0.001)

        folium.Marker(
            location=[latitude + lat_offset, longitude + lon_offset],
            popup=f"Herd {herd_id + 1}: {len(herd_animals)} animals",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    m.save("herd_map.html")
    print(" Map saved to herd_map.html")

if num_herds > 0:
    subject = " Animal Herd Detected!"
    body = f"""
One or more animal herds were detected near GPS: ({latitude}, {longitude})

- Number of herds: {num_herds}
- View the map: Open 'herd_map.html'

Please investigate if necessary.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(" Alert email sent!")
    except Exception as e:
        print(" Failed to send email:", e)

else:
    print("No herds detected. No alert sent.")
