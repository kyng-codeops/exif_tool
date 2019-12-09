import unittest

import exif_tool


class TestUnits(unittest.TestCase):

    def test_get_exif(self):
        """
        Unit Test: get_exif_datetime() on known file origin date & time
        """
        result = exif_tool.get_exif_datetime('jelena_dokic.jpg')
        self.assertEqual(result, '2002:05:29 13:04:29')

    def test_get_exception_handles(self):
        """
        Unit Test: trigger exceptions list in get_exif_datetime()
        """
        result = exif_tool.get_exif_datetime('gym_drink_ad.jpg')
        self.assertEqual(result, 'create stamp not found:')

        result = exif_tool.get_exif_datetime('null_file.jpg')
        self.assertEqual(result, 'File does not exist!!')

        result = exif_tool.get_exif_datetime('text.txt')
        self.assertEqual(result[:11], 'Skipped!!: ')

    def test_set_jpg(self):
        """
        Unit Test: set a new date & time with set_exif_datetime() and confirm with get_exif_datetime()
        """
        result = exif_tool.set_exif_datetime('299352.jpg', 2016, 5, 15, 16, 0, 5)
        self.assertEqual(result, 0)

        result = exif_tool.get_exif_datetime('299352.jpg')
        self.assertEqual(result, '2016:05:15 16:00:05')

    # TODO: Test WebP files?
    # TODO: Warning when trying to set EXIF origin on TIFF (not supported in piexif.insert())

    """
    First time using unittest. All of these tests are not really unit since success requires multiple
    unit functions to work properly (i.e. these are more like integration tests across functions).

    """


if __name__ == '__main__':
    unittest.main()
