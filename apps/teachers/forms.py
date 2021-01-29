from django import forms

from apps.teachers.models import Teachers


class CsvFileForm(forms.Form):
    csv_file=forms.FileField()


class TeacherForm(forms.ModelForm):
    subjects = forms.CharField( widget=forms.Textarea(
        attrs={'width':"50%", 'cols' : "50", 'rows': "2", }),
        max_length=500 )
    
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['readonly'] = True
    
    class Meta:
        model = Teachers
        fields = ['email','last_name','phone','image','room_number','subjects']

