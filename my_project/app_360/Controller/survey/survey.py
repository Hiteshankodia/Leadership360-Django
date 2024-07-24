from app_360.ServiceHelper.survey import Survey
from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.utility.utility import UtilityClass
from django.shortcuts import render
from django.http import JsonResponse
from app_360.Schema.Participant.save_survey import SaveQuestionRequestSchema, QuestionRequestSchema, AnswerSchema

surveyobj = Survey()
utilityobj = UtilityClass()


def displayquestions(request):  
    if request.method == 'POST':
        page_number = int(request.POST.get('page_number', '1')) 
        encodedpid = request.POST.get('strnameparticipantid', '')
        surveyid = request.POST.get('intnamesurveyid', '')
        
        fetchQuestionRequestSchema = FetchQuestionRequestSchema(
            participantid=3,  
            surveyid=1,  
            record_count=5,  
            no_of_question=5, 
            page_number=page_number  
        )
        
        question = surveyobj.displayquestions(fetchQuestionRequestSchema)
        
        selected_answers = {}
        
        for obj in question:
            question_id = obj['questionid']
            
           
            radio_button_name = f'rdioAnswer_9' #{question_id}'  # This needs to match your template
            
            
            selected_answer_id = request.POST.get(radio_button_name, '')  # Correct way to retrieve
            print(f'Selected answer for question {question_id}: {selected_answer_id}')
            
            selected_answers[question_id] = selected_answer_id
        
        #print('All selected answers:', selected_answers)
        
        next_page_number = page_number + 1
        show_next_button = len(question) >= 5
        
        context = {
            'question': question,
            'page_number': next_page_number,
            'encodedpid': encodedpid,
            'surveyid': surveyid,
            'show_next_button': show_next_button,
            'selected_answers': selected_answers  # Pass selected answers to the template
        }
        
        return render(request, 'Survey/survey2.html', context)

def SaveAnswer(request, question=None):
    print("Save Answer Method")
    if question is not None:
        selected_answers = {}
        for obj in question:
            question_id = obj['questionid']
            
            # Construct the name of the radio button input field dynamically
            radio_button_name = f'{question_id}' #{question_id}'  # This needs to match your template
            
            # Retrieve the selected answer ID from POST data
            selected_answer_id = request.POST.get(radio_button_name, '')  # Correct way to retrieve
            print(f'Selected answer for question {question_id}: {selected_answer_id}')
            
            selected_answers[question_id] = selected_answer_id
        
        print('All selected answers:', selected_answers)
     
        displayquestions(request)

def save_survey_answers(request):
    data = [{'questionid': 9, 'answerid': None, 'question': 'I always act on client/stakeholder feedback to ensure their satisfaction\n', 'answer': [{'answerid': 1, 'answer': 'Strongly Agree'}, {'answerid': 2, 'answer': 'Agree '}, {'answerid': 3, 'answer': 'Neutral'}, {'answerid': 4, 'answer': 'Disagree'}, {'answerid': 5, 'answer': 'Strongly Disagree'}], 'presequence_survey_id': 65}, {'questionid': 4, 'answerid': None, 'question': "I hold myself accountable for meeting my organization's objectives\n", 'answer': [{'answerid': 1, 'answer': 'Strongly Agree'}, {'answerid': 2, 'answer': 'Agree '}, {'answerid': 3, 'answer': 'Neutral'}, {'answerid': 4, 'answer': 'Disagree'}, {'answerid': 5, 'answer': 'Strongly Disagree'}], 'presequence_survey_id': 66}, {'questionid': 3, 'answerid': None, 'question': 'I am good at ensuring resources are available to accomplish organizational objectives\n', 'answer': [{'answerid': 1, 'answer': 'Strongly Agree'}, {'answerid': 2, 'answer': 'Agree '}, {'answerid': 3, 'answer': 'Neutral'}, {'answerid': 4, 'answer': 'Disagree'}, {'answerid': 5, 'answer': 'Strongly Disagree'}], 'presequence_survey_id': 67}, {'questionid': 10, 'answerid': None, 'question': 'I work closely with our clients/stakeholders in order to best meet their needs\n', 'answer': [{'answerid': 1, 'answer': 'Strongly Agree'}, {'answerid': 2, 'answer': 'Agree '}, {'answerid': 3, 'answer': 'Neutral'}, {'answerid': 4, 'answer': 'Disagree'}, {'answerid': 5, 'answer': 'Strongly Disagree'}], 'presequence_survey_id': 68}, {'questionid': 5, 'answerid': None, 'question': 'I hold others accountable for their organizational commitments and deadlines\n', 'answer': [{'answerid': 1, 'answer': 'Strongly Agree'}, {'answerid': 2, 'answer': 'Agree '}, 
{'answerid': 3, 'answer': 'Neutral'}, {'answerid': 4, 'answer': 'Disagree'}, {'answerid': 5, 'answer': 'Strongly Disagree'}], 'presequence_survey_id': 69}]
    
    save_request_data = SaveQuestionRequestSchema(
    surveyid=1,
    participantid=3,
    questionresponse=[
        QuestionRequestSchema(
            questionid=item['questionid'],
            question=item['question'],
            answers=[
                AnswerSchema(answerid=ans['answerid'], answer=ans['answer']) for ans in item['answer']
            ],
            presequencesurveyrequestid=item['presequence_survey_id']
        ) for item in data
    ]
)


def SubmitParticipantSurvey(request):
    participantid = 3 
    surveyid = 1

    submitParticipantSurveyRequestSchema = SubmitParticipantSurveyRequestSchema(
        participantid=participantid,
        surveyid=surveyid
    )
    
    surveyobj.SubmitParticipantSurvey(submitParticipantSurveyRequestSchema)

    