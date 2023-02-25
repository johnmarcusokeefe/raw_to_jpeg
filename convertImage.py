from PIL import Image
import pyunraw
import shutil
import os.path
import hashlib
import db


def report(input_folder):

    for root_dir, dirs, files in os.walk(input_folder):
        print(files)
        for filename in files:

            filename = filename.lower()
            file_saved = 0
            db_instance = db.ImageDB("rawtojpg.db")
            # add to hash record
            # create hash from file
            hash_in = create_hash(os.path.join(root_dir,filename))
            # check if saved
            is_hash = db_instance.read_hash(hash_in)
            print(is_hash[0][0])
            # if hash exists write report
            if is_hash[0][0] == 0:
                print("hash written", is_hash)
                db_instance.write_hash_to_db(hash_in, file_saved)
            else:
                print(is_hash)
                saved_flag = db_instance.get_saved_flag(hash_in)
                print("hash exists, saved flag is",saved_flag[0][1] )


            db_instance.conn.close()

def create_hash(file_name):

    with open(file_name,"rb") as f:
        image = f.read()

        sh1hash = hashlib.sha1(image).hexdigest()
        #print("sha1 hash", file_name, sh1hash)

        return sh1hash


#
# convert raw
#
def convert_nef(directory, filename, num):

    try:

        dir_file = os.path.join(directory, filename)
        out_filename = str(num) + "-" + filename
        out_file = os.path.join(directory, out_filename)

        raw = pyunraw.PyUnraw(dir_file)
        # test
        print("raw test", raw.is_raw)
        # prints exif for info
        for key, value in raw.data.items():
            print(" %-20s%s" % (key, str(value)))
        # output to source file
        raw.unraw(0, out_file)
        hash_value = create_hash(dir_file)
        print("hash",hash_value)


        print("raw outfile name", raw.out_filename)

    except Exception as e:

        print("raw image failed to convert nef", str(e))


#
# convert tif
#
def convert_tif(directory, filename, output_folder, seq):

    filename_split = filename.split(".")
    dir_file_out = output_folder+"/"+seq+"-"+filename_split[0] + ".jpg"

    try:

        dir_file = os.path.join(directory, filename)
        with Image.open(dir_file) as im:
            print(im.getexif())
            # icc and exif have to be extracted and added as they seem to be removed by default by save
            im.save(dir_file_out, format='JPEG', quality=100, subsampling=0,
                    icc_profile=im.info.get('icc_profile'), exif=im.getexif())

    except Exception as e:

        print("file failed to convert tif", str(e))


#
# copy jpeg
#
def copy_jpg(directory, filename, output_folder, seq):

    try:

        dir_file = os.path.join(directory, filename)
        # shutil.copy2 preserves exif
        shutil.copy2(dir_file, output_folder+"/"+seq+"-from_jpg-"+filename)

    except Exception as e:

        print("file failed to write jpg", str(e))
