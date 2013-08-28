SpkrBar.Models.TalkComment = Backbone.Model.extend
    defaults:
        name: ""

    urlRoot: -> "/rest_talk/" + @get('talk') + "/comment"
