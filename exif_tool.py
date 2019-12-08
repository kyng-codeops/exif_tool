#!/Users/esteban/venv/bin/python
#
# Author:   kyng-codeops
# Date:     2019/12/02
# Updated:  2019/12/07
# Version:  1.0

from datetime import datetime
import piexif
import argparse
import sys

# import glob


def set_exif_datetime(file, yr, m, d, hr, mn, sec):
    filename = file
    try:
        exif_dict = piexif.load(filename)
        exif_dict['Exif'] = {
            piexif.ExifIFD.DateTimeOriginal: datetime(yr, m, d, hr, mn, sec).strftime("%Y:%m:%d %H:%M:%S")}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, filename)
        return 0

    except piexif._exceptions.InvalidImageDataError as msg:
        return msg
    except ValueError as msg:
        return msg
    except FileNotFoundError as msg:
        return msg


def get_exif_datetime(file):
    filename = file
    try:
        exif_dict = piexif.load(filename)
        return exif_dict['Exif'][36867].decode('utf-8')

    except KeyError:
        return 'create stamp not found:'
    except FileNotFoundError:
        return 'File does not exist!!'
    except piexif._exceptions.InvalidImageDataError as err:
        return 'Skipped!!: ' + err.args[0]


def main(args):
    parser = argparse.ArgumentParser(description='Set or list the EXIF creation date and time on image files.')
    parser.add_argument('-t', '--set', nargs=1, required=False,

                        help='integer datetime formatted: [[CC]YY]mmddHHMM.[SS]')
    parser.add_argument('-l', '--list', action='store_true', required=False,
                        help='list EXIF dates if they exist')
    parser.add_argument('file', nargs='*',
                        help='file_name or file_name_pattern')

    dt_set = parser.parse_args(args)
    """
    #----No need for glob since the shell on macOS 10.14.6 expands *.jpg to a list of all jpeg files
    
    img_files = []
    if isinstance(dt_set.file, str):
        f_pattern = dt_set.file
        img_files = glob.glob("./" + f_pattern)
    elif isinstance(dt_set.file, list):
        img_files = dt_set.file

    """

    img_files = dt_set.file

    if dt_set.set:
        # Read the Linux/BSD 'touch -t' format [[CC]YY]mmddHHMM.[SS]
        s = dt_set.set[0]
        if '.' in s:
            s, sec = s.split('.')
            if len(sec) > 0:
                sec = int(sec)
            else:
                sec = 0
        else:
            sec = 0

        try:
            if len(s) == 12:
                y = int(s[:4])
                m = int(s[4:6])
                d = int(s[6:8])
                h = int(s[8:10])
                mn = int(s[10:12])
            elif len(s) == 10:
                y = int(s[:2])
                current_year = datetime.now().year
                y = 100*round(current_year/100) + y
                m = int(s[2:4])
                d = int(s[4:6])
                h = int(s[6:8])
                mn = int(s[8:10])
            elif len(s) == 8:
                y = datetime.now().year
                m = int(s[:2])
                d = int(s[2:4])
                h = int(s[4:6])
                mn = int(s[6:8])
            else:
                raise ValueError

        except ValueError as msg:
            print("Error: argument [{}] needs to be time and date integers formatted like [[CC]YY]mmddHHMM[.SS]".
                  format(s))
            if str(msg):
                print("\t{}".format(msg))
            return 1

        set_fail_count = 0

        for f in img_files:
            result = set_exif_datetime(f, y, m, d, h, mn, sec)
            if result == 0:
                print("{}\t{}".format(get_exif_datetime(f), f))
            else:
                set_fail_count += 1
                print("Error: {} while processing file {}".format(result, f))
                if str(type(result)) == '<class \'ValueError\'>':
                    return 1
        return set_fail_count

    elif dt_set.list:
        for f in img_files:
            print("{}\t{}".format(get_exif_datetime(f), f))
        return 0

    return 1


if __name__ == '__main__':
    main(sys.argv[1:])


