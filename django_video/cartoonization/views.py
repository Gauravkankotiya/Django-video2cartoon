from django.shortcuts import render
# Create your views here.
from pathlib import Path
import os
#######################################
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GetVideo
from video2cartoon.app import cartoonize

BASE_DIR = Path(__file__).resolve().parent.parent

@api_view(['GET', 'POST'])
def video_convert(request):
    vid = request.FILES.get('video')
    movie = GetVideo()
    movie.video = vid
    movie.save()   
    print("************************************")
    path = movie.video
    path = os.path.join(BASE_DIR / f'media/{path}')
    print(path)
    url = cartoonize(path)
    
    return Response({
        "status" : "Done",
        "link" : f"{url}"
    })