SpkrBar.Models.User = Backbone.Model.extend
    defaults:
        username: ""
        full_name: ""
        email: ""
        following: []
        followers: []
        is_speaker: true

    initialize: ->

    urlRoot: "/user"
