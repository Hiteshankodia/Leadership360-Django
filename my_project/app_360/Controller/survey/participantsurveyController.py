from django.shortcuts import render

from app_360.utility.utility import UtilityClass
from app_360.ServiceHelper.ParticipantSurvey import ParticipantSurvey


utilityobj = UtilityClass()
participantobj = ParticipantSurvey()


def CheckStatus(request):
    if request.method == 'POST':
        encoded_pid = request.POST.get('strnameparticipantid', '')
        survey_id = request.POST.get('intnamesurveyid', '')

        print(encoded_pid)
        print(survey_id)

        pid = utilityobj.decrypt(encoded_pid)
        print(pid)

        participant_survey_status = participantobj.FetchSurveyStatus(pid)
        context = {
            'encoded_pid' : encoded_pid, 
            'survey_id' : survey_id
        }

        if participant_survey_status["status"] == 'Completed':
            return render(request, 'Participant/thankyou.html', context = context)
        elif participant_survey_status["status"] == 'In Progress':
            return render(request, 'Survey/survey.html')
        elif participant_survey_status["status"] == 'Assigned':
            return render(request, 'Survey/before_survey.html')




