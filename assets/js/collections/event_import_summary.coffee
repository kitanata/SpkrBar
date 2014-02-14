SpkrBar.Collections.EventImportSummary = Backbone.Collection.extend
    model: SpkrBar.Models.EventImportSummary

    url: ->
        "/rest/import/" + @import_id + "/summary"

    initialize: (options) ->
        @import_id = options.import.id
