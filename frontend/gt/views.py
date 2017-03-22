import requests
import json

from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.utils import timezone

from .upload_form import UploadCodeForm
from .models import Problem, Submission


def index(request):
    problem_list = Problem.objects.order_by('pk')
    context = {
        'problem_list': problem_list, 
    }
    return render(request,'gt/index.html',context)

def problem(request, problem_id):
    problem = get_object_or_404(Problem,pk=problem_id)

    user_submissions = []
    correct_submissions = []
    pending_submissions = []
    
    if request.user.is_authenticated:
        user_submissions = Submission.objects.filter(user=request.user, problem=problem)
        correct_submissions = user_submissions.filter(correct=True)
        pending_submissions = user_submissions.filter(processed=False)

        for submission in pending_submissions:
            handle_pending(submission)
    
    complete = (len(correct_submissions) > 0)
    pending = (len(pending_submissions) > 0)
    form = UploadCodeForm()
    
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        success = False
        if form.is_valid():
            success = handle_submission(request.FILES['file'], request.user, problem)
            #return HttpResponseRedirect('/site')
        else:
            print("invalid for some reason")
        
        return render(request,'gt/problem.html',{'problem':problem, 'complete':complete, 'submitted': True,
                                                 'pending': pending, 'form': form, 'success': success})
    else:
        return render(request,'gt/problem.html',{'problem':problem, 'complete':complete, 'submitted': False,
                                                 'pending': pending, 'form': form, 'success': True})

def handle_submission(f, user, problem):
    with open('test.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    eval_server = "http://localhost:5000/"
    upload_files = {'file': open('test.txt', 'rb')}

    try:
        request_response = requests.post(eval_server, files=upload_files, data={'problem_id':problem.id})
    except:
        return False
    
    request_data = json.loads(request_response.text)

    new_submission = Submission(user=user, problem=problem, evaluator_id=request_data['id'],
                                processed=False, correct=False, submit_time=timezone.now())
    new_submission.save()
    print(request_data['id'])
    return True

def handle_pending(submission):
    eval_url = "http://localhost:5000/status/{}".format(submission.evaluator_id)
    request_response = requests.get(eval_url)
    request_data = json.loads(request_response.text)
    if request_data['status'] == "Done":
        submission.processed = True
        if request_data['content'].startswith('-1'):
            submission.correct = False
            print(request_data['output'])
        else:
            submission.correct = True
            print(request_data['output'])
        submission.save()
    print(request_response.text)
    

# LEGACY AND SHOULD BE REMOVED
def handle_uploaded_file(f):
    with open('test.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    eval_server = "http://localhost:5000/"
    upload_files = {'file': open('test.txt', 'rb')}
    request_response = requests.post(eval_server, files=upload_files)
    

def upload(request):
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/site')
        else:
            print("invalid for some reason")
    else:
        form = UploadCodeForm()

    return render(request, 'gt/upload.html', {'form': form})
            
        
