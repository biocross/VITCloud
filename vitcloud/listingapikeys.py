import os, re, json
from urllib2 import Request, urlopen
from urllib import quote

#Test with filenames to both functions

def findMovieId(name):

	filename, extension = os.path.splitext(name)
	title = None
	year = None
	extension = extension.rstrip()
	if extension in ['.mkv', '.mp4', '.avi', '.m4v', '.webm']:
		flag = False
		matches = re.findall(r"([\s\d]*)([\sA-Za-z'+-.]+)([\d]*)([\sA-Za-z'+-.]*)([\(\[]*[\d][\d][\d][\d][\)\]]*)", filename)
		for match in matches:
			title=(match[0].replace('.',' ').strip()+" "+match[1].replace('.',' ').strip()+" "+match[2].replace('.',' ').strip()+" "+match[3].replace('.',' ').strip()).replace('.',' ').strip()
			year=match[4].replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').strip()
			if int(year)>1000 and int(year)<3000:
				flag = True
				break
		if not flag:
			matches = re.findall(r"([\s\d]*)([\sA-Za-z'+-.]+)", filename)
			for match in matches:
				title = (match[0].replace('.',' ').strip()+" "+match[1].replace('.',' ').strip()).strip()
				year = None
				if title.lower() not in ['sample', 'silver', 'du', 'esd-hies', 'kkbb', 'extratorrentrg']:
					if ' br' in title.lower():
						title = title.lower().replace('br','').strip()
					if ' rip' in title.lower():
						title = title.lower().replace('rip','').strip()
					if ' yify' in title.lower():
						title = title.lower().replace('yify','').strip()
					if ' x' in title.lower():
						title = title.lower().replace('x','').strip()
					if 'target-' in title.lower():
						title = title[title.find('-')+1:title.find('-', title.find('-')+1)].strip()
					if 'dvdrip' in title.lower():
						title = title[0:title.lower().find('dvdrip')].strip()
					if 'hrspk' in title.lower():
						title = title[0:title.lower().find('hrspk')-1].strip()
				break
	else:
		return {}
	removablestrings = ['extended', 'unrated', 'directors cut', 'director\'s cut', 'final cut']
	if year == '1080':
		if '19' in title:
			year = title[title.find('19'):title.find('19')+4]
			title = title[0:title.find('19')].strip()
		elif '20' in title:
			year = title[title.find('20'):title.find('20')+4]
			title = title[0:title.find('20')].strip()
		for remstring in removablestrings:
			if remstring in title.lower():
				title = title[0:title.lower().find(remstring)].strip()
	movieSearchUrl = "https://api.themoviedb.org/3/search/movie?api_key=72380f72d2ac93525738d2ef104c283d&"
	headers = {"Accept": "application/json"}
	print "searching for title: " + title
	if year != None:
		url = movieSearchUrl+"query="+quote(title)+"&year="+year
	else:
		url = movieSearchUrl+"query="+quote(title)
	request = Request(url, headers=headers)
	response_body = urlopen(request).read()
	data = json.loads(response_body)
	if data["total_results"] != 0:
		movieid = data["results"][0]["id"]
		if year!= None:
			return {"title":title, "year":int(year), "id":movieid}
		else:
			return {"title":title, "id":movieid}
	else:
		movieid = None
		return {}

def findTvShowDetails(name):
	print "Entered TVFunction"
	show = season = episode = None
	result = {}
	filename, extension = os.path.splitext(name)
    	if extension in ['.mkv', '.mp4', '.avi', '.m4v', '.wmv', '.flv']:
	    	flag = True
	    	matches = re.findall(r"^((?P<series_name>.+?)[. _-]+)?s(?P<season_num>\d+)[. _-]*e(?P<ep_num>\d+)(([. _-]*e|-)(?P<extra_ep_num>(?!(1080|720)[pi])\d+))*[. _-]*((?P<extra_info>.+?)((?<![. _-])-(?P<release_group>[^-]+))?)?$", filename)
	    	for match in matches:
	    		show = match[0].replace('.',' ').strip()
	    		season = match[2]
	    		episode = match[3]
	    		flag =  False
	    		break
	    	if flag:
	    		matches = re.findall(r"^((?P<series_name>.+?)[\[. _-]+)?(?P<season_num>\d+)x(?P<ep_num>\d+)(([. _-]*x|-)(?P<extra_ep_num>(?!(1080|720)[pi])(?!(?<=x)264)\d+))*[\]. _-]*((?P<extra_info>.+?)((?<![. _-])-(?P<release_group>[^-]+))?)?$", filename)
	    		for match in matches:
	    			show = match[0].replace('.',' ').strip()
	    			season = match[2]
	    			episode = match[3]
	    			flag = False
	    	if flag:
	    		matches = re.findall(r"([\sA-Za-z'+-.]+)([sS])([\d][\d])([eE])([\d][\d])", filename)
	    		for match in matches:
	    			show = match[0].replace('.',' ').strip()
	    			season = match[2]
	    			episode = match[4]
	if show == None:
		return {}
	if '-' in show:
		show = show.replace('-', '').strip()
	tvSearchUrl = "https://api.themoviedb.org/3/search/tv?api_key=72380f72d2ac93525738d2ef104c283d&"
	#BUG : show is always empty
	print "searching for title: " + show
	url = tvSearchUrl+"query="+quote(show)
	headers = {"Accept": "application/json"}
	request = Request(url, headers=headers)
	response_body = urlopen(request).read()
	data = json.loads(response_body)
	if data["total_results"]!=0:
		return {'show':show, 'season':int(season), 'episode':int(episode), 'id':data["results"][0]["id"]}
	else:
		return {}

def findResult(name):
	print "got: " + name
	result = findTvShowDetails(name)
	if result != {}:
		result.update({'status':'valid', 'type':'tv'})
		return result
	else:
		result = findMovieId(name)
		if result != {}:
			result.update({'status':'valid', 'type':'movie'})
			return result
		else:
			result = {'status':'invalid'}
			return result