from django.shortcuts import render,redirect,reverse,HttpResponse
from .models import Suggestion
from .forms import SuggestionForm
from django.contrib import messages

import datetime
from datetime import date
import calendar
import pytz
import requests
from operator import itemgetter
import json
from .models import Suggestion
import copy
from babel.numbers import format_currency


def api(request):

    global_stats = requests.get('https://api.thevirustracker.com/free-api?global=stats')
    global_stats = global_stats.json()
    global_stats = global_stats['results'][0]
    del global_stats['source']
    for x in global_stats:
        a = global_stats[x]
        b = format_currency(a, 'INR', locale='en_IN')
        c = b[1:len(b)-3]
        global_stats[x] = c
    all_country = requests.get('https://api.thevirustracker.com/free-api?countryTotals=ALL')
    all_country = all_country.json()
    all_country = all_country['countryitems'][0]
    country_data = []
    for key,value in all_country.items():
        country_data.append(value)
    country_data.remove('ok')

    country_data = sorted(country_data, key=itemgetter('total_cases'),reverse=True)
    
    #response = requests.get('https://api.covid19api.com/summary')
    #info = response.json()
    response_india = requests.get('https://api.covid19india.org/data.json')
    india = response_india.json()
    #file = jsonfiles.objects.get(file = 'countries_JOhe0Es.json')
    #f = open(file.file.path, )
    #continents = json.load(f)
    #countries = info['Countries']
    #for j in range(186):
     #   for i in range(245):
     #      if continents[i]['country'] == countries[j]['Country']:
     #              countries[j]['Continent'] = continents[i]['continent']
     #              break          
    #f.close()           
    #countries = list(countries)
    #countries1 = sorted(countries, key=itemgetter('TotalConfirmed'),reverse=True)
    #graph=india['cases_time_series']
    #daywise={}
    #for entry in graph:
    #    day = entry.pop('date')
    #    daywise[day] = entry

    #daywise = dict(list(daywise.items())[119:0: -10])
    
    #daywise2 = dict(list(daywise.items())[::-1 ])



    state=india['statewise']
    state=list(state)
    newstate={}
    for entry in state:
        name = entry.pop('state')
        newstate[name] = entry
    statelist=list(newstate)
    statelist.remove('Total')

    #b = copy.deepcopy(countries1)
    #newcountries={}
    #for entry in countries:
    #    name = entry.pop('Country')
    #    newcountries[name] = entry
    #countrylist=list(newcountries)
         
    data={
        'all_country':country_data ,
        '1':country_data[0],
        '2':country_data[1],
        '3':country_data[2],
        'global': global_stats,
        'india_total':india['statewise'][0],
        'statelist':statelist,
        'india':india,
        #'daywise':daywise2,
        
    }
    
    
    return render(request, 'covidapp/api.html',data)


def statewise(request):
    d=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    response_india = requests.get('https://api.covid19india.org/data.json')

    india = response_india.json()
    url1='https://api.thevirustracker.com/free-api?countryTimeline={}'
    timeline=requests.get(url1.format('IN')).json()
    timeline = timeline['timelineitems'][0]
    m=len(timeline)
    m=m-2

    timeline = dict(list(timeline.items())[m:0:-5])


    timeline2 = dict(list(timeline.items())[::-1 ])


    
    india1=india['statewise']
    graph=india['cases_time_series']
    daywise={}
    for entry in graph:
        day = entry.pop('date')
        daywise[day] = entry

    l=len(daywise)
    l=l-1
    daywise = dict(list(daywise.items())[l:0: -10])


    daywise2 = dict(list(daywise.items())[::-1 ])
    
    
    


    data={
        'india':india1,
        'india_total':india['statewise'][0],
        'd':d,
        'daywise':daywise2,
        'timeline':timeline2,
      
    }

    return render(request, 'covidapp/sample.html',data)

