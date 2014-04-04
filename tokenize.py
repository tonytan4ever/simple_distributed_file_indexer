"""
This module has the tokenize method of a file.
Assumptions:
1. A word is consisting of letters, numbers or underscores
2. We conduct statistics on each unique words case-insensitively, 
    i.e: The == the
"""
import re, unittest

WORD_REGEX = re.compile("[A-Za-z0-9_]+")
#or word_regex = "\w+"

VERY_LARGE_DICT_LENGTH = 10

def tokenize_line(line, word_statistic_dict):
    word_list = WORD_REGEX.findall(line)
    for word in word_list:
        # case insensitive match
        word = word.lower()
        if not word in word_statistic_dict:
            word_statistic_dict[word] = 1
        else:
            word_statistic_dict[word] += 1


def tokenize_file(file_name, word_statistic_dict):
    with open(file_name) as infile:
        for line in infile:
            tokenize_line(line, word_statistic_dict)



class test_tokenizer(unittest.TestCase):
    def test_tokenize_line(self):
        line_1 = ""
        word_statistic_dict = {}
        tokenize_line(line_1, word_statistic_dict)
        self.assertEqual(word_statistic_dict, {}, "Empty string tokenize error")
        line_2 = "The quick brown fox jumps over the lazy dog"
        tokenize_line(line_2, word_statistic_dict)
        self.assertFalse(word_statistic_dict == {}, "Sample string tokenize error")
        self.assertEqual(word_statistic_dict["the"], 2, "Counting 'the' incorrectly")
    
    def test_tokenize_file(self):
        word_statistic_dict = {}
        try:
            # should probably use mock to simulate this exception, will do in version 2
            tokenize_file("no_existent_file.txt", word_statistic_dict)
        except:
            self.assertEqual(word_statistic_dict, {}, "Non existent file tokenzie error...")
        tokenize_file("test_files/LesMiserables.txt", word_statistic_dict)
        self.assertTrue(len(word_statistic_dict.keys())>=VERY_LARGE_DICT_LENGTH, "Not so many words in the book message")   
        

if __name__ == "__main__":
    unittest.main()