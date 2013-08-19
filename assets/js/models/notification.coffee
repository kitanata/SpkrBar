SpkrBar.Models.Notification = Backbone.Model.extend
    defaults:
        user: null
        title: null
        message: null
        date: null
        dismissed: false

    urlRoot: -> "/user/" + @get('user') + "/note"
