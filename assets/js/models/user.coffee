SpkrBar.Models.User = Backbone.Model.extend
    defaults:
        username: ""
        full_name: ""
        email: ""
        following: []
        followers: []
        is_speaker: false
        is_attendee: false
        is_event_planner: false

    initialize: ->

    urlRoot: "/user"
