from django.shortcuts import render

#3rd party imports
import requests
from bs4 import BeautifulSoup





def home(request, *args, **kwargs):
    '''
    The first part fetches the data about current situation in Bangladesh,
    which is organized inside a dictionary called bd_data, which is passed into
    the context so that it can be presented to frontend.
    try print(request) to verify the data
    '''

    bd_url = 'https://www.worldometers.info/coronavirus/country/bangladesh/'
    
    r = requests.get(bd_url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    bd_list = []

    for item in soup.find_all('div', {'class': 'maincounter-number'}):
        bd_list.append(item.text.strip('\n')) 
    
    bd_data = {
        'total_cases': bd_list[0],
        'deaths': bd_list[1],
        'recovered': bd_list[2],
        'active_cases': int(bd_list[0]) - int(bd_list[1]) - int(bd_list[2]),
    }
    
    '''
    Retrieve latest news and articles about COVID-19
    '''

    # ARTICLE_URL = 'https://newsapi.org/v2/everything?q=coronavirus&apiKey=591d4d4f1f514e18be25748b8a230ed0'

    # response = requests.get(ARTICLE_URL).json()

    # news_threshold = response['articles'][:8]

    # news_listings = []

    # for news in news_threshold:
    #     title = news['title']
    #     description = news['description']
    #     news_url = news['url']
    #     img_url = news['urlToImage']

    #     news_listings.append((title, description, news_url, img_url))



    context = {
        'bd_data': bd_data,
        # 'news_listings': news_listings,
    }
    

    return render(request, 'home.html', context)

def worldwide(request):
    '''
    Shows the worldwide data by default.
    If the user passes in a name of a country/region (inside the form)
    correctly, the data for that country/region will be displayed.
    If the data passed in is incorrect (if the API status is 404), then an error page will be displayed.
    '''


    region = 'Worldwide'
    url = "https://coronavirus-map.p.rapidapi.com/v1/summary/latest"

    headers = {
        'x-rapidapi-host': "coronavirus-map.p.rapidapi.com",
        'x-rapidapi-key': "64d7e3123bmsha7ad177c036f2abp187bbdjsn5ed1bd1f4442"
    }

    r = requests.get(url, headers=headers).json()

    if request.method == 'POST':
        url = "https://coronavirus-map.p.rapidapi.com/v1/summary/region"

        search_value = request.POST.get('search')
        querystring = {"region":search_value}
        headers = {
            'x-rapidapi-host': "coronavirus-map.p.rapidapi.com",
            'x-rapidapi-key': "64d7e3123bmsha7ad177c036f2abp187bbdjsn5ed1bd1f4442"
        }

        r = requests.get(url, headers=headers, params=querystring).json()
        region = search_value

    if r['type'] == 'error':

        context = {
            'search_value': request.POST.get('search')
        }

        return render(request, 'error.html', context)


    world_data = {
        'total_cases': r['data']['summary']['total_cases'],
        'active_cases': r['data']['summary']['active_cases'],
        'recovered': r['data']['summary']['recovered'],
        'deaths': r['data']['summary']['deaths'],
    } 
    
    context = {
        'world_data': world_data,
        'region': region
    }
    
    return render(request, 'worldwide.html', context)

def measures(request):
    return render(request, 'measures.html')
