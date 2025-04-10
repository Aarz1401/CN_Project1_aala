import socket

tracker_data = {}

s = socket.socket()
s.bind(("localhost", 9000))
s.listen(5)

print("Tracker is running...")

while True:
    conn, addr = s.accept()
    data = conn.recv(4096).decode()
    filename, mapping = data.split(":", 1)
    tracker_data[filename] = eval(mapping)
    print(f"Updated tracker for {filename}: {tracker_data[filename]}")
    conn.close()
