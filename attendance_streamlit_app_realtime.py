import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# --- Paths ---
IMAGES_PATH = "ImagesAttendance"
ATTENDANCE_CSV = "Attendance.csv"

os.makedirs(IMAGES_PATH, exist_ok=True)

# --- Functions ---
@st.cache_data
def load_images_and_names(path):
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        if cl.endswith(('.jpg', '.jpeg', '.png')):
            curImg = cv2.imread(f'{path}/{cl}')
            if curImg is not None:
                images.append(curImg)
                classNames.append(os.path.splitext(cl)[0].lower())  # lowercase
    return images, classNames


@st.cache_data
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList


def markAttendance(name, csv_path=ATTENDANCE_CSV):
    name = name.lower()
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as f:
            f.write("Name,Date,Time\n")
    with open(csv_path, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.strip().split(',')[0] for line in myDataList if line.strip() and not line.startswith("Name")]
        if name not in nameList:
            now = datetime.now()
            dString = now.strftime('%Y-%m-%d')
            tString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dString},{tString}')


def process_frame(frame, encodeListKnown, classNames):
    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis) if len(faceDis) > 0 else None

        if matchIndex is not None and matches[matchIndex]:
            name = classNames[matchIndex]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    return frame


# --- UI ---
st.set_page_config(page_title="Face Attendance System", layout="wide")
st.title("📸 Face Recognition Attendance System")

tab1, tab2 = st.tabs(["📍 Attendance", "➕ Register New Person"])

# --- Tab 1: Attendance ---
with tab1:
    st.subheader("Real-time Attendance")
    images, classNames = load_images_and_names(IMAGES_PATH)
    encodeListKnown = findEncodings(images)

    run_camera = st.checkbox("Start Webcam")
    FRAME_WINDOW = st.image([])

    if run_camera:
        cap = cv2.VideoCapture(0)
        while run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access camera")
                break
            frame = process_frame(frame, encodeListKnown, classNames)
            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cap.release()

    st.subheader("Attendance Records")
    if os.path.exists(ATTENDANCE_CSV):
        try:
            df = pd.read_csv(ATTENDANCE_CSV)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading attendance file: {e}")
    else:
        st.info("No attendance records yet.")


# --- Tab 2: Register ---
with tab2:
    st.subheader("Register a New Person")

    new_name = st.text_input("Enter Name")
    new_capture = st.camera_input("Capture Face")

    if st.button("Save new person"):
        if new_capture is None:
            st.error("Please capture a photo first.")
        elif not new_name.strip():
            st.error("Please enter a name.")
        else:
            safe_name = "".join(c for c in new_name.strip() if c.isalnum() or c in (' ', '_', '-')).rstrip().lower()
            filename = f"{safe_name.replace(' ', '_')}.jpg"

            # duplicate safeguard
            if os.path.exists(os.path.join(IMAGES_PATH, filename)):
                st.error(f"Name '{safe_name}' is already registered!")
            else:
                file_bytes = np.asarray(bytearray(new_capture.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                save_path = os.path.join(IMAGES_PATH, filename)
                cv2.imwrite(save_path, img)
                st.success(f"Saved: {save_path}")

                # Clear cached data so new encoding loads next time
                load_images_and_names.clear()
                findEncodings.clear()
