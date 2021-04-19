from os.path import abspath
from time import time
from pathlib import Path
from argparse import ArgumentParser, Namespace

_END_FILE_NAME = 'result_1.jsonl'


class LogMerger:

    def __init__(self, first_file_path, second_file_path, result_file_dir):
        self.end_file = result_file_dir.joinpath(_END_FILE_NAME)
        self.log_1 = first_file_path
        self.log_2 = second_file_path

        self.file_log_a = None
        self.file_log_b = None
        self.result_file = None

        self.lines_in_first = None
        self.lines_in_second = None
        # if string_to_search in first[1]:
        #     print(first[1].split(string_to_search)[1].split('"')[0])


    def open_files(self):
        self.file_log_a = open(self.log_1, 'r')
        self.file_log_b = open(self.log_2, 'r')
        self.result_file = open(self.end_file, 'w')

        # for readlines
        # we could take only one line, but we don't need to cause of log files size (small enough)
        # self.lines_in_first = self.file_log_a.readlines()
        # self.lines_in_second = self.file_log_b.readlines()

    def close_files(self):
        self.file_log_a.close()
        self.file_log_b.close()
        self.result_file.close()

    def rude_merge(self):
        self.open_files()

        # We will be needed some variables, so start it bellow
        string_to_search = 'timestamp": "'

        end_first_file = False
        end_second_file = False
        string_from_first = None
        string_from_second = None
        take_first = True
        take_second = True

        # for readlines
        # i, j = 0, 0
        # len_first = len(self.lines_in_first)
        # len_second = len(self.lines_in_second)

        while True:  # бесконечные циклы не безопасны, но для данного случая это может быть быстрее
            # if first file still have elements and there is a call for new element => take it
            if end_first_file is False and take_first:
                # using readline
                string_from_first = self.file_log_a.readline()
                if string_from_first == '':
                    end_first_file = True
                    string_from_first = None
                # using readlines and know len
                # if i < len_first:
                #     string_from_first = self.lines_in_first[i]
                #     i += 1
                # else:
                #     end_first_file = True
                #     string_from_first = None
                # using readlines and don't know len try-except style
                # try:
                #     string_from_first = self.lines_in_first[i]
                #     i += 1
                # except IndexError:
                #     end_first_file = True
                #     string_from_first = None
                take_first = False
            # same
            if end_second_file is False and take_second:
                string_from_second = self.file_log_b.readline()
                if string_from_second == '':
                    end_second_file = True
                    string_from_second = None

                # if j < len_second:
                #     string_from_second = self.lines_in_second[j]
                #     j += 1
                # else:
                #     end_second_file = True
                #     string_from_second = None

                # try:
                #     string_from_second = self.lines_in_second[j]
                #     j += 1
                # except IndexError:
                #     end_second_file = True
                #     string_from_second = None
                take_second = False

            # Остановка цикла, потому что все элементы пройдены
            if end_second_file and end_first_file:
                break

            # if one of strings from file is None => left only other files string, so focusing on it
            if string_from_first is None:
                self.result_file.write(string_from_second)
                take_second = True
                continue
            if string_from_second is None:
                self.result_file.write(string_from_first)
                take_first = True
                continue

            # Some checks if line don't have timestamp we will ignore it
            if string_to_search in string_from_first:
                first_timestamp = string_from_first.split(string_to_search)[1].split('"')[0]
            else:
                take_first = True
                continue
            if string_to_search in string_from_second:
                second_timestamp = string_from_second.split(string_to_search)[1].split('"')[0]
            else:
                take_second = True
                continue

            # so we have YYYY-MM-DD HH:MM:SS format. For this format we even don't need to transfer data to
            # datetime, ordinary string comparison will work fine. Still, we can switch type and compare purely
            # first_timestamp = datetime.datetime.strptime(first_timestamp, "%Y-%m-%d %H:%M:%S")
            # second_timestamp = datetime.datetime.strptime(second_timestamp, "%Y-%m-%d %H:%M:%S")

            # hard checking which date goes first. If equivalent => first file goes first
            if first_timestamp > second_timestamp:
                self.result_file.write(string_from_second)
                take_second = True
            elif first_timestamp == second_timestamp:
                self.result_file.write(string_from_first)
                self.result_file.write(string_from_second)
                take_second, take_first = True, True
            elif first_timestamp < second_timestamp:
                self.result_file.write(string_from_first)
                take_first = True

        self.close_files()


def _parse_args() -> Namespace:
    parser = ArgumentParser(description='Tool to generate test logs.')

    parser.add_argument(
        '-first_file_path',
        metavar='<FIRST FILE PATH>',
        type=str,
        default=abspath('./logs/log_a.jsonl'),
        help='path to log_a',
    )

    parser.add_argument(
        '-second_file_path',
        metavar='<SECOND FILE PATH>',
        type=str,
        default=abspath('./logs/log_b.jsonl'),
        help='path to log_b',
    )

    parser.add_argument(
        '-result_file_dir',
        metavar='<RESULT FILE DIR>',
        type=str,
        default=abspath('./logs/'),
        help='result file dir',
    )

    return parser.parse_args()


def take_max_len():
    t0 = time()
    # TBD
    print(f"finished in {time() - t0:0f} sec")


def main_rude():
    args = _parse_args()
    first_file_path = Path(args.first_file_path)
    second_file_path = Path(args.second_file_path)
    result_file_dir = Path(args.result_file_dir)
    t0 = time()
    merge_me = LogMerger(first_file_path, second_file_path, result_file_dir)
    merge_me.rude_merge()
    print(f"finished in {time() - t0:0f} sec")


if __name__ == '__main__':
    main_rude()
