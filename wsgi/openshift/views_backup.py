import os, json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from openshift.models import File
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render_to_response('home/home.htm')

def pageSearch(request):
    return render_to_response('home/search.htm')
    
def pageHowitworks(request):
    return render_to_response('home/howitworks.htm')
    
def pageTopsharers(request):
    return render_to_response('home/topsharers.htm') 
    
def pageGettheapp(request):
    return render_to_response('home/gettheapp.htm')

def submitOne(request):
    error = False
    if 'filename' in request.GET:
        filename = request.GET['filename']
        filesize = request.GET['filesize']
        fileblock = request.GET['block']
        fileroom = request.GET['room']
        if not filename:
            error = True
        else:
            p1 = File.objects.create(name=filename, size = filesize, block = fileblock, room = fileroom)
            results = File.objects.all()
            return render_to_response('home/success.htm', { 'results': results })
    return render_to_response('home/submitone.htm', { 'error': error })

@csrf_exempt
def interface(request):
    if request.method == "POST":
        data = json.loads(request.raw_post_data)
        currentBlock = data[0]
        currentRoom = data[1]
        no = len(data) 
        for x in range(2, no, 2):
            temp = File.objects.create(name=data[x], size=data[x+1], block = currentBlock, room = currentRoom)
        files_inserted = no/2
        result = "inserted files: \n\n" + str(files_inserted) + str(request.raw_post_data)
        return HttpResponse(result)


    
    else:
        return HttpResponse("Request not POST")
                
            
            
            
