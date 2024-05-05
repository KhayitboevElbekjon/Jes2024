from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# status codda xatolik kodini chiqarib beradi
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
from .models import *
from rest_framework import status
import subprocess
class Text(APIView):

    def post(self,request):
        text = request.data.get('text', '')
        command = f"text_to_gloss_to_pose --text \"{text}\" --glosser \"simple\" --lexicon \"spoken-to-signed-translation/assets/dummy_lexicon\" --spoken-language \"de\" --signed-language \"sgg\" --pose \"quick_test.pose\""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            return Response({'error': error.decode()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response({'result': output.decode()}, status=status.HTTP_200_OK)
        with open("quick_test.pose", "rb") as f:
            pose_data = f.read()
        p = Pose.read(pose_data)
        scale = p.header.dimensions.width / 256
        p.header.dimensions.width = int(p.header.dimensions.width / scale)
        p.header.dimensions.height = int(p.header.dimensions.height / scale)
        p.body.data = p.body.data / scale
        v = PoseVisualizer(p)
        gif_file_path = f"{text[:20]}.gif"
        v.save_gif(gif_file_path, v.draw())
        GeneratedGif.objects.create(text=text, gif_file=gif_file_path)
        return Response({'result': 'Success'},status=status.HTTP_200_OK)

        # try:
        #     generated_gif = GeneratedGif.objects.all().last()
        #     gif_file_path = generated_gif.gif_file.path
        # except GeneratedGif.DoesNotExist:
        #     return Response({'error': 'GIF not found'}, status=status.HTTP_404_NOT_FOUND)
        #
        # # .gif faylini foydalanuvchiga yuborish
        # with open(gif_file_path, 'rb') as gif_file:
        #     response = HttpResponse(gif_file.read(), content_type='image/gif')
        #     response['Content-Disposition'] = 'inline; filename="{}.gif"'.format(text[:20])
        #     return response


class Gif(APIView):
    def get(self, request):
        try:
            generated_gif = GeneratedGif.objects.all().last()
            gif_file_path = generated_gif.gif_file.path
        except GeneratedGif.DoesNotExist:
            return Response({'error': 'GIF not found'}, status=status.HTTP_404_NOT_FOUND)

        # .gif faylini foydalanuvchiga yuborish
        with open(gif_file_path, 'rb') as gif_file:
            response = HttpResponse(gif_file.read(), content_type='image/gif')
            response['Content-Disposition'] = 'inline; filename="{}.gif"'.format(generated_gif.text[:20])
            return response

