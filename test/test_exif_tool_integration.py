import unittest
from datetime import datetime

import exif_tool


class TestIntegration(unittest.TestCase):

    def test_list_default(self):
        """
        Integration Test
        list only with no file args should default to all image types
        """
        result = exif_tool.main(['-l'])
        self.assertEqual(result, 0)

    def test_list_one_with(self):
        """
        Integration Test
        correctly parse args and call functions with correct args to list a file exif without crashing main()
        """
        result = exif_tool.main(['-l', 'jelena_dokic.jpg'])
        self.assertEqual(result, 0)

    def test_list_multiple_good_bad(self):
        """
        Integration Test
        correctly parse args for multiple good and bad file types without crashing main()
        """
        result = exif_tool.main(['--list', '299352.jpg', 'text.txt',
                                 'none', 'gym_drink_ad.jpg'])
        self.assertEqual(result, 0)

    def test_set_noargs(self):
        result = exif_tool.main(['--set'])
        self.assertEqual(result, 1)

    def test_set_one_current_nosec(self):
        """
        test set-time format mmddHHMM from options [[CC]YY]mmddHHMM[.SS]
        check listing results match set arg
        """
        exif_tool.main(['--set', '10211423', 'oxygen_mag.jpg'])
        result = exif_tool.get_exif_datetime('oxygen_mag.jpg')
        current_year = str(datetime.now().year)
        self.assertEqual(result, current_year + ':10:21 14:23:00')

    def test_set_one_current_sec(self):
        """
        test set-time format mmddHHMM.SS from options [[CC]YY]mmddHHMM[.SS]
        check listing results match set arg
        """
        exif_tool.main(['-t', '10211423.13', 'oxygen_mag.jpg'])
        result = exif_tool.get_exif_datetime('oxygen_mag.jpg')
        current_year = str(datetime.now().year)
        self.assertEqual(result, current_year + ':10:21 14:23:13')

    def test_set_one_ccyy_sec(self):
        """
        Integration Test:
        test set-time format CCYYmmddHHMM.SS from options [[CC]YY]mmddHHMM[.SS]
        main() parses full datetime arg, runs set_exif_datetime(), compares get_exif_datetime()
        """
        exif_tool.main(['--set', '201710211423.02', 'oxygen_mag.jpg'])
        result = exif_tool.get_exif_datetime('oxygen_mag.jpg')
        self.assertEqual(result, '2017:10:21 14:23:02')

    def test_set_multiple_yy_nosec(self):
        """
        Integration Test:
        test set-time format YYmmddHHMM from options [[CC]YY]mmddHHMM[.SS]
        main() parses datetime arg without [CC] or [.SS] on [file]..[file],
        runs set_exif_datetime(), compares get_exif_datetime() on each [file] [file]
        """
        exif_tool.main(['-t', '1810120101',
                        'oxygen_mag.jpg',
                        'f18.jpg'])

        current_cc = round(datetime.now().year/100)
        current_yr = str(current_cc) + '18'

        result = exif_tool.get_exif_datetime('oxygen_mag.jpg')
        # self.assertEqual(result, '2018:10:12 01:01:00')
        self.assertEqual(result, current_yr + ':10:12 01:01:00')

        result = exif_tool.get_exif_datetime('f18.jpg')
        self.assertEqual(result, current_yr + ':10:12 01:01:00')

    def test_set__good_bad_files(self):
        """
        include some bad files in list of files to set, non_image, nonexistent file
        bad files and good files are order independent
        on good files, set dates, integration test alters datetime, and get_exif_datetime confirms good files processed
        """
        current_year = datetime.now().year
        exif_tool.set_exif_datetime('tcook.jpg', current_year, 10, 19, 0, 0, 0)
        exif_tool.set_exif_datetime('f18.jpg', current_year, 10, 19, 0, 0, 0)

        result = exif_tool.main(['-t', '10211423', 'text.txt', 'tcook.jpg',
                                 'none', 'f18.jpg'])
        self.assertEqual(result, 2)

        result = exif_tool.get_exif_datetime('tcook.jpg')
        self.assertEqual(result, str(current_year) + ':10:21 14:23:00')
        result = exif_tool.get_exif_datetime('f18.jpg')
        self.assertEqual(result, str(current_year) + ':10:21 14:23:00')

    def test_set_bad_indate_alpha(self):
        result = exif_tool.main(['-t', 'SET', 'text.txt'])
        self.assertEqual(result, 1)

    def test_set_bad_indate_alphanum_1(self):
        result = exif_tool.main(['-t', 'set20191205.', 'tcook.jpg', 'f18.jpg'])
        self.assertEqual(result, 1)

    def test_set_bad_indate_alphanum_2(self):
        result = exif_tool.main(['--set', '20191205hhMM.', 'tcook.jpg', 'f18.jpg'])
        self.assertEqual(result, 1)

    def test_set_bad_indate_rangeout(self):
        result = exif_tool.main(['--set', '201912052460.', 'tcook.jpg', 'f18.jpg'])
        self.assertEqual(result, 1)

    """
    Note: Currently unable to test '*.jpg' because in a real live shell, the shell expands the wildcard and the script
    actually sees a list of files fully expanded (i.e. without wildcard characters).  Manual testing shows '*.jpg' as
    well as 'C*.jpg' or '*2*.jpg' all expand.  Pattern vs 'isfile' checking in the code to determine if glob should be
    used becomes unnecessary because the shell seems to 'always' expand the wildcard upstream of the python script. 
    """


if __name__ == '__main__':
    unittest.main()
