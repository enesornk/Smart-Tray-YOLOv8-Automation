from flask import Flask, render_template, Response, jsonify, request
from ultralytics import YOLO
import cv2
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

model = YOLO("best.pt")
DB_NAME = "akilli_tepsi.db"

# MENÜ (Fiyat ve Kalori)
MENU = {
    "coke":   {"price": 30,  "cal": 140},
    "burger": {"price": 180, "cal": 550},
    "pizza":  {"price": 220, "cal": 800},
    "fries":  {"price": 50,  "cal": 320},
    "water":  {"price": 10,  "cal": 0},
    "ayran":  {"price": 20,  "cal": 70},
    "fanta":  {"price": 30,  "cal": 150}
}

current_cart = {}

# --- VERİTABANI FONKSİYONLARI ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tablo yoksa oluştur: ID, Tarih, İçerik (JSON), Toplam Fiyat, Toplam Kalori
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            items TEXT,
            total_price REAL,
            total_cal INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Uygulama başlarken veritabanını hazırla
init_db()

def generate_frames():
    global current_cart
    camera = cv2.VideoCapture(1) 

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        results = model(frame, conf=0.40)
        detected_items = {} 
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                
                x1, y1, x2, y2 = box.xyxy[0]
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                item_info = MENU.get(class_name, {"price": 0, "cal": 0})
                label = f"{class_name} {item_info['cal']}kcal"
                cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                if class_name in detected_items:
                    detected_items[class_name] += 1
                else:
                    detected_items[class_name] = 1
        
        current_cart = detected_items
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

# Yeni Admin Sayfası
@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders_raw = cursor.fetchall()
    conn.close()

    # Veriyi HTML'e göndermeden önce düzenle
    orders = []
    for order in orders_raw:
        orders.append({
            "id": order[0],
            "date": order[1],
            "siparis_icerigi": json.loads(order[2]),
            "total_price": order[3],
            "total_cal": order[4]
        })

    return render_template('admin.html', orders=orders)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_bill')
def get_bill():
    bill_data = []
    total_price = 0
    total_calories = 0
    
    # Sepet Hesaplama
    for item, quantity in current_cart.items():
        info = MENU.get(item)
        if info:
            price = info['price']
            cal = info['cal']
            subtotal_price = price * quantity
            subtotal_cal = cal * quantity
            total_price += subtotal_price
            total_calories += subtotal_cal
            
            bill_data.append({
                "name": item.capitalize(),
                "quantity": quantity,
                "price": price,
                "cal": cal,
                "subtotal": subtotal_price,
                "subtotal_cal": subtotal_cal
            })

    discount = 0
    campaign_name = ""

    # Kural: Hamburger + Patates + İçecek varsa indirim yap
    has_burger = 'burger' in current_cart
    has_fries = 'fries' in current_cart
    has_drink = ('coke' in current_cart) or ('fanta' in current_cart) or ('ayran' in current_cart)

    if has_burger and has_fries and has_drink:
        discount = 40 
        campaign_name = "OGRENCI MENUSU"
        total_price -= discount 
        
    return jsonify({
        "items": bill_data, 
        "total_price": max(0, total_price), # Fiyat eksiye düşmesin
        "total_cal": total_calories,
        "discount": discount,       
        "campaign": campaign_name   
    })

# Yeni Sipariş Kaydetme Rotası
@app.route('/save_order', methods=['POST'])
def save_order():
    data = request.json
    
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    items_json = json.dumps(data['items'])
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (date, items, total_price, total_cal) VALUES (?, ?, ?, ?)",
                   (now, items_json, data['total_price'], data['total_cal']))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

# --- SİLME İŞLEMİ ROTASI ---
@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
    
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Sipariş silindi."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
# --- KOMPLE SIFIRLAMA ROTASI ---
@app.route('/reset_db', methods=['POST'])
def reset_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 1. Tüm siparişleri sil
        cursor.execute("DELETE FROM orders")
        
        # 2. Sayacı (ID) sıfırla 
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
        
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Veritabanı tamamen sıfırlandı. Sayaç 1'den başlayacak."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)