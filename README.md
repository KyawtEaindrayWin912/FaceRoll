# FaceRoll  
> "Say cheese, mark present — attendance made smart."

**FaceRoll** is an AI-powered face recognition attendance system that replaces the traditional roll call. With just a webcam and a browser, it detects faces in real time and logs attendance instantly, complete with date and time stamps. Perfect for classrooms, offices, and events.

---

## Features
- 🎥 **Real-time face recognition** via webcam  
- 📝 **Automatic CSV attendance logging** with timestamps  
- 📂 **Store & manage known faces** in `ImagesAttendance/`  
- 🖼 **Test script** to verify face recognition works before running the main project  
- ⚡ Fast and accurate recognition with `face_recognition`  

---

## Project Structure
```

FaceRoll/
│
├── Basics.py                          # Basic face comparison demo
├── AttendanceProject.py               # Webcam-based attendance system
├── attendance\_streamlit\_app\_realtime.py  # Streamlit real-time attendance web app
├── ImagesBasic/                       # Sample images for Basics.py
│   ├── ElonMusk.jpg
│   ├── BillGates.jpg
│   └── ...
├── ImagesAttendance/                  # Stored registered face images
├── Attendance.csv                    # Auto-generated attendance log
└── README.md

````

---

## Script Details

### 1️⃣ Basics.py
A minimal example that:
- Loads two sample images (`ElonMusk.jpg`, `BillGates.jpg`).
- Detects faces, encodes them, and compares for similarity.
- Displays the result and face distance.

Use this script to **understand the basics** of face encoding & comparison.

---

### 2️⃣ AttendanceProject.py
A standalone OpenCV-based attendance tracker:
- Loads images from `ImagesAttendance`.
- Encodes known faces.
- Starts webcam to detect & recognize faces.
- Marks attendance in `Attendance.csv` with **Name, Date, Time**.
- Runs continuously until manually stopped.

---

### 3️⃣ attendance_streamlit_app_realtime.py
A **Streamlit web app** for:
- **Real-time webcam attendance tracking** inside a browser tab.
- **Registering new people** by capturing their photo from the browser.
- Displaying attendance records in a table.
- Automatically saving & encoding new faces.

**Tabs in the App:**
- **📍 Attendance:** Start/stop webcam, live recognition, auto-attendance marking.
- **➕ Register New Person:** Capture a new user’s face and save it.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/KyawtEaindrayWin912/FaceRoll.git
cd FaceRoll
````

### 2. Create & Activate a Virtual Environment

```bash
conda create -n faceroll python=3.9
conda activate faceroll
```

### 3. Install Dependencies

Make sure you have CMake & dlib installed (required by `face_recognition`).

```bash
pip install cmake
pip install face_recognition opencv-python streamlit pandas
```

On macOS you may also need:

```bash
brew install cmake boost
```

---

## Running the Scripts

**Run Basics.py:**

```bash
python Basics.py
```

**Run AttendanceProject.py:**

```bash
python AttendanceProject.py
```

**Run Streamlit App:**

```bash
streamlit run attendance_streamlit_app_realtime.py
```

---

## Attendance Data

* Attendance is stored in **Attendance.csv** with:

| Name | Date       | Time     |
| ---- | ---------- | -------- |
| elon | 2025-08-09 | 14:35:12 |
| bill | 2025-08-09 | 14:36:47 |

* Each registered face is stored in **ImagesAttendance/** as a `.jpg` file named after the person.

---

## ⚠️ Limitations

* Limited accuracy in low-light conditions or when faces are partially covered.
* Recognition accuracy can drop for faces at extreme angles or rapid movement.
* Real-time performance depends on hardware capability; low-spec machines may experience lag.

---

## License

MIT License

---

Feel free to contribute or raise issues on the GitHub repo.

---



