import os
import sys
import mmap
from time import sleep
import posix_ipc

# turn off stdout buffering
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

print "Page size of the system is {}".format(posix_ipc.PAGE_SIZE)
shm = posix_ipc.SharedMemory("/mysharedmem")
map = mmap.mmap(shm.fd, shm.size)
shm.close_fd()

# create a semaphore to signal sender we are ready
sem = posix_ipc.Semaphore("/mysemaphore", posix_ipc.O_CREX)
sem.release()
# wait for the sender to get the lock
sleep(1)

while True:
    # wait for sender to send message
    sem.acquire()
    # print the line out
    map.seek(0)
    line = map.readline()
    print line,
    # signal sender we are ready for next msg
    sem.release()
    if line.startswith("."):
        sem.acquire()
        break
    # sleep so sender has chance to get the lock
    sleep(1)


try:
    map.close()
except:
    print "failed to close mmap"

try:
    sem.release()
    sem.unlink()
except:
    print "failed to close semaphore"