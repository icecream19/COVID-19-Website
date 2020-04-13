from django.shortcuts import render

#3rd party imports
import requests





def home(request, *args, **kwargs):
    '''
    The first part fetches the data about current situation in Bangladesh,
    which is organized inside a dictionary called bd_data, which is passed into
    the context so that it can be presented to frontend.
    try print(request) to verify the data
    '''

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
    return render(request, 'worldwide.html')

def measures(request):
    return render(request, 'measures.html')
