from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    problem_title       = models.CharField(max_length=200)
    problem_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.problem_title

class Submission(models.Model):
    user         = models.ForeignKey(User, on_delete = models.CASCADE)
    problem      = models.ForeignKey(Problem, on_delete = models.CASCADE)
    evaluator_id = models.IntegerField()
    submit_time  = models.DateTimeField()
    processed    = models.BooleanField()
    correct      = models.BooleanField()


    def __str__(self):
        if self.correct:
            correct = "Correct"
        else:
            correct = "Incorrect"

        if self.processed:
            processed = "Processed"
        else:
            processed = "Not processed"
            
        return "{}, {}, {}, {}".format(self.user.username, self.problem.problem_title,
                                       processed, correct)

    
