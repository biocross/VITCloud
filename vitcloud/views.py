from django.views.generic import View
from django.http import HttpResponse
import os, json, datetime
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from vitcloud.models import File
from django.views.decorators.csrf import csrf_exempt
from listingapikeys import findResult
import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

#Custom Functions:
def repeated(fname, fsize, fblock, froom):
    if(File.objects.filter(name=fname, size=fsize, block=fblock, room=froom)):
        return True
    else:
        return False

#**Not for Production** Views
def clean(request):
    q = File.objects.filter(block__iexact="L")
    q.delete()

    
#Views:
def home(request):
    no_of_files = len(File.objects.values_list('name').distinct())
    no_of_blocks = len(File.objects.values_list('block').distinct())
    no_of_rooms = len(File.objects.values_list('room').distinct())
    file_sizes = File.objects.all()
    total_file_size = 0
    for x in file_sizes:
        total_file_size = total_file_size + int(x.size)
    total_file_size = (total_file_size/1024)
    return render_to_response('home/home.htm' , {'x' : no_of_files, 'y' : no_of_blocks, 'z' : no_of_rooms, 'w' : total_file_size })



def pageSearch(request):
    return render_to_response('home/search.htm')
    
def pageHowitworks(request):
    return render_to_response('home/howitworks.htm')
    
def pageTopsharers(request):
    return render_to_response('home/topsharers.htm') 
    
def pageGettheapp(request):
    return render_to_response('home/gettheapp.htm')

def search(request):
    if request.method == "GET":
        if (request.GET['thesearchbox'] == ""):
            if ('latest' in request.GET):
                results = File.objects.all().order_by("-id")
                no = len(results)
                paragraph = True
                return render_to_response('home/results.htm', {'results' : results, 'paragraph' : paragraph,  'no' : no })
            else:
                return redirect('/blockwise')
        else:
            filename = str(request.GET['thesearchbox'])
            paragraph = False
            results = File.objects.filter(name__icontains=filename).order_by("-id")
            no = len(results)
            return render_to_response('home/results.htm', {'results' : results, 'paragraph': paragraph, 'no' : no })

def blockwise(request):
    blockNames = File.objects.values_list('block').distinct()
    for x in blockNames:
        print str(x[0])
    return render_to_response('home/blockwise.htm', {'blocks' : blockNames})

def blockwiseFeeder(request):
    if request.method == "GET":
        block = request.GET['block']
        blockFiles = File.objects.filter(block__iexact=block).order_by("-id")
        return render_to_response('home/blockwiseFeeder.htm', {'block': block, 'results': blockFiles})

def suggestions(request):
    if request.method == "GET":
        filename = str(request.GET['q'])
        results = File.objects.filter(name__icontains=filename)
        length = len(results)
        suggestions = [filename, []]
        for x in range(0, length, 1):
            suggestions[1].append(results[x].name)
        return HttpResponse(json.dumps(suggestions))

class Block:
    name = ""
    total = ""

def statistics(request):
    finalArray = []
    blockNames = []
    blockSizes = []
    blocks = File.objects.values_list('block').distinct()
    for x in blocks:
        blockName = str(str(x[0]).upper())
        blockName = blockName + " Block"
        blockNames.append(str(blockName).encode('utf-8'))
        blockFiles = File.objects.filter(block__iexact=x[0])
        totalSize = 0
        for y in blockFiles:
            totalSize = totalSize + int(y.size)
        blockSizes.append(totalSize/1024)
    return render_to_response('home/stats.htm', {  'blockNames' : blockNames, 'blockSizes' : blockSizes  })
            
    
def apiFeed(request):
    if request.method == "GET":
        if("q" in request.GET):
            filename = str(request.GET['q'])
            result = findResult(filename)
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse("Need The Required Parameters to work!")
    
    

def fileDetails(request):
    if request.method == "GET":
        filename = str(request.GET['q'])
        results = File.objects.filter(name__icontains=filename)
        filen = "NOTFOUND.404"
        for x in results:
            filen = x.name
        return render_to_response('home/file.htm', {'results' : results, 'filen': filen })
      

def submitOne(request):
    error = False
    if 'filename' in request.GET:
        filename = request.GET['filename']
        filesize = 100000
        fileblock = "MN"
        fileroom = "447"
        if not filename:
            error = True
        else:
            now = datetime.datetime.now()
            p1 = File.objects.create(name=filename, size = filesize, block = fileblock, room = fileroom, date = now)
            results = File.objects.all()
            return render_to_response('home/success.htm', { 'results': results })
    return render_to_response('home/submitone.htm', { 'error': error })

@csrf_exempt
def interface(request):
    if request.method == "POST":
        data = json.loads(request.body)
        currentBlock = str(data['Block'])
        currentRoom = str(data['Room'])
        currentHostelType = str(data['Hostel'])
        no = len(data['Files'])
        inserted = 0
        data=data['Files']
        for x in range(0, no, 2):
            data[x+1] = int(data[x+1])
            data[x+1] = (data[x+1]/1048576)
            if not repeated(fname = data[x], fsize = str(data[x+1]), fblock=currentBlock, froom = currentRoom):
                now = datetime.datetime.now()
                temp = File.objects.create(name=data[x], size=str(data[x+1]), block = currentBlock, room = currentRoom, date = now)
                inserted = (inserted + 1)
        files_inserted = inserted
        result = "inserted files: \n\n" + str(files_inserted)
        return HttpResponse(result)
    else:
        return HttpResponse("<h2>VITCloud</h2> <h4>Desktop App Interface</h4><br/><br/><strong>Current Status:</strong> Listening at /interface...<br/><br/>Copyright 2012-2013<br/>Siddharth Gupta<br/>Saurabh Joshi")
