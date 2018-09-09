import asyncio
import aiohttp
import csv
import random
import string
import uuid

from aiohttp.web import HTTPBadRequest, HTTPNotFound

from utils import (
    validate_url,
    get_or_create_url,
    get_url
)

web = aiohttp.web

async def spam(request):
    """View for fetching redirecting to a shortened url
    
    Arguments:
        request {request} -- Request object
    
    Returns:
        HTTPFound 302 
    """

    id = request.match_info.get('id', 'Anonymous')

    if request.method == 'GET':
        word = request.match_info.get('id', 'Anonymous')
        location = get_url(id)
        if location:
            raise web.HTTPFound(location=location)
        else:
            raise HTTPNotFound()

    return {}

async def url_shortener(request):
    """
        View to that recieves an url and returns
        a smaller version of it
    """
    if request.method == 'POST':
        # get data from post
        data = await request.json()
        # validate structure of the json contained by the request
        if 'url' not in data.keys():
            raise HTTPBadRequest(reason='url not in body')
        url = data['url']
        # validate the provide url
        if not validate_url(url):
            raise HTTPBadRequest(reason='wrong url format')
        _url = get_or_create_url(url)
        # generate response
        return web.json_response(
            data={
                'status':201,
                'url': f'http://localhost:8000/sht/{_url.hash}'
            }
        )
        


def init():
    """Config aiohttp app
    
    Returns:
        app
    """

    app = web.Application()
    app.router.add_get('/sht/{id}', spam, name='sht')
    app.router.add_post('/short/', url_shortener, name='short')
    return app

if(__name__ == '__main__'):
    init()