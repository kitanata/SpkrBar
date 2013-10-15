SpkrBar.Models.TalkComment = Backbone.RelationalModel.extend
    defaults:
        commenter: ""
        comment: ""
        created_at: ""
        updated_at: ""
        children: []

    urlRoot: "/rest/talk_comment"
