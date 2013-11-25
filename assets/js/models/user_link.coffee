SpkrBar.Models.UserLink = Backbone.RelationalModel.extend
    defaults:
        type_name: "WEB"
        other_name: "Other Website"
        url_target: ""
    urlRoot: "/rest/user_link"
