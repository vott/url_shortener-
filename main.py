import asyncio
import aiohttp
import csv
import random
import string
import uuid

from aiohttp.web import HTTPBadRequest

from utils import (
    validate_url,
    get_or_create_url,
    get_url
)

web = aiohttp.web

async def spam(request):
    """View for fetching duckduckgo results
    it could be in it's own file but it's not
    necessary.
    
    Arguments:
        request {request} -- Request object
    
    Returns:
        Json Response, Contains 3 results for a search
    """

    id = request.match_info.get('id', 'Anonymous')

    if request.method == 'GET':
        word = request.match_info.get('id', 'Anonymous')
        error = ''
        if error:
            return {'error': error}
        else:
            location = get_url(id)
            print(location)
            raise web.HTTPFound(location=location)

    return {}

async def url_shortener(request):
    if request.method == 'POST':
        data = await request.json()
        if 'url' not in data.keys():
            raise HTTPBadRequest(reason='url not in body')
        url = data['url']
        if not validate_url(url):
            raise HTTPBadRequest(reason='wrong url format')
        _url = get_or_create_url(url)
        return web.json_response(data={
            'url': f'http://localhost:8000/sht/{_url.hash}'
        })
        


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