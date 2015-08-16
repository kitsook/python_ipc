import posix_ipc

# clean up the mess in case sender/receiver was terminated unexpectedly
try:
    posix_ipc.unlink_shared_memory("/mysharedmem")
except:
    print "failed to clean up shared memory"
    
try:
    posix_ipc.unlink_semaphore("/mysemaphore")
except:
    print "failed to clean up semaphore"