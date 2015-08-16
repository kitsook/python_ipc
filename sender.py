from time import sleep
import sys
import os
import mmap
import posix_ipc

# turn off stdout buffering
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

# create named shared memory and use memory map to access it
print "Page size of the system is {}".format(posix_ipc.PAGE_SIZE)
shm = posix_ipc.SharedMemory("/mysharedmem", posix_ipc.O_CREX, size=posix_ipc.PAGE_SIZE)
map = mmap.mmap(shm.fd, shm.size)
shm.close_fd()

# receiver will create a semaphore to signal we can start sending messages
sem = None
print "waiting for receiver"
while True:
    try:
        sleep(1)
        sem = posix_ipc.Semaphore("/mysemaphore", flags = 0)
        # receiver is on. get the semaphore
        sem.acquire()
        break
    except:
        print '.',

print
print "receiver connected, start typing messages. type .(dot) to exit"

while True:
    line = raw_input()
    map.seek(0)
    map.write(line+'\n')
    print ">> sending msg...",
    # release the lock...
    sem.release()
    # ... and sleep to give chance for receiver to get the lock
    sleep(1)
    # wait for receiver to process the previous message and release the lock
    sem.acquire()
    print "done"
    if line.startswith("."):
        sem.release()
        break
    
try:
    map.close()
except:
    print "failed to close mmap"
    
try:
    shm.unlink()
except:
    print "failed to clean up shared memory"
    
try:
    sem.close()
except:
    print "failed to clean up semaphore"