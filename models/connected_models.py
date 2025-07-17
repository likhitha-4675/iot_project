from datetime import datetime

mysql = None
def init_mysql(mysql_obj):
    global mysql
    mysql = mysql_obj

def add_device(device_name: str, device_id: str) -> tuple[bool, str]:
    connected_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_usage = '0'
    status = True
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO connected_users (device_name, device_id, connected_date, data_usage, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (device_name, device_id, connected_date, data_usage, status))
        mysql.connection.commit()
        cur.close()
        return True, "Device added successfully."
    except Exception as e:
        return False, str(e)

def get_all_devices() -> list[dict]:
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT device_name, device_id, connected_date, data_usage, status FROM connected_users")
        rows = cur.fetchall()
        cur.close()
        devices = []
        for row in rows:
            devices.append({
                "device_name": row[0],
                "device_id": row[1],
                "connected_date": row[2],
                "data_usage": row[3],
                "status": bool(row[4])
            })
        return devices
    except Exception as e:
        print(f"Error fetching devices: {e}")
        return []
def deactivate_device(device_id: str) -> tuple[bool, str]:
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE connected_users SET status = FALSE WHERE device_id = %s
        """, (device_id,))
        mysql.connection.commit()
        cur.close()
        return True, "Device deactivated successfully."
    except Exception as e:
        return False, str(e)
