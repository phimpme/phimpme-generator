from django.shortcuts import render
from django.http import Http404#HttpResponseServerError

# Create your views here.
def app_config(request):
    if request.method == 'POST':
        app_name = request.POST['app_name'].upper()
        # Read configurations from POST
        configs = {}
        for (k, v) in request.POST.items():
            if k.find("enable_") != -1:
                configs[k] = v
        
        # run script
        from generator.gen_script import generate
        ret, path = generate(app_name = app_name, app_logo = None, configs = configs)
        print path
        if ret == 0:
            return render(request, 'app_config.html', {'generated': True, 'download_link':'URL...'})
        else:
            raise Http404#HttpResponseServerError
    else:
        return render(request, 'app_config.html')