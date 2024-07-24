from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.ServiceHelper.survey import Survey
from django.shortcuts import render, redirect
from app_360.Schema.Participant.save_survey import SaveQuestionRequestSchema, QuestionRequestSchema
from app_360.Schema.Participant.preview_survey import PreviewParticipantSurvey, SaveParticipantSurvey
from app_360.utility.utility import UtilityClass

surveyobj = Survey()
utilityobj = UtilityClass()


def FetchQuestions(request, page_number1 = 1, survey_id = 1, encoded_pid = ''):
    if encoded_pid == '':
        encoded_pid = request.POST.get('hiddenstrpid')
    if not survey_id == 1: 
        survey_id = request.POST.get('hiddenintsurveyid')
    if not page_number1 == 1: 
        page_number = int(request.POST.get('hiddenpage_number' , '1'))
    
    record_count = 5
    participant_id = utilityobj.decrypt(encoded_pid)


    #Fetch Milestone Message
    miltestone_message_list = surveyobj.FetchMilestoneMessage(survey_id)
    print(f"Milestone Messages: {miltestone_message_list}")

    #Fetch Questions for survey
    fetchQuestionRequestSchema = FetchQuestionRequestSchema(
        participantid=participant_id,
        surveyid=survey_id,
        record_count=record_count,
        no_of_question=5,
        page_number=next_page
    )

    question = surveyobj.displayquestions(fetchQuestionRequestSchema)
    print(f"Questions: {question}")


    context = {
        'question': question,
        'encodedpid': encoded_pid,
        'surveyid': survey_id,
        'page_number': page_number
        #'show_submit_button': show_submit_button, 
        #'message' : miltestone_message_list[milestone_message_index]['message']
    }
    
    #Render Questions to survey html page
    return render(request, 'Survey/survey2.html', context)
 
  
def SaveAndFetchNextQuestions(request):
    page_number = int(request.POST.get('hiddenpage_number')) 
    enocded_pid = request.POST.get('hiddenstrpid')
    surveyid = request.POST.get('hiddenintsurveyid')
    print(page_number)
    print(enocded_pid)
    print(surveyid)
      
    page_number += 1 
  
    #Save Survey Logic 


    FetchQuestions(request= request, page_number1 = page_number, survey_id=surveyid, encoded_pid= enocded_pid) 
