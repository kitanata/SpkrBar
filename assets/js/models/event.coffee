SpkrBar.Models.Event = Backbone.Model.extend
    defaults:
        owner: null
        location: null
        start_date: null
        end_date: null
        endorsements: null

    initialize: ->

    urlRoot: "/rest_event"
