SpkrBar.Models.Engagement = Backbone.RelationalModel.extend
    defaults:
        updated_at: "2013-09-13T19:23:00.807"
        created_at: "2013-09-11T21:12:15.908"
        event_name: "Origins Game Fair"
        room: "Eliot Hall"
        date: "2014-10-09"
        time: "18:30:00"
        location: 0
        talk: 0
        speaker: 0

    relations: [
        {
            type: Backbone.HasOne
            key: 'speaker'
            relatedModel: 'SpkrBar.Models.User'
        },
        {
            type: Backbone.HasOne
            key: 'location'
            relatedModel: 'SpkrBar.Models.Location'
        }
    ]

    initialize: ->

    urlRoot: "/rest/engagement"

    validation:
        event_name:
            required: true
        room:
            required: true
        date:
            required: true
        time:
            required: true

    toJSON: ->
        updated_at: @get('updated_at')
        created_at: @get('created_at')
        event_name: @get('event_name')
        room: @get('room')
        date: @get('date')
        time: @get('time')
        location: @get('location').id
        talk: @get('talk').id
        speaker: @get('speaker').id