def stateview(request,sname):
    if sname == 'Total':
        return redirect('statewise')
    else:    
        d=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

        zones = requests.get('https://api.covid19india.org/zones.json')
        zones = zones.json()
        zones = zones['zones']
        zone_name = {}
        for entry in zones:
            district_name = entry.pop('district')
            zone_name[district_name] = entry


        response_india = requests.get('https://api.covid19india.org/data.json')
        india = response_india.json()

        response_state=requests.get('https://api.covid19india.org/state_district_wise.json')
        districts= response_state.json()
        state=india['statewise']
        state=list(state)
        newstate={}
        for entry in state:
            name = entry.pop('state')
            newstate[name] = entry
        s=newstate[sname]
        dis=districts[sname]['districtData']

        for key,value in dis.items():
            for x in zone_name:
                if x == key:
                    dis[key]['zone'] = zone_name[x]['zone']
                
                
        data={
            's':s,
            'sname':sname,
            'd':d,
            'dis':dis,
            'zone_name':zone_name
            
         
        }
       
        
    return render(request, 'covidapp/stateview.html',data)

    
def statesearch(request):
    
    statelist=['Maharashtra', 'Tamil Nadu', 'Delhi', 'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh', 'West Bengal', 'State Unassigned', 'Andhra Pradesh', 'Bihar', 'Karnataka', 'Punjab', 'Telangana', 'Jammu and Kashmir', 'Odisha', 'Haryana', 'Kerala', 'Assam', 'Uttarakhand', 'Jharkhand', 'Chhattisgarh', 'Chandigarh', 'Himachal Pradesh', 'Tripura', 'Goa', 'Ladakh', 'Puducherry', 'Manipur', 'Andaman and Nicobar Islands', 'Meghalaya', 'Nagaland', 'Dadra and Nagar Haveli and Daman and Diu', 'Arunachal Pradesh', 'Mizoram', 'Sikkim', 'Lakshadweep']
    
    statelist=set(statelist)


    countrylist=['US', 'BR', 'RU', 'ES', 'GB', 'IT', 'FR', 'DE', 'IN', 'TR', 'PE', 'IR', 'CL', 'CA', 'MX', 'SA', 'CN', 'PK', 'BE', 'QA', 'BD', 'NL', 'BY', 'EC', 'SE', 'SG', 'AE', 'PT', 'ZA', 'CH', 'CO', 'KW', 'ID', 'IE', 'PL', 'UA', 'EG', 'RO', 'PH', 'IL', 'DO', 'JP', 'AT', 'AR', 'AF', 'PA', 'DK', 'OM', 'RS', 'KZ', 'NG', 'BO', 'AM', 'DZ', 'CZ', 'NO', 'MD', 'GH', 'MY', 'MA', 'AU', 'FI', 'KR', 'IQ', 'CM', 'AZ', 'HN', 'SD', 'GT', 'LU', 'HU', 'TJ', 'GN', 'SN', 'UZ', 'DJ', 'TH', 'GR', 'CI', 'GA', 'SV', 'BG', 'BA', 'HR', 'MK', 'CU', 'SO', 'KE', 'EE', 'HT', 'IS', 'KG', 'LT', 'LK', 'NP', 'SK', 'NZ', 'SI', 'VE', 'GQ', 'GW', 'ML', 'LB', 'AL', 'HK', 'TN', 'LV', 'ET', 'ZM', 'CR', 'SS', 'PY', 'NE', 'CY', 'SL', 'BF', 'UY', 'GE', 'TD', 'NI', 'MG', 'JO', 'DP', 'JM', 'CG', 'TZ', 'MR', 'GF', 'PS', 'TW', 'TG', 'UG', 'RW', 'VN', 'ME', 'YE', 'LR', 'MW', 'MZ', 'BJ', 'MM', 'MN', 'ZW', 'GY', 'BN', 'LY', 'KH', 'TT', 'BS', 'AO', 'BI', 'BT', 'PR', 'BW', 'GM', 'NA', 'NC', 'BZ', 'FJ', 'SR', 'FK', 'GL', 'EH', 'PG', 'LS', 'CF', 'CD', 'ER', 'TF', 'KP', 'LA', 'XK', 'SB', 'SJ', 'SZ', 'SY', 'TL', 'TM', 'VU', 'CD', 'XK', 'KP']
    
    countrylist=set(countrylist)
    if request.method == 'POST':
        sname = request.POST.get("searchstate")
            
        if sname in statelist:
                return redirect('stateview',sname=sname)
        elif sname in countrylist:
                if sname == 'IN':
                    return redirect('statewise')
                else:
                    return redirect('countryview',code=sname)
        else:
                #messages.info(request, 'No search found.')
                return redirect('api')
                #return HttpResponse('No such country or state exists')


