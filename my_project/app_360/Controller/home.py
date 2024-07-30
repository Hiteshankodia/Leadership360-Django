from django.shortcuts import render


def index(request):
    return render(request, 'Homepage/homepage.html')
    

def ThanksFrom360(request):
    print("Thanks from 360")
    return render(request, 'Homepage/before_survey_hr.html')    