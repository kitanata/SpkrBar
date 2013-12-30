SpkrBar.Models.TalkLink = Backbone.Model.extend
    defaults:
        name: ""

    urlRoot: -> "/rest/talk_link"
