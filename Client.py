from scapy.all import *
import socket
import psutil
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

Video = input('URL Example : ')
a = Ether(src=psutil.net_if_addrs()['Wi-Fi'][0][1].replace('-',':'), dst="88:3C:1C:63:49:4E")
# a.show()
b = IP(ttl=10, src=socket.gethostbyname(socket.gethostname()), dst="125.209.210.90")
# b.show()
c = UDP(sport=50348, dport=80)
# c.show()
sendp(a/b/c/'naver.me/xmPGIg4v')  # sendp(a/b/c/Video)

# Library for Receiving Video
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import cv2, imutils, socket
import numpy as np
import time
import base64
from datetime import datetime

fourcc = 0x7634706d
now = datetime.now()
time_str = now.strftime("%d%m%Y%H%M%S")
time_name = '_Rec_' + time_str + '.mp4'
FPS = 30
frame_shape = False

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9999
message = b'Hello'

client_socket.sendto(message, (host_ip, port))
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
while True:
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.fromstring(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)
    frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1
    if not frame_shape:
        video_file_name = str(host_ip) + time_name
        out = cv2.VideoWriter(video_file_name, fourcc, FPS, (frame.shape[1], frame.shape[0]), True)
        frame_shape = True
    out.write(frame)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
client_socket.close()
out.release()
