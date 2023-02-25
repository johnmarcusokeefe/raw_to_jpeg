import tkinter.filedialog
from tkinter import *
import os
import re
import convertImage
import db
import settings


class mainWindow:

    def __init__(self, master):

        self.master = master
        self.file_count = StringVar()
        self.nef_file_count = StringVar()
        self.tif_file_count = StringVar()
        self.jpg_file_count = StringVar()
        self.input_folder_name = StringVar()
        self.output_folder_name = StringVar()
        #
        so = settings.Settings('settings.json')
        settings_data = so.read_settings()
        #print(settings_data['output_folder'])
        self.input_folder_name.set(settings_data['input_folder'])
        self.output_folder_name.set(settings_data['output_folder'])

        self.file_count.set(str(0))
        self.nef_file_count.set(str(0))
        self.tif_file_count.set(str(0))
        self.jpg_file_count.set(str(0))

        # that directory
        self.count_nef = 0
        self.count_tif = 0
        self.count_jpg = 0
        self.count_tot = 0

        self.input_folder = ""
        self.output_folder = ""


        master.title("Covert files to jpeg")

        self.input_label = Label(mainframe, text="Select Input Folder")
        self.input_label.grid(column=1, row=1)

        self.input_folder_label = Label(mainframe, textvariable=self.input_folder_name)
        self.input_folder_label.grid(column=1, columnspan=2, row=2, padx=10, pady=10)

        self.output_label = Label(mainframe, text="Select Output Folder")
        self.output_label.grid(column=1, row=3)

        self.output_folder_label = Label(mainframe, textvariable=self.output_folder_name)
        self.output_folder_label.grid(column=1, columnspan=2, row=4, padx=10, pady=10)

        self.nef_files_read_label = Label(mainframe, text="Total NEF Files:")
        self.nef_files_read_label.grid(column=1, row=5)

        self.nef_total_files_label = Label(mainframe, textvariable=self.nef_file_count)
        self.nef_total_files_label.grid(column=2, row=5)

        self.tif_files_read_label = Label(mainframe, text="Total TIF Files:")
        self.tif_files_read_label.grid(column=1, row=6)

        self.tif_total_files_label = Label(mainframe, textvariable=self.tif_file_count)
        self.tif_total_files_label.grid(column=2, row=6)

        self.jpg_files_read_label = Label(mainframe, text="Total JPG Files:")
        self.jpg_files_read_label.grid(column=1, row=7)

        self.jpg_total_files_label = Label(mainframe, textvariable=self.jpg_file_count)
        self.jpg_total_files_label.grid(column=2, row=7)
        # total files
        self.files_read_label = Label(mainframe, text="Total Files Read:")
        self.files_read_label.grid(column=1, row=8)

        self.total_files_label = Label(mainframe, textvariable=self.file_count)
        self.total_files_label.grid(column=2, row=8)

        # define buttons
        self.input_file_dialog = Button(mainframe, text="Input Folder", command=self.set_input_folder)
        self.input_file_dialog.grid(column=2, row=1)

        self.output_file_dialog = Button(mainframe, text="Output Folder", command=self.set_output_folder)
        self.output_file_dialog.grid(column=2, row=3)

        self.report_button = Button(mainframe, text="report", command=self.get_report)
        self.report_button.grid(column=1, row=9, padx=10, pady=10)

        self.run_button = Button(mainframe, text="run", command=self.run_conversions)
        self.run_button.grid(column=2, row=9, padx=10, pady=10)

        self.quit_button = Button(mainframe, text="Close", command=master.quit)
        self.quit_button.grid(column=2, row=11, padx=10, pady=10)

    #
    def file_count(self):

        self.total_files_label = Label(mainframe, textvariable=self.file_count)
        self.total_files_label.grid(column=2, row=8)

    def get_report(self):

        convertImage.report(self.input_folder_name.get())


    def set_input_folder(self):

        self.input_folder = tkinter.filedialog.askdirectory()
        # write input to settings
        
        self.input_folder_name.set(self.input_folder)
        # open database
        print("set input folder", self.input_folder)

    def set_output_folder(self):
        self.output_folder = tkinter.filedialog.askdirectory()
        self.output_folder_name.set(self.output_folder)
        print("set output folder", self.output_folder)

    # test function
    def run(self):
        print("folders", self.input_folder, self.output_folder)

    def run_conversions(self):
        print("run conversions")

        print("folders", self.input_folder, self.output_folder)
        # save folders to settings
        setting_values = {
            "input_folder": self.input_folder,
            "output_folder": self.output_folder
        }
        so = settings.Settings('settings.json')
        so.write_settings(setting_values)

        # converts nef to tiff and saves to source folder
        for root_dir, dirs, files in os.walk(self.input_folder):
            print(files)
            for filename in files:

                filename = filename.lower()
                # all files are made lower case for ease of testing
                # nef will be output to the source file so they can be reprocess
                if re.search(".nef", filename):
                    self.count_nef += 1

                    convertImage.convert_nef(root_dir, filename, self.count_nef)

        # converts tiff and copyies jpeg to output
        for root_dir, dirs, files in os.walk(self.input_folder):
            print(files)

            for filename in files:
                self.count_tot += 1
                # calls the file caunt label

                if re.search(".tif", filename) or re.search(".tiff", filename):
                    self.count_tif += 1
                    self.tif_file_count.set(str(self.count_tif))
                    # print(".NEF", re.search(".NEF", filename), root+filename)
                    convertImage.convert_tif(root_dir, filename, self.output_folder, str(self.count_tot))

                if re.search(".jpg", filename) or re.search(".jpeg", filename):
                    self.count_jpg += 1
                    self.jpg_file_count.set(str(self.count_jpg))
                    convertImage.copy_jpg(root, filename, self.output_folder, str(self.count_tot))

                self.file_count.set(str(self.count_tot))

        print("NEF files", self.count_nef) 


if __name__ == "__main__":

    # setup database, and create databases
    db_instance = db.ImageDB("rawtojpg.db")
    db_instance.create_tables()
    db_instance.conn.close()
    so = settings.Settings('settings.json')

    root = Tk()
    mainframe = Frame(root, padx=20, pady=20)
    mainframe.grid(column=0, row=0)
    my_gui = mainWindow(root)
    root.mainloop()
