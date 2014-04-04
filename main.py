"""
Simple file index implementation
Strategy:
1. Use multiprocessing.pool to implement worker process.
2. A global dictionalry,  master_word_statistics holds words' statistics.
3. Each worker process is running as a 0mq REPLY process which responds to the
   the main process's incoming message(s) (two types: file blob message and EOF
   message indicating complete). Why not PUSH/PULL ? to avoid message loss! 
   Simple results show PUSH/PULL have high message loss rate, I myself have
   couple of examples.
3. Distribute the work load (i.e file blob message) on worker process in a round-robin 
   fashion. (probably not very efficient, but given all the assumptions this is the 
   unkonw optimal strategy )

Protocol:
Assign each file's blob to each worker in round-robin style, when all the files are 
assigned send an EOF to each worker to end the worker process.

Assumption:
1. Providing a list of files in plain text to index on.
"""
import multiprocessing
import os, sys, time, argparse, traceback
import zmq

from tokenize import tokenize_line

EOF = u'\x0004'

master_word_statistics = {}

def merge(worker_result):
    global master_word_statistics
    for key in worker_result.keys():
        if key in master_word_statistics:
            master_word_statistics[key] += worker_result[key]
        else:
            master_word_statistics[key] = worker_result[key]


def worker(connection_string):
    """
    To do:
    Failure mode: 
    How to handle failures in a worker process ?
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s" % connection_string)
    print("Running worker process on:  %s\n" % connection_string)
    worker_local_statistics = {}
    while True:
        file_blob = socket.recv_unicode()
        if file_blob == EOF:
            print("Get EOF, shutdown worker process %s..." % os.getpid())
            socket.send_unicode("Get EOF, shutdown worker process %s..." % os.getpid())
            break
        else:
            socket.send_unicode("Worker process %s gets message, building index on it..." % os.getpid())
            tokenize_line(file_blob, worker_local_statistics)
    print("Ending worker process... %s" % str(os.getpid()))
    return worker_local_statistics


def main(N, worker_ip_port_list, files_list):
    pool = multiprocessing.Pool(processes=N)
    results = []
    for w_ip_port in worker_ip_port_list:
        r = pool.apply_async(worker, (w_ip_port, ), callback=merge)
        results.append(r)
    sender_ctx = zmq.Context()
    sender_socket = sender_ctx.socket(zmq.REQ)
    # distribute each file to worker process to count words on
    # load balance strategy: round-robin
    for idx, f in enumerate(files_list):
        try:
            infile = open(f)
            s = infile.read()
            worker_ip_port = worker_ip_port_list[idx % len(worker_ip_port_list)]
            sender_socket.connect("tcp://%s" % worker_ip_port)
            sender_socket.send_unicode(s.decode("UTF-8"))
            message = sender_socket.recv_unicode()
            print "Received reply from %s, file %s is processing..." % (worker_ip_port, f)
            sender_socket.disconnect("tcp://%s" % worker_ip_port)
        except IOError, e:
            print("Error while processing file %s, error info:" % f)
            traceback.print_exc()
            
    # send an EOF to each worker process to indicate end of indexing process...
    for c in worker_ip_port_list:
        sender_socket.connect("tcp://%s" % c)
        sender_socket.send_unicode(EOF)
        message = sender_socket.recv_unicode()
        print "Worker process running on %s is terminated..." % c 
        sender_socket.disconnect("tcp://%s" % c)
    for r in results:
        r.wait()
    pool.close()
    pool.join()
    # sort the word statistics by it's number of appeareance. 
    sorted_word_statistics = sorted(master_word_statistics.iteritems(), 
                                      key=lambda word_number_tuple: word_number_tuple[1], 
                                      reverse=True)
    return sorted_word_statistics[:10]
    
    


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
        print("Nothing to index...")
        parser.print_help()
        sys.exit(1)
        
    if len(worker_ip_port_list) != N:
        print("The number of worker's ip:port connection string does not match: %s" % N)
    res = main(N, worker_ip_port_list, files_list)
    #print res
    print "Top 10 words are: %s" % str([t[0] for t in res])
    time.sleep(0.1)
    sys.exit(0)
        