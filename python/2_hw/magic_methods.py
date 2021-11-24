import os.path
import tempfile


class File:
    def __init__(self, path):
        self._path = path
        self._curr = 0

        # create file if it doesn't exist
        if not os.path.exists(path):
            with open(path, 'w'):
                pass

    def __str__(self):
        return os.path.abspath(self._path)

    def __add__(self, other_file):
        path_for_combined_files = os.path.join(tempfile.gettempdir(), 'tmp.txt')
        combined_file = File(path_for_combined_files)
        combined_data = self.read() + other_file.read()
        combined_file.write(combined_data)
        return combined_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self._path, 'r') as f:
            # pointer to current position of file
            f.seek(self._curr)
            _line = f.readline()

            if _line:
                # get current pointer for the future reading
                self._curr = f.tell()
                return _line

            self._curr = 0
            raise StopIteration

    def read(self):
        with open(self._path, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self._path, 'w') as f:
            f.write(text)


path_to_file = '.TEMP'
file_obj_1 = File(path_to_file + '_1')
file_obj_2 = File(path_to_file + '_2')
file_obj_1.write('line 1\n')
file_obj_2.write('line 2\n')
new_file_obj = file_obj_1 + file_obj_2

for line in new_file_obj:
    print(ascii(line))
