from django.test import TestCase

from googleapiclient.discovery import build

api_key = 'AIzaSyAJ1x3VVK9AoeuA5QCGgq1-46lAbGEIau0'

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
        part='statistics',
        forUsername='prakashkhatri'
    )

response = request.execute()

print(response)