import csv
import codecs
import os
import shutil

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic

from . forms import CsvFileForm, TeacherForm
from .models import Teachers

def add_csv(request):
    """ Endpoint for adding csv file """

    f = 0
    list_of_images = []
    if request.method == 'POST':
        csv_file=request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 
                    'Incorrect format')
            return redirect("user_home")
        csv_reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count=+1
            else:
                try:
                    teacher = Teachers()
                    teacher.first_name = row[0]
                    teacher.last_name = row[1]
                    if row[2].strip()!="":
                        teacher.image = row[2]
                        list_of_images.append(row[2])
                    else:
                        teacher.image = "default.jpg"
                    teacher.email = row[3]
                    teacher.phone = row[4]
                    teacher.room_number = row[5]
                    list_subjects = row[6].split()
                    subjects = " "
                    teacher.subjects = subjects.join(list_subjects[0:5])
                    if teacher.email.strip():
                        teacher.save()
                    f = 1
                except Exception as e:
                    pass  
        if f != 1:
             messages.error(request, 
                    'record is already added')
        else:
            load_images_from_folder(list_of_images)
            messages.success(request, 'uploaded successfully')
        return redirect("user_home")
    else:
        return render(request, 'add_csv.html', {
          "csvform": CsvFileForm
          })

class UserHome(generic.ListView):
    """
    Endpoint for searching / filtering recipes
    """
    template_name = 'list_teachers.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset =  Teachers.objects.all()
        queryset = self.search(queryset)
        return queryset
    
    def search(self, queryset):
        search_query_subject = self.request.GET.get('subject_query')
        search_query_name = self.request.GET.get('name_query')
        if  search_query_subject:
            query =  search_query_subject.strip()
            queryset = queryset.filter(
                Q(subjects__icontains=query))
        if search_query_name:
            query =  search_query_name.strip()
            queryset = queryset.filter(
                Q(last_name__startswith=query))                   
        return queryset

def detail_view(request, id=None):
    """Endpoint for Teachers detail view"""

    if id:
        teacher_object = Teachers.objects.get(id=id)
        form = TeacherForm(request.POST or None, instance=teacher_object)
    return render(request, 'detail_teacher.html', {
          "form": form
          })


def load_images_from_folder(list_of_images):
        in_folder_path = '/home/sayone/teachers' #specify the path of image folder
        try:
            os.mkdir(os.path.join(settings.BASE_DIR,"media"))
        except:
            pass
        out_folder_path = os.path.join(settings.BASE_DIR,"media")
        for image_name in list_of_images:
            try:
                cur_image_path = os.path.join(in_folder_path,image_name)
                cur_image_out_path = os.path.join(out_folder_path,image_name)
                shutil.copyfile(cur_image_path, cur_image_out_path)
            except:
                pass
    
        
        

    
