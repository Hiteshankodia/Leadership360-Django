
from app_360.ServiceHelper.Teamsurvey import Survey
from django.shortcuts import render, redirect
from app_360.utility.utility import UtilityClass
from app_360.Schema.Team.survey import TeamFetchQuestionSchema
from app_360.Schema.Team.survey import TeamPreviewSurvey, TeamSubmitSurvey

teamsurevyobj = Survey()
utilityobj = UtilityClass()

def FetchQuestions(request, participantid = 0 , teamemberid = 0 , surveyid = 0 , page_number = 1):
    print(page_number, "Page Number")
    print('FetchQuestionS')
    if participantid is None or participantid == 0:
        participantid = int(request.POST.get('hiddenstrpid', participantid))
    print(participantid)
      
    if teamemberid is None or teamemberid == 0 or teamemberid == '':
        teamemberid = int(request.POST.get('hiddentintteammemberid', teamemberid))
    print(teamemberid)

    milestone_message_index = int(request.POST.get('milestone_message_index', '0'))

    if surveyid is None or surveyid == 0 :
        surveyid = int(request.POST.get('hiddenintsurveyid', surveyid))
    print(surveyid)

    if page_number == 1:
        page_number = int(request.POST.get('hiddenpage_number', page_number))
    print(page_number) 

    record_count = 5
    
    miltestone_message_list = teamsurevyobj.FetchMilestoneMessage(surveyid)
    print(f"Milestone Messages: {miltestone_message_list}")

    teamFetchQuestionSchema = TeamFetchQuestionSchema(
        participantid = participantid, 
        surveyid = surveyid, 
        record_count = record_count, 
        no_of_question = 5, 
        page_number = page_number, 
        teammemberid = teamemberid

    )

    question = teamsurevyobj.displayquestions(teamFetchQuestionSchema)
    print(f"Questions: {question}")
    
    show_submit_button = len(question) < record_count
    
    context = {
        'question': question, 
        'surveyid': surveyid,
        'page_number': page_number,
        'show_submit_button': show_submit_button, 
        'message' : miltestone_message_list[milestone_message_index]['message'],
        'miestone_index' : miltestone_message_list[milestone_message_index]['question_count'], 
        'milestone_message_index' : milestone_message_index, 
        'participantid' : participantid,
        'teammemberid' : teamemberid, 
        
    }
    print(page_number, "Page Number")
    if len(question) == 0: 
        print("*" * 100)
        teamPreviewSurvey = TeamPreviewSurvey(
                participantid = participantid, 
                surveyid = surveyid, 
                teammemberid = teamemberid) 
        return PreviewSurvey(request= request, teamPreviewSurvey = teamPreviewSurvey) 
    
    elif  ((int(page_number)-1) * record_count) == context['miestone_index'] :
        print(milestone_message_index) 
        context['milestone_message_index'] += 1 
        return render(request, 'Team/milestone.html', context)
    
    else:
        return render(request, 'Team/survey.html', context)


def SaveAndFetchNextQuestions(request):
    print("SaveAND Fetch NExt Questions!")
    if request.method == 'POST':
        page_number = int(request.POST.get('hiddenpage_number', '1')) + 1 
        participantid = request.POST.get('hiddenstrpid', '')
        surveyid = request.POST.get('hiddenintsurveyid', '1')
        teammemberid = request.POST.get('hiddentintteammemberid')
        
        
        
        question_responses = []

        # Loop through POST data to capture question responses
        for key, value in request.POST.items():
            if key.startswith('rdioAnswer_'):
                question_id = int(key.split('_')[1])
                answer_id = int(value)
                presequence_id = int(request.POST.get(f'hiddenpresequenceid_{question_id}', ) or '0') + 1
                question_responses.append({
                    "questionid": question_id,
                    "answerid": answer_id,
                    "presequencesurveyrequestid":  presequence_id
                })

        # Construct survey data object
        survey_data = {
            "surveyid": surveyid,
            "participantid": participantid,
            "questionresponse": question_responses,
            "teammemberid": teammemberid
        }

        print("Survey Data:", survey_data)
    
        saved_status = teamsurevyobj.TeamSaveSurveyAnswers(survey_data)
        
        if saved_status['StatusCode'] == 1: 
            return FetchQuestions(request,  participantid = participantid , teamemberid = teammemberid , surveyid = surveyid, page_number = page_number) 


def PreviewSurvey(request, teamPreviewSurvey : TeamPreviewSurvey):
    print('PreviewSurvey ')
    print(teamPreviewSurvey)
    preview_survey = teamsurevyobj.TeamPreviewSurvey(teamPreviewSurvey)
    print(preview_survey) 
    
    print("Length of preview survey List", len(preview_survey))
    
    context = {
        'preview_survey_data': preview_survey, 
        'enocded_pid' : teamPreviewSurvey.participantid,  
        'surveyid' : teamPreviewSurvey.surveyid,
        'teammemberid' : teamPreviewSurvey.teammemberid
        
    }

    return render(request, 'Team/survey_preview.html', context = context) 

def SubmitSurvey(request):  
    print("Submit Survey!")
    surveyid = request.POST.get('hiddenintsurveyid')
    participantid = request.POST.get('hiddenstrpid')
    teammemberid = request.POST.get('hiddentintteammemberid')
    print(surveyid)
    print(participantid)
    print(teammemberid)

    teamSubmitSurvey = TeamSubmitSurvey(
            participantid = int(participantid), 
            surveyid = int(surveyid), 
            teammmeberid = int(teammemberid)
        )
    save_survey_status = teamsurevyobj.TeamSubmitSurvey(teamSubmitSurvey)
    print(save_survey_status)
    if save_survey_status['StatusCode'] == 1:
        return render(request, 'Team/AfterSurveyThankyou.html') 
    return render(request, 'Team/AfterSurveyThankyou.html')
