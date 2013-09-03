SpkrBar.Models.TalkComment = Backbone.Model.extend
    defaults:
        talk: 0
        comment: 0

    urlRoot: -> "/rest_talk/" + @get('talk') + "/comment"
