SpkrBar.Models.EventImport = Backbone.RelationalModel.extend
    defaults:
        user: null
        name: ""
        location: null
        state: "AT_REST"

    relations: [
        {
            type: Backbone.HasOne
            key: 'user'
            relatedModel: 'SpkrBar.Models.User'
        },
        {
            type: Backbone.HasOne
            key: 'location'
            relatedModel: 'SpkrBar.Models.Location'
        }
    ]

    initialize: ->

    urlRoot: "/rest/import"

    toJSON: ->
        user: @get('user').id
        name: @get('name')
        location: @get('location').id
        state: @get('state')
