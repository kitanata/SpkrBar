from urlparse import urlparse, urlunparse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from core.models import UserLink

from core.forms import ProfileLinkForm

@login_required
def profile_link_new(request):
    if request.method == "POST":
        form = ProfileLinkForm(request.POST)

        if form.is_valid():
            profile = request.user.get_profile()

            link_model = UserLink()

            link_type = form.cleaned_data['type']
            orig_url = form.cleaned_data['url']
            url = urlparse(orig_url, scheme="http")

            if link_type in [UserLink.LINKEDIN, UserLink.BLOG, UserLink.WEBSITE]:
                orig_url = url.geturl()
            else:
                found = False
                for test in ['www.', 'facebook', 'twitter', 'github']:
                    if test in url.path.lower():
                        found = True
                        orig_url = url.geturl()
                        break

                if not found:
                    path = str(url.path)
                    if path.startswith('@'):
                        path = path[1:]

                    root_urls = {
                            UserLink.FACEBOOK: 'www.facebook.com/',
                            UserLink.TWITTER: 'www.twitter.com/',
                            UserLink.GITHUB: 'www.github.com/'
                            }

                    new_url = (url.scheme, '', (root_urls[link_type] + path), '', '', '')
                    orig_url = urlunparse(new_url)

            link_model.type_name = link_type
            link_model.url_target = orig_url
            link_model.user = profile.user
            link_model.save()

            return redirect(request.user.get_profile())
        return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()
