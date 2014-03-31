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
