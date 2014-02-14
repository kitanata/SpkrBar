SpkrBar.Collections.EventImportErrors = Backbone.Collection.extend
    model: SpkrBar.Models.EventImportError

    url: ->
        "/rest/import/" + @import_id + "/errors"

    initialize: (options) ->
        @import_id = options.import.id
