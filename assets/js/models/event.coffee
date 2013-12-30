SpkrBar.Models.Event = Backbone.RelationalModel.extend
    defaults:
        name: ""
        tags: []
        speakers: []
        engagements: []

    relations: [
        {
            type: Backbone.HasMany
            key: 'engagements'
            relatedModel: 'SpkrBar.Models.Engagement'
        },
        {
            type: Backbone.HasMany
            key: 'speakers'
            relatedModel: 'SpkrBar.Models.User'
        },
    ]

    initialize: ->

    urlRoot: "/rest/event"
