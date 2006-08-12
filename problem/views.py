#coding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.judge.models import Judge
from oj.problem.models import Problem
from oj.volume.models import ProblemVolume
from oj.userprofile.views import userpermitproblem
from django import forms

import datetime

def problemdetail(request, problemid):
    problem = Problem.objects.get(problemid__exact = problemid)
    if not userpermitproblem(request.user, problem):
        errors = {'Permission not allowed':''}
        return render_to_response('errors.html',{'errors':errors})
    return render_to_response('problem/problemdetail.html', {'object':problem, 'user':request.user})

def problemsubmit(request, problemid):
    manipulator = Judge.AddManipulator()
    user = request.user
    problem = Problem.objects.get(problemid__exact = problemid)
    if not userpermitproblem(user, problem):
        errors = {'Permission not allowed':''}
        return render_to_response('errors.html', {'errors':errors})
    
    if(request.POST):
        submittime = datetime.datetime.now()
        result = 'WAIT'
        
        new_data = request.POST.copy()

        new_data['user'] = user.id
        new_data['problem'] = problem.id
        new_data['submittime_date'] = str(submittime.date())
        new_data['submittime_time'] = str(submittime.time().strftime('%H:%M'))
        new_data['result'] = result

        errors = manipulator.get_validation_errors(new_data)
        if errors:
            return render_to_response('errors.html', {'errors': errors})
        else:
            manipulator.do_html2python(new_data)
            manipulator.save(new_data)
            return render_to_response('problem/problemsubmitresult.html', {'user':request.user})
    else:
        errors = {}
        new_data = {'language':'c++'}
        problem = Problem.objects.get(problemid__exact=problemid)
        form = forms.FormWrapper(manipulator, new_data, errors)
        return render_to_response('problem/problemsubmit.html', {'problem':problem, 'form': form, 'user':request.user})

def problemstatus(request, problemid):
    problem = Problem.objects.get(problemid__exact = problemid)
    if not userpermitproblem(request.user, problem):
        errors = {'Permission not allowed':''}
        return render_to_response('errors.html', {'errors':errors})

    judges = Judge.objects.filter(problem__exact = problem)
    return render_to_response('problem/problemstatus.html', {'problem':problem, 'judge_list':judges, 'user':request.user})