def dev(request):
    from datetime import date
    from datetime import datetime
    x = datetime.now(pytz.timezone('Asia/Kolkata'))
    today = date.today()

    d2 = today.strftime("%B %d, %Y")
    return render(request,'covidapp/dev.html', {'d':d2, 'x':x})

def countryview(request,code):
    if code == 'IN':
        return redirect('statewise')
    else:    
        d=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        url = 'https://api.thevirustracker.com/free-api?countryTotal={}'
        url1 = 'https://api.thevirustracker.com/free-api?countryTimeline={}'
        info = requests.get(url.format(code)).json()
        timeline = requests.get(url1.format(code)).json()
        timeline = timeline['timelineitems'][0]
        info=info['countrydata']
        info=info[0]
        
        name=info['info']['title']


        l=len(timeline)
        l=l-2
        timeline = dict(list(timeline.items())[l:0:-5])


        timeline2 = dict(list(timeline.items())[::-1 ])

        '''countries = info['Countries']

        countries = list(countries)
        
        newcountries={}
        for entry in countries:
            name = entry.pop('Country')
            newcountries[name] = entry

        n=newcountries[cname]'''
        data={
            'name':name,
            'info':info,
            'd':d,
            'timeline':timeline2,
        }
    return render(request,'covidapp/countryview.html',data)

def Helpline(request):
    
    regional= [
        {"loc": "Andhra Pradesh", "number": "+91-866-2410978"},
        {"loc": "Arunachal Pradesh", "number": "+91-9436055743"},
        {"loc": "Assam", "number": "+91-6913347770"},
        {"loc": "Bihar", "number": "104"},
        {"loc": "Chhattisgarh", "number": "104"},
        {"loc": "Goa", "number": "104"},
        {"loc": "Gujarat", "number": "104"},
        {"loc": "Haryana", "number": "+91-8558893911"},
        {"loc": "Himachal Pradesh", "number": "104"},
        {"loc": "Jharkhand", "number": "104"},
        {"loc": "Karnataka", "number": "104"},
        {"loc": "Kerala", "number": "+91-471-2552056"},
        {"loc": "Madhya Pradesh", "number": "+91-755-2527177"},
        {"loc": "Maharashtra", "number": "+91-20-26127394"},
        {"loc": "Manipur", "number": "+91-3852411668"},
        {"loc": "Meghalaya", "number": "108"},
        {"loc": "Mizoram", "number": "102"},
        {"loc": "Nagaland", "number": "+91-7005539653"},
        {"loc": "Odisha", "number": "+91-9439994859"},
        {"loc": "Punjab", "number": "104"},
        {"loc": "Rajasthan", "number": "+91-141-2225624"},
        {"loc": "Sikkim", "number": "104"},
        {"loc": "Tamil Nadu", "number": "+91-44-29510500"},
        {"loc": "Telengana", "number": "104"},
        {"loc": "Tripura", "number": "+91-381-2315879"},
        {"loc": "Uttarakhand", "number": "104"},
        {"loc": "Uttar Pradesh", "number": "18001805145"},
        {"loc": "West Bengal", "number": "1800313444222,+91-3323412600,"},
        {"loc": "Andaman and Nicobar Islands", "number": "+91-3192-232102"},
        {"loc": "Chandigarh", "number": "+91-9779558282"},
        {"loc": "Dadra and Nagar Haveli", "number": "104"},
        {"loc": "Daman & Diu", "number": "104"},
        {"loc": "Delhi", "number": "+91-11-22307145"},
        {"loc": "Jammu and Kashmir", "number": "+91-191-2520982,+91-194-2440283"},
        {"loc": "Ladakh", "number": "+91-1982-256462"},
        {"loc": "Lakshadweep", "number": "104"},
        {"loc": "Puducherry", "number": "104"},
    ]
    
    data={
        'helpline1':regional,

    }
    
    return render(request,'covidapp/helpline.html',data)



def about(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for the review. It motivates us to do more great stuff!')
    else:
        form = SuggestionForm()
    count = Suggestion.objects.all().count()
    return render(request, 'covidapp/about.html', {'form':form, 'count':count})