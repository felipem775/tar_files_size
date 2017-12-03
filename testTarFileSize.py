import unittest
import tar_file_size

import os

class TestTarFileSize(unittest.TestCase):

    def setUp(self):
        self.path = "test/files"
        self.output = "test/tmp"
        self.size = 60000

    def test_complete_list_files(self):
        complete_list_files = tar_file_size.filesInDir(self.path)
        self.assertEqual(len(complete_list_files), 38)
        
    def test_files_in_list(self):
        complete_list_files = tar_file_size.filesInDir(self.path)
        list_tar = tar_file_size.split_in_max_size(self.size, complete_list_files)
        count_list_tar = 0
        for l in list_tar:
            count_list_tar += len(l)
        self.assertNotEqual(len(complete_list_files), 0)
        self.assertEqual(len(complete_list_files), count_list_tar)

    def test_all_tar_must_have_files(self):
        complete_list_files = tar_file_size.filesInDir(self.path)
        list_tar = tar_file_size.split_in_max_size(self.size, complete_list_files)
        for l in list_tar:
            self.assertNotEqual(len(l),0)

    def test_do_tar(self):
        filelist = ['test/files/0Dxv3ZsKZo8l', 'test/files/fdtg9OJjJy83', 'test/files/k7RZc10CYT4j']
        output = "test/tmp_test_do_tar_files.tar"

        if os.path.isfile(output):
            os.remove(output)
        self.assertFalse(os.path.isfile(output))

        tar_file_size.do_tar(output, filelist)
        self.assertTrue(os.path.isfile(output))
        
    @unittest.skip("Movido")
    def test_human2bytes(self):
        number_bytes = tar_file_size.human2bytes("1 K")
        self.assertEqual(number_bytes, 1024)
        number_bytes = tar_file_size.human2bytes("1K")
        self.assertEqual(number_bytes, 1024)
        number_bytes = tar_file_size.human2bytes("5M")
        self.assertEqual(number_bytes, 5242880)
        number_bytes = tar_file_size.human2bytes("5 G")
        self.assertEqual(number_bytes, 5368709120)
        number_bytes = tar_file_size.human2bytes("1000")
        self.assertEqual(number_bytes, 1000)
        
        
if __name__ == '__main__':
    unittest.main()
