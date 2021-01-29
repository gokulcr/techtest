class MW_PostLoginCommon():

    excluded_apps = [
        "login",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        appName=request.path.split("/")[1]
        if appName not in self.excluded_apps:
            request.session.set_expiry(500)

        return self.get_response(request)