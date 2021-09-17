import os
import re
import requests as r
from bottle import request, route, run, redirect, template

@route('/v0')
def v0():
    gmaps = request.query['r']
    url = r.get(gmaps, allow_redirects=False).headers['location']
    print(url)
    coords = re.match('.*@(.+)z.*', url)[1].split(',')
    print(coords)
    redir = 'https://www.openstreetmap.org/#map={}/{}/{}'.format(coords[2], coords[0], coords[1])
    return template('Your redirect URL is: <a href="{{redir}}">{{redir}}</a>', redir=redir)

@route('/v1')
def v1():
    gmaps = request.query['r']
    url = r.get(gmaps, allow_redirects=False).headers['location']
    print(url)
    coords = re.match('.*@(.+)z.*', url)[1].split(',')
    print(coords)
    redir = 'https://www.openstreetmap.org/#map={}/{}/{}'.format(coords[2], coords[0], coords[1])
    return redirect(redir)

@route('/json')
def json():
    gmaps = request.query['r']
    url = r.get(gmaps, allow_redirects=False).headers['location']
    print(url)
    coords = re.match('.*@(.+)z.*', url)[1].split(',')
    print(coords)
    redir = 'https://www.openstreetmap.org/#map={}/{}/{}'.format(coords[2], coords[0], coords[1])
    return {"redirect_url": redir}

@route('/v2')
def v2():
    gmaps = request.query['r']
    return template('''
<!doctype html>
<html>
    <head>
        <script type="application/javascript">
            async function main() {
                const gmapsURL = '{{gmaps}}'
                resp = await fetch(gmapsURL, {mode: 'no-cors'})
                url = resp.headers.get('Location')
                if (url === null) {
                    throw "oops... something bad happened"
                }
                // there will be an error above, it makes no sense to continue :D 
            }

            main()
        </script>
    </head>
</html>
''', gmaps=gmaps)

@route('/v3')
def v3():
    gmaps = request.query['r']
    return template('''
<!doctype html>
<html>
    <head>
        <script type="application/javascript">
            async function main() {
                const gmapsURL = '{{gmaps}}'
                resp = await fetch('/json?r=' + encodeURIComponent(gmapsURL))
                j = await resp.json()
                window.location.href = j.redirect_url
            }

            main()
        </script>
    </head>
</html>
''', gmaps=gmaps)


run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

