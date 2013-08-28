SpkrBar.Collections.TalkComments = Backbone.Collection.extend
    model: SpkrBar.Models.TalkComment

    url: -> "/rest_talk/" + @talk_id + "/comments"

    initialize: (options) ->
        @talk_id = options.talk_id
