from django.shortcuts import render

#3rd party imports
import requests
from bs4 import BeautifulSoup
from requests.compat import quote





def home(request, *args, **kwargs):
    '''
    The first part fetches the data about current situation in Bangladesh,
    which is organized inside a dictionary called bd_data, is passed into
    the context so that it can be presented to frontend.
    try print(request) to verify the data
    '''

    bd_url = 'https://www.worldometers.info/coronavirus/country/bangladesh/'
    
    r = requests.get(bd_url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    bd_list = []

    for item in soup.find_all('div', {'class': 'maincounter-number'}):
        bd_list.append(item.text.strip('\n').replace(',', '')) 
    
    bd_data = {
        'total_cases': bd_list[0],
        'deaths': bd_list[1],
        'recovered': bd_list[2],
        'active_cases': int(bd_list[0]) - int(bd_list[1]) - int(bd_list[2]),
    }
    
    '''
    Retrieve latest news and articles about COVID-19
    '''

    ARTICLE_URL = 'https://newsapi.org/v2/everything?q=coronavirus&apiKey=591d4d4f1f514e18be25748b8a230ed0'

    response = requests.get(ARTICLE_URL).json()

    news_threshold = response['articles'][:8]

    news_listings = []

    for news in news_threshold:
        title = news['title']
        description = news['description']
        news_url = news['url']
        img_url = news['urlToImage']

        news_listings.append((title, description, news_url, img_url))



    context = {
        'bd_data': bd_data,
        'news_listings': news_listings,
    }
    

    return render(request, 'home.html', context)




def worldwide(request):
    '''
    Shows the worldwide data by default.
    If the user passes in a name of a country/region (inside the form)
    correctly, the data for that country/region will be displayed.
    If the data passed in is incorrect (if the world_list is empty), then an error page will be displayed.
    '''

    base_url = 'https://www.worldometers.info/coronavirus/'
    region = 'Worldwide'

    r = requests.get(base_url)
    data = r.text

    

    if request.method == 'POST':
        base_url = 'https://www.worldometers.info/coronavirus/country/{}/'

        search_value = request.POST.get('search')
        new_url = base_url.format(search_value.replace(' ', '-'))
        
        region = search_value
        r = requests.get(new_url)
        data = r.text

    soup = BeautifulSoup(data, 'html.parser')

    world_list = []

    for item in soup.find_all('div', {'class': 'maincounter-number'}):
        world_list.append(item.text.strip('\n').replace(',', ''))

    if not world_list:
        context = {
            'search_value' : search_value
        }

        return render(request, 'error.html', context)


    world_data = {
        'total_cases': world_list[0],
        'deaths': world_list[1],
        'recovered': world_list[2],
        'active_cases': int(world_list[0]) - int(world_list[1]) - int(world_list[2]),
    }
    

    context = {
        'world_data': world_data,
        'region': region
    }
    
    return render(request, 'worldwide.html', context)



def measures(request):
    return render(request, 'measures.html')
