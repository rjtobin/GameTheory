import time
import os

while True:
    did_sleep = False
    for file in os.listdir("store/"):
        if file.startswith("file"):
            time.sleep(0.1)
            did_sleep = True
            index = int(file[4:])
            filesize = os.path.getsize("store/{}".format(file))
            if filesize > 100:
                output = "Yes"
            else:
                output = "No"
            with open("store/res/output{}".format(index), "w") as output_file:
                output_file.write(output)
                output_file.write("\n")
            os.remove("store/{}".format(file))

    if not did_sleep:
        time.sleep(1)

