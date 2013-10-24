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
