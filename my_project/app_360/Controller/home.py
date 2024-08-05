from django.shortcuts import render
from app_360.ServiceHelper.AuthServiceHelper import AuthServiceHelper 
from django.shortcuts import HttpResponse
from app_360.utility.utility import UtilityClass

utilityobj = UtilityClass()
authobj = AuthServiceHelper()

def index(request):
    if request.method == 'POST':
        '''encoded_pid = request.POST.get('strnameparticipantid', '')
        survey_id = request.POST.get('intnamesurveyid', '')

        context = {

            'encoded_pid': encoded_pid,  
            'survey_id' : survey_id,    
        }  
        print("Index Page!")
        print(encoded_pid)
        print(survey_id)
        
        url = request.build_absolute_uri()
        print(url)
        print('If part!')

'''

        return render(request, 'Homepage/homepage.html', context = context)
    
    else:
        # Initialize company_id to avoid UnboundLocalError
        company_id = None

        # Check for the cookie
        company_id_json = request.COOKIES.get('company_id')
        
        if not company_id_json:
            # Cookie not present, fetch company ID
            url = request.build_absolute_uri()
            response_data = authobj.FetchCompanyid(url)  # Assuming this returns a dict or similar structure
            company_id = response_data.get('companyid')
            
            # Create an HttpResponse object
            response = HttpResponse(render(request, 'Homepage/homepage.html', {'company_id': company_id}))
            
            # Set the cookie in the response
            response.set_cookie('company_id', str(company_id))
            
            # Debugging information
            print('Cookie set:', response.cookies)
            print('Company ID:', company_id)
            
            return response

        # Ensure company_id has a value before using it
        try:
            context = {
                'encoded_pid': encoded_pid,  
                'survey_id': survey_id,    
                'companyid': company_id
            }
        except:
            context = {
                'companyid': company_id
            }

        # Return the rendered template with context
        return render(request, 'Homepage/homepage.html', context=context)


def ThanksFrom360(request):
    print("Thanks from 360")
    print("Here!")
    return render(request, 'Homepage/before_survey_hr.html')    