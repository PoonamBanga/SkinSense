import os
from django.db.migrations import serializer
import google.generativeai as genai
from google.cloud import vision
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Scan
from .serializers import ScanSerializer
from django.shortcuts import render

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class ScanUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image_file = request.FILES.get('image')

        #Validation
        if not image_file:
            return Response({'error': 'No image provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if image_file.content_type not in ['image/jpeg', 'image/png']:
            return Response({'error': 'Invalid file type. Only JPEG/PNG allowed.'},status =status.HTTP_400_BAD_REQUEST)

        if image_file.size > 5*1024*1024: #5MB Limit
            return Response({'error': 'File too large. Max size is 5MB.'}, status = status.HTTP_400_BAD_REQUEST)

        #Call Vision API

        try:
            # vision_client = vision.ImageAnnotatorClient(client_options={"api_key": os.getenv('VISION_API_KEY')})
            # content = image_file.read()
            # vision_image = vision.Image(content=content)
            # vision_response = vision_client.label_detection(image=vision_image)
            #labels = [label.description for label in vision_response.label_annotations]
            # Temporary: mock Vision output until billing access is resolved
            labels = ["skin", "face", "acne", "dry skin", "forehead", "oiliness"] 
        except Exception as e:
            return Response({'error': f'Vision API failed: {str(e)}'}, status= status.HTTP_502_BAD_GATEWAY)


        #Call Gemini API
        try:
            model = genai.GenerativeModel('gemini-3.6-flash')
            prompt = f"Based on these detected skin-related laels: {labels}, provide a structured skincare recommendation with severity and care paln."
            gemini_response = model.generate_content(prompt)
            recommendation_text = gemini_response.text
        except Exception as e:
            return Response({'error': f'Gemini API failed: {str(e)}'}, status = status.HTTP_502_BAD_GATEWAY)


        # Save to Dtabase
        image_file.seek(0)
        scan = Scan.objects.create(
            user = request.user,
            image = image_file,
            vision_output={'labels': labels},
            recommendation={'text': recommendation_text}
        )    

        serializer = ScanSerializer(scan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
