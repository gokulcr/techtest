from django.contrib import messages
from django.shortcuts import redirect
class MW_Authentication():

    excluded_apps = [
        "login",
        "media",
        "admin"
    ]
    def __init__(self, get_response):
      self.get_response = get_response
    def __call__(self, request):
        appname=request.path.split("/")[1]
        try:
           secondname=request.path.split("/")[2]
        except IndexError as error:
            secondname=None
        if appname not in self.excluded_apps  and secondname!='signup':
            if not request.session.get("USER_ID"):
                return redirect('Renders Login Page')
            else:
                if request.session['USER_ID'] == None:
                   messages.warning(request, "error_session_time_out")
                   return redirect('Renders Login Page')
        return self.get_response(request)

      