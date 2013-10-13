SpkrBar.Models.Talk = Backbone.Model.extend
    defaults:
        speaker: null
        created_at: ""
        updated_at: ""
        name: ""
        abstract: ""
        published: false
        endorsements: []
        engagements: []
        comments: []
        tags: []
        links: []
        slides: []
        videos: []

    initialize: ->

    urlRoot: "/rest/talk"
