# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import StreamingHttpResponse, Http404
from django.core.servers.basehttp import FileWrapper

# Create your views here.
def app_config(request):
    if request.method == 'POST':
        app_name = request.POST['app_name']
        # Read configurations from POST
        enables = []
        for (k, v) in request.POST.items():
            if k.find("enable_") != -1:
                enables.append(k.upper())
        # run script
        from generator.gen_script import generate
        ret, path = generate(app_name = app_name, app_logo = None, enables = enables)
        # ret = 0 if successfully generated
        if ret == 0:
            apk_file = file(path)
            response = StreamingHttpResponse(FileWrapper(apk_file), content_type='application/apk')
            response['Content-Disposition'] = 'attachment; filename=phimpme-gen.apk'
            return response
        else:
            raise Http404
    else:
        return render(request, 'app_config.html')