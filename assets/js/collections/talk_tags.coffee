SpkrBar.Collections.TalkTags = Backbone.Collection.extend
    model: SpkrBar.Models.TalkTag

    url: -> "/rest_talk/" + @id + "/tags"

