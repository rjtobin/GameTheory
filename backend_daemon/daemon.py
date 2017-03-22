import time
import os
import shutil

import subprocess

def evaluate_submission(submission_id, problem_id):
    filename = "store/file{}_{}".format(submission_id, problem_id)
    eval_dir_name = "ed/ed{}_{}".format(submission_id, problem_id)
    shutil.copytree("ed/eval_skeleton",eval_dir_name)
    shutil.copy(filename,"{}/submission.py".format(eval_dir_name))

    command = "docker run -v `pwd`/{}:/eval_dir ub-py python3 /eval_dir/evaluator.py".format(eval_dir_name, submission_id)
    subprocess.call(command, shell="True")
    

    shutil.copy("{}/output".format(eval_dir_name,submission_id), "store/res/output{}".format(submission_id))

    

while True:
    did_sleep = False
    for file in os.listdir("store/"):
        if file.startswith("file"):

            ids = file[4:].split('_')

            if len(ids) != 2:
                print("Filename does not match the expected format...")
                continue
            
            print("got file: {} {}".format(ids[0], ids[1]))
            print(ids)
            
            time.sleep(0.1)
            did_sleep = True
            index = int(ids[0])

            #filesize = os.path.getsize("store/{}".format(file))
            #if filesize > 100:
            #    output = "Yes"
            #else:
            #    output = "No"
            #with open("store/res/output{}".format(ids[0]), "w") as output_file:
            #    output_file.write(output)
            #    output_file.write("\n")

            evaluate_submission(ids[0], ids[1])
            
            os.remove("store/{}".format(file))

    if not did_sleep:
        time.sleep(1)

