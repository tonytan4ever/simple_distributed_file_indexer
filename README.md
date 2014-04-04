Simple Distributed File Indexer (Python)

===============================

A Multip-process, command-line indexer application that finds the top 10 words across a collection of documents.


1. Have a fixed number (N) of worker processes (say, N=3) that handle text
indexing. Workers should be able to run on separate machines from each
other.

2. When a worker process receives a text blob to process, it tokenizes it
into words. Words are delimited by any character other than A-Z or 0-9.

3. A master collection, shared between all workers, keeps track of all
unique words encountered and the number of times it was encountered. Each
time a word is encountered, the count for that word is incremented (the
word is added to the list if not present). Words should be matched in a
case-insensitive manner and without any punctuation.

4. The application should output the top 10 words (and their counts) to
standard out.



Build/Run Instructions:
1 This project depends on ZeroMQ, my favorite messaging library. Install ZeroMQ library on a linux machine:
            ```
      $wget http://download.zeromq.org/zeromq-4.0.4.tar.gz

      $tar -xzvf zeromq-4.0.4.tar.gz

      $cd zeromq-4.0.4

      $./configure

      $make && sudo make install
      ```
2. Install pyzmq
      ```
      $sudo pip install pyzmq
      ```
3. You will need to have python installed, to run this app:
      ```
      $python main.py [-N <number of workers>] -W <worker_1 ip:port> <worker_2 ip:port> <worker_3 ip:port> -F <file_1_path> <file_2_path>
      ```

       e.g: 
       $python main.py -W 127.0.0.1:5002 127.0.0.1:5004 127.0.0.1:5006 -F test_files/sample.txt test_files/TaleOfTwoCities.txt

       Number of workers has been defaulted to 3.
