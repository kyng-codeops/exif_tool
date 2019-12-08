import unittest
from datetime import datetime

import exif_tool


class TestIntegration(unittest.TestCase):

    def test_list_one_with(self):
        """
        Integration Test
        correctly parse args and call functions with correct args to:
        correctly list the EXIF date on a file that has an EXIF date
        """

        result = exif_tool.main(['-l', 'test/jelena_dokic.jpg'])
        self.assertEqual(result, 0)

    def test_list_multiple_good_bad(self):
        """
        Integration Test
        correctly parse args and call functions with correct args to:

        list the EXIF date on multiple files that have an EXIF date
        """
        result = exif_tool.main(['--list', 'test/299352.jpg', 'requirements.txt',
                                 'test/none', 'test/gym_drink_ad.jpg'])
        self.assertEqual(result, 0)

    def test_set_one_current_nosec(self):
        exif_tool.main(['--set', '10211423', 'test/oxygen_mag.jpg'])
        result = exif_tool.get_exif_datetime('test/oxygen_mag.jpg')
        current_year = str(datetime.now().year)
        self.assertEqual(result, current_year + ':10:21 14:23:00')

    def test_set_one_current_sec(self):
        exif_tool.main(['-t', '10211423.13', 'test/oxygen_mag.jpg'])
        result = exif_tool.get_exif_datetime('test/oxygen_mag.jpg')
        current_year = str(datetime.now().year)
        self.assertEqual(result, current_year + ':10:21 14:23:13')

    def test_set_one_ccyy_sec(self):
        """
        Integration Test:
        main() parses full datetime arg, runs set_exif_datetime(), compares get_exif_datetime()
        """
        exif_tool.main(['--set', '201710211423.02', 'test/oxygen_mag.jpg'])
        result = exif_tool.get_exif_datetime('test/oxygen_mag.jpg')
        self.assertEqual(result, '2017:10:21 14:23:02')

    def test_set_multiple_yy_nosec(self):
        """
        Integration Test:
        main() parses datetime arg without CC in [[CC]yy] or [.SS] on [file]..[file],
        runs set_exif_datetime(), compares get_exif_datetime() on each [file] [file]
        """
        exif_tool.main(['-t', '1810120101',
                        'test/oxygen_mag.jpg',
                        'test/f18.jpg'])

        current_cc = round(datetime.now().year/100)
        current_yr = str(current_cc) + '18'

        result = exif_tool.get_exif_datetime('test/oxygen_mag.jpg')
        # self.assertEqual(result, '2018:10:12 01:01:00')
        self.assertEqual(result, current_yr + ':10:12 01:01:00')

        result = exif_tool.get_exif_datetime('test/f18.jpg')
        self.assertEqual(result, current_yr + ':10:12 01:01:00')

    def test_set__good_bad_files(self):
        """
        include some bad files in list of files to set, non_image, nonexistent file
        bad files and good files are order independent
        on good files, set dates, integration test alters datetime, and get_exif_datetime confirms good files processed
        """
        current_year = datetime.now().year
        exif_tool.set_exif_datetime('test/tcook.jpg', current_year, 10, 19, 0, 0, 0)
        exif_tool.set_exif_datetime('test/f18.jpg', current_year, 10, 19, 0, 0, 0)

        result = exif_tool.main(['-t', '10211423', 'requirements.txt', 'test/tcook.jpg',
                                 'test/none', 'test/f18.jpg'])
        self.assertEqual(result, 2)

        result = exif_tool.get_exif_datetime('test/tcook.jpg')
        self.assertEqual(result, str(current_year) + ':10:21 14:23:00')
        result = exif_tool.get_exif_datetime('test/f18.jpg')
        self.assertEqual(result, str(current_year) + ':10:21 14:23:00')

    def test_set_bad_indate_alpha(self):
        result = exif_tool.main(['-t', 'SET', 'requirements.txt'])
        self.assertEqual(result, 1)

    def test_set_bad_indate_alphanum_1(self):
        result = exif_tool.main(['-t', 'set20191205.', 'test/tcook.jpg', 'test/f18.jpg'])
        self.assertEqual(result, 1)

    def test_set_bad_indate_alphanum_2(self):
        result = exif_tool.main(['--set', '20191205hhMM.', 'test/tcook.jpg', 'test/f18.jpg'])
        self.assertEqual(result, 1)

    def test_set_bad_indate_rangeout(self):
        result = exif_tool.main(['--set', '201912052460.', 'test/tcook.jpg', 'test/f18.jpg'])
        self.assertEqual(result, 1)


    """
    Note: Currently unable to test '*.jpg' because in a real live shell, the shell expands the wildcard and the script
    actually sees a list of files fully expanded (i.e. without wildcard characters).  Manual testing shows '*.jpg' as
    well as 'C*.jpg' or '*2*.jpg' all expand.  Pattern vs 'isfile' checking in the code to determine if glob should be
    used becomes unnecessary because the shell seems to 'always' expand the wildcard upstream of the python script. 
    """


if __name__ == '__main__':
    unittest.main()
