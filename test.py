import threading

threads = []

def longCalc(j):
    for i in range(100000000 // (j+1)):
        pass
    print('done', j)
    return None

for i in range(5):
    threads.append(threading.Thread(target=longCalc, args=(i,)))
    threads[-1].start()