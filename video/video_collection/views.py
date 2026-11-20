from django.shortcuts import redirect, render
from .forms import VideoForm, SearchForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.contrib import messages
from .models import Video

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
            try:
                # Save the new video to the database
                new_video_form.save()
                return redirect('video_list')
                # messages.success(request, 'Video added successfully!')
            # TODO: Add a success message or redirect to a success page
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already added this video')
        # If the form is not valid, render the form with error messages
        messages.error(request, 'Please check the data you entered and try again.')
        return render(request, 'video_collection/add.html', {'form': new_video_form})
    
    # Create a new instance of the VideoForm
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'form': new_video_form})

def video_list(request):
    # Logic for displaying the list of videos will go here
    
    search_form =SearchForm(request.GET) # build form from data user has sent to app
    
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term'] # example: 'yoga' or 'squats'
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))
        
    else: # form is not filled in or this is the first time the user sees the page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))
    
    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form} )