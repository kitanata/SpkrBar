def speaker_restricted(view):
    def f(request, *args, **kwargs):
        print request
        print args
        print kwargs
        return view(request, *args, **kwargs)

    return f
