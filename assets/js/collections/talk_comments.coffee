SpkrBar.Collections.TalkComments = Backbone.Collection.extend
    model: SpkrBar.Models.TalkComment

    url: -> 
        talkId = @talk.id
        "/rest/talk/" + talkId + "/comments"
