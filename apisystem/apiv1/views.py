from django.shortcuts import render
from django.http import JsonResponse
from .models import Student, Teacher
from .serializers import StudentSerializers, TeacherSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from rest_framework.views import APIView

from rest_framework import viewsets
# Create your views here.


def home(request):

    data = {
        'name': 'prakash',
        'age': 25
    }
    return JsonResponse(data)


@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        stu = Student.objects.all()
        serializer = StudentSerializers(stu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        stu_data = request.data
        serializer = StudentSerializers(data=stu_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def student_details(request, pk=None):
    try:
        stu_data = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializers(stu_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = StudentSerializers(stu_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stu_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# teaccher views

@api_view(['GET', 'POST'])
def teacher_list(request):
    if request.method == 'GET':
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        teacher = request.data
        serializer = TeacherSerializer(data=teacher)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def teacher_details(request, pk=None):
    try:
        teacher = Teacher.objects.get(pk=pk)
    except Teacher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class based views

class StudentView(APIView):

    def get_obj(self, pk=None):
        try:
            stu_data = Student.objects.get(pk=pk)
            return stu_data
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        if pk is not None:
            stu_data = self.get_obj(pk=pk)
            serializer = StudentSerializers(stu_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            stu_data = Student.objects.all()
            serializer = StudentSerializers(stu_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        stu_data = self.get_obj(pk=pk)
        serializer = StudentSerializers(stu_data, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        stu_data = self.get_obj(pk=pk)
        stu_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# viewsets


class TecaherViewSet(viewsets.ModelViewSet):
    # queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        sub = self.request.query_params.get('sub', None)
        if sub and sub.lower() == 'hindi':
            return Teacher.objects.filter(sub=sub)
        return Teacher.objects.all()
