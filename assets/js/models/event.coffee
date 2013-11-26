SpkrBar.Models.Event = Backbone.RelationalModel.extend
    defaults:
        name: ""
        num_speakers: 0
        num_engagements: 0
        speakers: []
        tags: []
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
