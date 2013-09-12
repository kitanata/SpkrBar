SpkrBar.Models.Engagement = Backbone.Model.extend
    defaults:
        talk: null
        event: null
        date: ""
        from_speaker: true
        confirmed: false

    initialize: ->

    urlRoot: "/rest/engagement"
