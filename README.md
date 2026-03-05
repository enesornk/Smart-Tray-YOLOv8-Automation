# 🍽️ Smart Tray: Deep Learning-Based Cafeteria Automation

## 📌 Project Overview
This project is an autonomous checkout and dietary tracking system designed for mass dining areas such as university cafeterias and restaurants. By leveraging advanced computer vision techniques, the system eliminates traditional cashier queues and provides users with instant nutritional feedback.

## 🚀 Problem & Solution
* **The Problem:** Traditional manual checkout processes in cafeterias take an average of 30-40 seconds per tray, causing significant bottlenecks.
* **The Solution:** This custom-trained YOLOv8 model detects multiple food items simultaneously, communicates with the backend, and calculates the total price and total calories in **3-5 seconds**.

## 🛠️ Tech Stack & Architecture
* **AI / Computer Vision:** YOLOv8 (Custom Trained), OpenCV
* **Backend:** Python, Flask
* **Database:** SQLite (Automated order logging and management)
* **Frontend:** HTML/CSS (Jinja2 Templates)

## ⚙️ Key Features
- **Real-Time Object Detection:** Accurately identifies items like burgers, fries, beverages, and condiments in varying conditions (angles, lighting, occlusion).
- **Contextual Logic & Pricing:** Matches detected items with backend dictionaries to calculate the total basket price instantly.
- **Nutritional Analysis:** Computes the total caloric value of the selected meal.
- **Database Integration:** Logs every transaction dynamically into an SQLite database with complete CRUD capabilities (reset, delete specific orders).

## 📥 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Smart-Tray-YOLOv8-Automation.git](https://github.com/YOUR_USERNAME/Smart-Tray-YOLOv8-Automation.git)
2. Install the required dependencies:
   pip install -r requirements.txt
3. Run the application:
   python app.py
4. Access the web interface at http://127.0.0.1:5000

📄 Documentation
Academic reports and presentation slides regarding the model training process, dataset creation, and architectural decisions can be found in the docs/ directory.
