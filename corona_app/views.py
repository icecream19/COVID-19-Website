from django.shortcuts import render

#3rd party imports
import requests





def home(request, *args, **kwargs):
    url = "https://coronavirus-map.p.rapidapi.com/v1/summary/region"

    querystring = {"region":"Bangladesh"}

    headers = {
        'x-rapidapi-host': "coronavirus-map.p.rapidapi.com",
        'x-rapidapi-key': "64d7e3123bmsha7ad177c036f2abp187bbdjsn5ed1bd1f4442"
    }

    # response = requests.request("GET", url, headers=headers, params=querystring).json()

    r = requests.get(url, headers=headers, params=querystring).json()


    bd_data = {
        'total_cases': r['data']['summary']['total_cases'],
        'active_cases': r['data']['summary']['active_cases'], 
        'deaths': r['data']['summary']['deaths'],
        'recovered': r['data']['summary']['recovered'],
    }
    
    context = {
        'bd_data': bd_data,
    }
    

    return render(request, 'home.html', context)

def worldwide(request):
    return render(request, 'worldwide.html')

def measures(request):
    return render(request, 'measures.html')
