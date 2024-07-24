from django.shortcuts import render
from django.http import JsonResponse
from pydantic import BaseModel
from typing import List

class ParticipantSchema(BaseModel):
    name: List[str]
    email: List[str]

def SampleFunction(request):
    if request.method == 'POST':
        try:
            form_data = {
                'name': request.POST.getlist('name'),
                'email': request.POST.getlist('email'),
            }
            
            # Validate the form data against the Pydantic schema
            form = ParticipantSchema(**form_data)
            
            # At this point, form is a validated Pydantic object
            # You can access its attributes like form.name, form.email, etc.
            
            # Example of printing the validated data
            print("Invite Controller! ")
            print(form.dict())
            
            # For demonstration, return a success message
            return JsonResponse({'message': 'Form data validated successfully'})
        
        except Exception as e:
            # Handle validation errors or other exceptions
            print(f"Error: {str(e)}")
            return JsonResponse({'error': 'Form data validation failed'}, status=400)
    
    # Handle GET requests or other cases where form submission is not POST
    return render(request, 'Participant/sample.html')