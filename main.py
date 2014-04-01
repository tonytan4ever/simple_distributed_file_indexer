import multiprocessing
import time

def merge(d2):
    time.sleep(1) # some time consuming stuffs
    for key in d2.keys():
        if key in d1:
            d1[key] += d2[key]
        else:
            d1[key] = d2[key]

def init(d):
    global d1
    d1 = d

if __name__ == '__main__':

    d1 = multiprocessing.Manager().dict()
    pool = multiprocessing.Pool(initializer=init, initargs=(d1, ))

    l = [{ x % 5 : x } for x in range(10)]

    for item in l:
        pool.apply_async(merge, (item,))

    pool.close()
    pool.join()

    print(l)
    print(d1)