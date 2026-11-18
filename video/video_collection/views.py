from django.shortcuts import redirect, render
from .forms import VideoForm
from django.contrib import messages

def home(request):
    # Logic for the home view will go here
    
    # Set the app name to be displayed in the template in home.html
    app_name = 'Video Collection'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):
    # Logic for adding a video will go here
    
    if request.method == 'POST':
        # Process the submitted form data
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            # Save the new video to the database
            new_video_form.save()
            messages.success(request, 'Video added successfully!')
            # TODO: Add a success message or redirect to a success page
        else: 
            # If the form is not valid, render the form with error messages
            messages.error(request, 'Please check the data you entered and try again.')
            return render(request, 'video_collection/add.html', {'form': new_video_form})
    
    # Create a new instance of the VideoForm
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'form': new_video_form})