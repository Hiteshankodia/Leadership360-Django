from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        encoded_pid = request.POST.get('strnameparticipantid', '')
        survey_id = request.POST.get('intnamesurveyid', '')
        context = {

            'encoded_pid': encoded_pid,  
            'survey_id' : survey_id,    
        }  
        print("Index Page!")
        print(encoded_pid)
        print(survey_id)

        return render(request, 'Homepage/homepage.html', context = context)
    else: 
        return render(request, 'Homepage/homepage.html')

def ThanksFrom360(request):
    print("Thanks from 360")
    print("Here!")
    return render(request, 'Homepage/before_survey_hr.html')    