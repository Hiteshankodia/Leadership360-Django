from django.http import HttpResponse
from django.shortcuts import render

def set_participant_id(request, participantid: int):
    response = HttpResponse("Cookie is set!")
    response.set_cookie('participantid', participantid, max_age=3600)
    return response

def get_participant_id(request):
    participant_id = request.COOKIES.get('participantid')
    if participant_id:
        response_text = str(participant_id)
    else:
        response_text = "2"
    return HttpResponse(response_text) 

