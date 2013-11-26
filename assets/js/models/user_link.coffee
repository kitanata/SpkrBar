SpkrBar.Models.UserLink = Backbone.RelationalModel.extend
    defaults:
        user: null
        type_name: "WEB"
        other_name: "Other Website"
        url_target: ""
    urlRoot: "/rest/user_link"

    toJSON: ->
        user: @get('user').id
        type_name: @get('type_name')
        other_name: @get('other_name')
        url_target: @get('url_target')
