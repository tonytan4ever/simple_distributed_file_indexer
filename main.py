"""
Simple file index implementation
Strategy:
1. Use multiprocessing.pool to implement worker process.
2. Use multiprocessing.Manager to implement a master collection 
   that holds words' statistics.
3. Distribute the work load on worker process in a round-robin fashion

Assumption:
1. Providing a list of files in plain text to index on.
"""
import multiprocessing
import sys, argparse
import zmq


def merge(d2):
    for key in d2.keys():
        if key in d1:
            master_word_statistics[key] += d2[key]
        else:
            master_word_statistics[key] = d2[key]

def init(d):
    global master_word_statistics
    master_word_statistics = d


def server(port="5556"):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    
    # serves only 5 request and dies
    for reqnum in range(5):
        # Wait for next request from client
        message = socket.recv()
        print "Received request #%s: %s" % (reqnum, message)
        socket.send("World from %s" % port)
        

def worker(connection_string):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://%s" % connection_string)
    print "Running worker process on:  %s\n" % connection_string
    while True:
        file_blob = socket.recv()
    


def main(N, worker_ip_port_list, files_list):
    master_word_statistics = multiprocessing.Manager().dict()
    pool = multiprocessing.Pool(initializer=init, initargs=(master_word_statistics,))
    pool.map(worker, worker_ip_port_list)
    #for f in files_list:
    pool.close()
    pool.join()   
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", "--worker_count", type=int,
                    default=3,
                    help="Number of workers")
    parser.add_argument("-W", "--worker_ip_port_list", type=str, nargs="+",
                    help="A list of worker processes' denoted by ipaddress:port. The length of this list must match N")
    parser.add_argument("-F", "--files_list", type=str, nargs="+",
                    help="A list of files to be indexed on")

    args = parser.parse_args()
    N = args.worker_count
    worker_ip_port_list = args.worker_ip_port_list
    files_list = args.files_list
    if files_list is None:
        print "Nothing to index..."
        parser.print_help()
        sys.exit(1)
        
    if len(worker_ip_port_list) != N:
        print "The number of worker's ip:port connection string does not match: %s" % N
    main(N, worker_ip_port_list, files_list)
        