SpkrBar.Models.Engagement = Backbone.Model.extend
    defaults:
        id: 0
        talk: null
        event: null
        date: ""
        attendees: []
        from_speaker: true
        vetoed: false

    initialize: ->

    urlRoot: "/engagement"
