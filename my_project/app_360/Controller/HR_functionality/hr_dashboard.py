from django.shortcuts import render
from app_360.ServiceHelper.HrData import HrDataClass
import pandas as pd 
from django.http import JsonResponse

hrdataobj = HrDataClass()


def JSDashBoard(request, company_id = 1):
    company_id = int(request.COOKIES.get('company_id'))
    data = hrdataobj.HRDashboardData(company_id)
    df = pd.DataFrame(data['data'])
    # print(df)
    
    dimension_list = ['Coaching & Feedback', 'Empowering', 'Team Building', 'Emotional Intelligence', 'Integrity', 'Tenacity and Courage', 
    'Ability to Execute', 'Change Orientation', 'Energizing', 'Visioning', 'Client & Stakeholders','Network & Alliances']
    
    # Filter rows where 'dimensionname' is in the dimension_list
    filtered_df = df[df['dimensionname'].isin(dimension_list)]
    
    grouped_df = filtered_df.groupby('dimensionname').agg({
        'participantaverage': 'mean',  
        'peeraverage': 'mean',         
        'subordinateaverage': 'mean',  
        'reportingmanageraverage': 'mean'  
    }).reset_index()
    # print(grouped_df)
    data_json = grouped_df.to_json(orient='records')
    # grouped_df.to_csv('organisation_wise.csv', index=True)
    unique_df = df[['participantname', 'participantid']].drop_duplicates()
    # unique_df.to_csv('participants_button.csv', index = True)
    # Convert to list of dictionaries
    participants = unique_df.to_dict('records')
    
    department_list = df['department'].drop_duplicates().tolist()
    
    context = {
        'data': data_json,  
        'participants': participants, 
        'department' :  department_list 

        }

    # Render the template with the context
    return render(request, 'Hr_pages/JS_dashboard.html', context)
     
def participant_wise(request, participant_id):
    company_id = int(request.COOKIES.get('company_id'))
    data = hrdataobj.HRDashboardData(company_id)
    df = pd.DataFrame(data['data'])
    dimension_list = ['Coaching & Feedback', 'Empowering', 'Team Building', 'Emotional Intelligence', 'Integrity', 'Tenacity and Courage', 
    'Ability to Execute', 'Change Orientation', 'Energizing', 'Visioning', 'Client & Stakeholders','Network & Alliances']
    
    # Filter rows where 'dimensionname' is in the dimension_list
    filtered_df = df[df['dimensionname'].isin(dimension_list)]
    df_participant = filtered_df[filtered_df['participantid'] == participant_id]
    relevant_columns = df_participant[['participantname', 'participantid', 'dimensionname', 
                       'participantaverage', 'peeraverage', 
                       'subordinateaverage', 'reportingmanageraverage']]

    # Step 2: Group by 'dimensionname' and calculate the mean for the specified columns
    grouped_df = relevant_columns.groupby('dimensionname').agg({
        'participantaverage': 'mean',
        'peeraverage': 'mean',
        'subordinateaverage': 'mean',
        'reportingmanageraverage': 'mean'
    }).reset_index()
    # grouped_df.to_csv('participant_wise.csv', index=True)
    
    return JsonResponse(grouped_df.to_json(orient='records'), safe=False)
    
def department_wise(request, department_name) : 
    print(department_name)
    company_id = int(request.COOKIES.get('company_id'))
    data = hrdataobj.HRDashboardData(company_id)
    df = pd.DataFrame(data['data'])
    dimension_list = ['Coaching & Feedback', 'Empowering', 'Team Building', 'Emotional Intelligence', 'Integrity', 'Tenacity and Courage', 
    'Ability to Execute', 'Change Orientation', 'Energizing', 'Visioning', 'Client & Stakeholders','Network & Alliances']
    
    # Filter rows where 'dimensionname' is in the dimension_list
    df = df[df['dimensionname'].isin(dimension_list)]
    df_department = df[df['department'] == department_name]
    relevant_columns = df_department[['dimensionname', 'participantaverage', 
                       'peeraverage', 'reportingmanageraverage', 
                       'subordinateaverage']]

    # Group by 'dimensionname' and calculate the mean for the specified columns
    grouped_df = relevant_columns.groupby('dimensionname').agg({
        'participantaverage': 'mean',
        'peeraverage': 'mean',
        'reportingmanageraverage': 'mean',
        'subordinateaverage': 'mean'
    }).reset_index()
    # grouped_df.to_csv('department_wise.csv', index=True)

    
    return JsonResponse(grouped_df.to_json(orient='records'), safe=False)



