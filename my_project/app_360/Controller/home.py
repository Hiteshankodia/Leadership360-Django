from django.shortcuts import render
from app_360.ServiceHelper.AuthServiceHelper import AuthServiceHelper 
from django.shortcuts import HttpResponse
from app_360.utility.utility import UtilityClass

utilityobj = UtilityClass()
authobj = AuthServiceHelper()

def index(request):
    response = HttpResponse(render(request, 'Homepage/homepage.html'))
    for cookie in request.COOKIES:
            response.delete_cookie(cookie)
    
    if request.method == 'POST':
        response = HttpResponse(render(request, 'Homepage/homepage.html'))
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        
        encoded_pid = request.POST.get('strnameparticipantid', '')
    
        survey_id = request.POST.get('intnamesurveyid', '')
        
        
        
        context = {

            'encoded_pid': encoded_pid,  
            'survey_id' : survey_id,    
        }  

        
        
        
        url = request.build_absolute_uri()
        


        return render(request, 'Homepage/homepage.html', context = context)
    
    else:
        print("Else Part")
        response = HttpResponse(render(request, 'Homepage/homepage.html'))
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
         
        company_id = None

        
        company_id_json = request.COOKIES.get('company_id')
        
        if not company_id_json:
            print("above FetchCompnayid()")
            # Cookie not present, fetch company ID
            url = request.build_absolute_uri()
            print('myurl', url) 
            response_data = authobj.FetchCompanyid(url) 
             # Assuming this returns a dict or similar structure
            company_id = response_data.get('companyid')
            
            # Create an HttpResponse object
            response = HttpResponse(render(request, 'Homepage/homepage.html', {'company_id': company_id}))
            
            # Set the cookie in the response
            response.set_cookie('company_id', str(company_id))
             
            
            
            return response

        # Ensure company_id has a value before using it
        try:
            encoded_pid = request.POST.get('strnameparticipantid', '')
            survey_id = request.POST.get('intnamesurveyid', '') 
            
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

        company_id = request.COOKIES.get('company_id')
        print("browser Session companyid", company_id)
        return render(request, 'Homepage/homepage.html', context=context)


def ThanksFrom360(request):
    
    return render(request, 'Homepage/before_survey_hr.html')    