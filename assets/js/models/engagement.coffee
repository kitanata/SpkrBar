SpkrBar.Models.Engagement = Backbone.Model.extend
    defaults:
        talk: null
        event: null
        date: ""
        attendees: []
        from_speaker: true
        confirmed: false

    initialize: ->

    urlRoot: "/engagement"
