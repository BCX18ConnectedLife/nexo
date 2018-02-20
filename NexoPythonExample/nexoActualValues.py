# Echo server program
import socket
import sys
import threading
import nexoActualValues_pb2

print 'nexoActualValues python server started'

HOST = '' # Symbolic name meaning the local host
PORT = 1264 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(8)
print 'listen for max. 8 connections'
prntMutex = threading.Lock()
threads = []

#Connection handler
def socketHandler(conn, addr):
  nxData = nexoActualValues_pb2.actValues()
  while True:
    data = conn.recv(32000)
    if not data:
      break
    prntMutex.acquire()
    print 'from ', addr
    try:
      nxData.ParseFromString(data)
      print nxData
    except :
      data = conn.recv(32000)
    prntMutex.release()
  conn.close()

while 1:
  conn, addr = s.accept()
  print 'Connected by ', addr
  task = threading.Thread(target=socketHandler, args=(conn, addr,), name='socketWorker')
  threads.append(task)
  task.start()
s.close()
print("exit nexoActualValues")
