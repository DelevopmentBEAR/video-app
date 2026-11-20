from django.test import TestCase
from django.urls import reverse
from .models import Video
from django.contrib.messages import get_messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Tests if home page has the name of "Video Collection" is there or not
class TestHomePageMessage(TestCase):
    
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Video Collection')
       
# Tests for the 'add videos' page
class TestAddVideos(TestCase):
    
    # Tests if the user can add videos to the website 
    def test_add_video(self):
        
        # Test data
        valid_video = {
            'name': 'Habit Tracker',
            'url': 'https://www.youtube.com/watch?v=gMBe_Llzd1w',
            'notes': 'Great for tracking my habits.'
        }
        
        # Goes to 'add_video' url to test on that part of the website
        url =reverse('add_video')
        # Checks response from test with test data and if the form is working
        response = self.client.post(url, data=valid_video, follow=True)
        
        # Checks if correct template was used
        self.assertTemplateUsed('video_collection/video_list.html')
        
        # Does the video list show the new video? + Adds 'test data'
        self.assertContains(response, 'Habit Tracker')
        self.assertContains(response, 'Great for tracking my habits.')
        self.assertContains(response, 'https://www.youtube.com/watch?v=gMBe_Llzd1w')
        
        # Tests if there is at least one video in list currently ('test data')
        video_count = Video.objects.count()
        self.assertEqual(1, video_count)
        
        # Makes sure 'test data' is checked first
        video = Video.objects.first()
        
        # Checks if name, notes, and url match 'test data'
        self.assertEqual('Habit Tracker', video.name)
        self.assertEqual('Great for tracking my habits.', video.notes)
        self.assertEqual('https://www.youtube.com/watch?v=gMBe_Llzd1w', video.url)
        
        # Checks 'video_id' is set correctly
        self.assertEqual('gMBe_Llzd1w', video.video_id)
        
    def test_add_video_invalid_url_not_added(self):
        
        # List of bad examples for url
        invalid_video_urls = {
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://youtu.be/gMBe_Llzd1w?si=Xh-7mly8sgDXb7MR',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=123456',   
        }
        
        # Goes through list of bad urls and adds into fields for name and notes with example text
        for invaild_video_url in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url' : invaild_video_url,
                'notes': 'example notes'
            }
            
            # Goes to 'add_video' url to test on that part of the website
            url = reverse('add_video')
            # Sends response to add_video page with bad url example
            response = self.client.post(url, new_video)
            
            # Checks if on wrong template aka 'add.html' instead of 'video_list'
            self.assertTemplateNotUsed('video_collection/add.html')
            
            # Calls and checks if error message was displayed
            messages = get_messages(response.wsgi_request)
            # Saves message response from response test
            message_texts = [str(message) for message in messages]
            
            # Checks for specific messages for bad urls
            self.assertIn('Invalid YouTube URL', message_texts)
            self.assertIn('Please check the data you entered and try again.', message_texts)
            
            # Clears database and shows bad url example didn't get threw
            video_count = Video.objects.count()
            self.assertEqual(0, video_count)

# Tests for the 'video list' page
class TestVideoList(TestCase):
    
    # Tests if videos are displayed in the order of alphabet by 'name'
    def test_all_videos_displayed_in_correct_order(self):
        
        # Good examples of data for testing
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=456')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=789')
        v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=001')
        
        # Expected order of good example videos
        expected_video_order = [v3, v2, v4, v1]
        
        # Links back to 'video_list' part of website
        url = reverse('video_list')
        # Makes a GET response with test examples
        response = self.client.get(url)
        
        # Turns response of test data into a list
        videos_in_template = list(response.context['videos'])
        
        # Checks if these two are the same thing
        self.assertEqual(videos_in_template, expected_video_order)
        
    # Tests if no-video-message is displayed when needed
    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, 'No videos found matching this term.')
        self.assertEqual(0, len(response.context['videos']))
        
    # Tests if number of videos in list is displayed correctly
    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        url = reverse('video_list')
        response = self.client.get(url)
        
        # Yes = '1 video', No = '1 videos'
        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')
        
    # Tests if number of videos in list is displayed correctly
    def test_video_number_message_two_videos(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
        url = reverse('video_list')
        response = self.client.get(url)
            
        # Yes = '2 videos'
        self.assertContains(response, '2 videos')
            
        

# Tests if we can search for specific videos by name
class TestVideoSearch(TestCase):
    pass

#
class TestVideoModel(TestCase):
    
    def test_invalid_url_raises_validation_error(self):
        
        # List of bad examples for url
        invalid_video_urls = {
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://youtu.be/gMBe_Llzd1w?si=Xh-7mly8sgDXb7MR',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            '1234546789',
            'hhhhhhhhhttps://www.youtube.com/watch',
            'http://www.youtube.com/watch',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=123456',
            'https://www.youtube.com/watch/somethingelse',
            'https://www.youtube.com/watch/somethingelse?v=123',   
        }
                
        for invalid_video_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example', url=invalid_video_url, notes='example')
        
        self.assertEqual(0, Video.objects.count())
    
    # Tests if dublicate video rasies integrity error message when needed
    def test_dublicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')