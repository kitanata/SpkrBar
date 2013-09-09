SpkrBar.Models.Talk = Backbone.Model.extend
    defaults:
        speaker: null
        published: false
        location: null
        start_date: null
        end_date: null
        photo: ""
        endorsements: []
        ratings: []

    initialize: ->

    urlRoot: "/rest_talk"
