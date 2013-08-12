SpkrBar.Collections.TalkTags = Backbone.Collection.extend
    model: SpkrBar.Models.TalkTag

    url: -> "/rest_talk/" + @talk_id + "/tags"

    initialize: (options) ->
        @talk_id = options.talk_id
