"""
URL configuration for project_360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from app_360 import views 
from app_360.Controller import home
from app_360.Controller import authcontroller
from app_360.Controller.Participant import invite
from app_360.Controller.survey import survey_, teamsurvey
from app_360.Controller.Participant import Sample
from app_360.Controller.Participant import participantsurvey
from app_360.Controller.Team import inviteTeam
from app_360.utility.utility import UtilityClass
from app_360.views import set_participant_id, get_participant_id
urlpatterns = [
         
    path("admin/", admin.site.urls),
    path('auth', authcontroller.auth, name = 'auth'),  
    path('', home.index, name = 'index'), 
    path('thanksfrom360/', home.ThanksFrom360, name = 'thanksfrom360'), 
    path('participantinvite/', invite.ParticipantDeatils, name = 'participantinvite'),
    #path('inviteparticipant/', inviteController.invite, name='inviteparticipant'),
    path('load_states', invite.load_states, name='load_states'), 
    path('save_data/', invite.save_data, name = 'save_data'), 
    path('participantinvitesent/', invite.ParticipantInvite, name = 'participantinvitesent'), 
    path('participantexist/', participantsurvey.fetchparticipantid, name='fetchparticipantid'),
    path('setpassword/', participantsurvey.setpassword, name = 'setpassword'),
    path('save_password/', participantsurvey.save_password, name = 'save_password'),
    path('displayquestions/', survey_.FetchQuestions, name = 'displayquestions'), 
    path('saveandfetchnextquestions/', survey_.SaveAndFetchNextQuestions, name = 'saveandfetchnextquestions'), 
    path('previewsurvey/', survey_.PreviewSurvey, name = 'previewsurvey'), 
    path('submitsurvey/', survey_.SubmitSurvey, name = 'submitsurvey'), 
    path('beforesubmitinvite/', inviteTeam.Beforeinvite, name = 'beforesubmitinvite'),
    path('teaminvite/', inviteTeam.TeamFormDetails, name = 'teaminvite'), 
    path('teamsavedata/', inviteTeam.SaveData, name = 'teamsavedata'),   
    path('load_state_team', inviteTeam.load_states, name='load_state_team'), 
    path('teaminvitesend/', inviteTeam.TeamInvite, name = 'teaminvitesend'), 
    path('teamdisplayquestions/', teamsurvey.TeamFetchQuestions, name = 'teamdisplayquestions'),
    path('teamsaveandfetchnextquestions/', teamsurvey.SaveAndFetchNextQuestions , name = 'teamsaveandfetchnextquestions'),
    path('teampreviewsurvey/', teamsurvey.PreviewSurvey, name = 'teampreviewsurvey'),
    path('teamsubmitsurvey/', teamsurvey.SubmitSurvey, name = 'teamsubmitsurvey'), 
    path('auth/teamtoken/', authcontroller.TeamMemberAssignSurvey, name = 'teammemberverify'),
    path('set-participant-id/<int:participantid>/', set_participant_id),
    path('get-participant-id/', get_participant_id),
    path('participant_survey_after_invite/', authcontroller.ParticipantSurveyAfterInvite, name = 'participant_survey_after_invite')

  
  
] 

