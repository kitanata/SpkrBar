SpkrBar.Models.TalkLink = Backbone.Model.extend
    defaults:
        name: ""

    urlRoot: -> "/rest_talk/" + @get('talk') + "/link"
