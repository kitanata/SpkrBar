SpkrBar.Collections.TalkLinks = Backbone.Collection.extend
    model: SpkrBar.Models.TalkLink

    url: -> "/rest_talk/" + @talk_id + "/links"

    initialize: (options) ->
        @talk_id = options.talk_id
