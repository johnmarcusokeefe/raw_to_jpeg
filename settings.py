import json
import os


class Settings:

    def __init__(self, filename):

        self.filename = filename
        path = os.getcwd()
        self.out_file = os.path.join(path, filename)


    def write_settings(self, in_value):

        with open(self.out_file, 'w') as outfile:
            json.dump(in_value, outfile)
        # create file
        outfile.close()


    def read_settings(self):

        print(self.out_file)
        with open(self.out_file, 'r') as out:

            return json.loads(out.read())
