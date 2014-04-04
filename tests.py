import unittest
from main import main



class testSDFI(unittest.TestCase):
    def setUp(self):
        self.files_list_simple = ['test_files/sample.txt', 
                                  'test_files/sample2.txt']
        
        self.files_list_complex = ['test_files/LesMiserables.txt', 
                                  'test_files/AliceInWonderland.txt',
                                  'test_files/prideNprejudice.txt',
                                  'test_files/TaleOfTwoCities.txt',
                                  'test_files/SherlockHolmes.txt',
                                  ]
    
    
    def test_simple(self):
        res = main(3, ["127.0.0.1:5000","127.0.0.1:5002","127.0.0.1:5004"], 
                   self.files_list_simple)
        self.assertTrue(len(res) <= 10, "result message length assertion failed...")
        self.assertTrue(res[0][1] >= res[1][1], "popularity occurrence assertion failed...")
        self.assertEqual(res[0][0], "the", "Most popular word is not 'the'...")
    
    
    def test_complete(self):
        res = main(3, ["127.0.0.1:5000","127.0.0.1:5002","127.0.0.1:5004"], 
                   self.files_list_complex)
        self.assertTrue(len(res) <= 10, "result message length assertion failed...")
        self.assertTrue(res[0][1] >= res[1][1], "popularity occurrence assertion failed...")
        self.assertEqual(res[0][0], "the", "Most popular word is not 'the'...")
        print("Top 10 words are: %s" % str([t[0] for t in res]))
    


if __name__ == "__main__":
    unittest.main()