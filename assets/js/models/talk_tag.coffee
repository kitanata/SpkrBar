SpkrBar.Models.TalkTag = Backbone.Model.extend
    defaults:
        name: ""

    urlRoot: -> "/rest_talk/" + @get('talk') + "/tag"
