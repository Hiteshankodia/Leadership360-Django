from django.shortcuts import render, redirect
from django.contrib import messages
from app_360.Schema.home import ParticipantForm
from app_360.Schema.ParticipantInviteSchema import ParticipantInviteRequestSchema

def invite(request):  
    form = ParticipantForm(request.POST)
    if form.is_valid():
        print("Invite Controller! ")
        name = request.POST.getlist('name')
        designation = request.POST.getlist('designation')
        department = request.POST.getlist('department')
        location = request.POST.getlist('location')
        email = request.POST.getlist('email')
        dob = request.POST.getlist('dob')
        country = request.POST.getlist('country')
        state = request.POST.getlist('state')

        # Create a dictionary with the fetched lists
        participant_data = {
            'name': name,
            'designation': designation,
            'department': department,  
            'location': location,
            'email': email,
            'dob': dob,  
            'country': country,  
            'state': state  
        }
        schema = ParticipantInviteRequestSchema(**participant_data)
        print("Data validated successfully:")
        print(schema.dict())    
        

            

        #messages.success(request, 'Registration successful!')
        #return redirect('inviteparticipant')  # Replace 'index' with your actual redirect URL name

        # If the request method is GET or form submission failed, render the form again
        return render(request, 'Participant/invite.html')


    