from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)
    
    def save(self, *args, **kwargs):
        # Checks if url begins with youtube/com/watch
        if not self.url.startswith('https://www.youtube.com/watch'):
            raise ValidationError(f'Not a YouTube URL {self.url}')
        
        # Extract the video ID from the URL and store it in the video_id field
        url_components = parse.urlparse(self.url)
        # query_string = parse.parse_qs(url_components.query) # 'v=123456789' -> {'v': ['123456789']}
        # if not query_string:
        #     raise ValidationError("Invalid YouTube URL {self.url}")
        # parameters = parse.parse_qs(query_string, strict_parsing=True)
        parameters = parse.parse_qs(url_components.query)
        v_parameters = parameters.get('v') # return None if no key found, e.g. for a URL like https://www.youtube.com/watch?v=dQw4w9WgXcQ, v_parameters will be ['dQw4w9WgXcQ']
        if not v_parameters: # checking if None or empty list
            raise ValidationError(f"Invalid YouTube URL: missing parameters {self.url}")
        self.video_id = v_parameters[0] # string
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Notes: {self.notes[:200]}, Video ID: {self.video_id}'