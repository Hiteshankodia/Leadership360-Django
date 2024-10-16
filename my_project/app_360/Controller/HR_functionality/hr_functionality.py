from django.shortcuts import render
from app_360.ServiceHelper.HrData import HrDataClass
from datetime import datetime

hrdataobj = HrDataClass()


def HRLandingPage(request) : 
    return render(request, 'Hr_pages/landing_page_after_login.html')



def ViewSurveyStatus(request) : 
    company_id = int(request.COOKIES.get('company_id'))
    # company_id = 1
    survey_status_data = hrdataobj.FetchSurveyStatus(company_id)
    context = {
        'survey_status': {
            'participants': survey_status_data['number_of_participant'],
            'departments': survey_status_data['number_of_department'],
            'reporting_managers': survey_status_data['number_of_rm'],
            'peers': survey_status_data['number_of_peer'],
            'subordinates': survey_status_data['number_of_sub']
        }
    }

    return render(request, 'Hr_pages/survey_status.html', context)




def DashboardDownloadButton(request): 
    return render(request, 'Hr_pages/dashboard_download_button.html')


def DownloadReport(request):
    company_id = int(request.COOKIES.get('company_id'))
    # company_id = 1
    download_pdf_survey_details_data = hrdataobj.DownloadPDFSurveyDetails(company_id)
    
    # Process the data for the template
    processed_data = []
    for item in download_pdf_survey_details_data:
        survey_date = datetime.strptime(item['survey_date'], '%Y-%m-%d').strftime('%d-%m-%Y')
        processed_data.append({
            'participant_id' : item['participantid'], 
            'name': item['participantname'],
            'department': item['department'],
            'status': 'Completed' if item['deactivated'] else 'Pending',
            'survey_date': survey_date,
            'download_status': 'Download Now' if  item['deactivated'] else 'Not Completed'
        })

    context = {
        'survey_details': processed_data
    }

    return render(request, 'Hr_pages/download_pdf.html', context)



def JSDashBoard(request) : 
    return render(request, 'Hr_pages/JS_dashboard.html')

