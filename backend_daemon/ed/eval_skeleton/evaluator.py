import sys

def reference_fun(i):
    return i*i

def get_score():
    score = 0
    for i in range(1,10):
        if submission.test_fun(i) == reference_fun(i):
            score += 1
    return score

assigned_status = False
status_code = 0
result_string = ""

try:
    import submission
except Exception as ErrorDetails:
    result_string = "error: {}".format(ErrorDetails)
    status_code = -1
    assigned_status = True

if not assigned_status:
    status_code = get_score()
    result_string = "Success"
    assigned_status = True

with open("/eval_dir/output", "w") as output:
    output.write(str(status_code))
    output.write("\n")
    output.write(result_string)
    output.write("\n")

