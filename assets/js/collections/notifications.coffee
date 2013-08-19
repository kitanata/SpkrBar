SpkrBar.Collections.Notifications = Backbone.Collection.extend
    model: SpkrBar.Models.Notification

    url: -> "/user/" + @user_id + "/notes"

    initialize: (options) ->
        @user_id = options.user_id

