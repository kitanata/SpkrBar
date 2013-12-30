SpkrBar.Models.UserFollowing = Backbone.RelationalModel.extend
    defaults:
        user: null
        following: null
        created_at: ""
        updated_at: ""

    urlRoot: "/rest/user_follow"

    relations: [
        {
            type: Backbone.HasOne
            key: 'user'
            relatedModel: 'SpkrBar.Models.User'
            reverseRelation: {
                key: 'following'
            }
        },
        {
            type: Backbone.HasOne
            key: 'following'
            relatedModel: 'SpkrBar.Models.User'
            reverseRelation: {
                key: 'followers'
            }
        },
    ]

    toJSON: ->
        user: @get('user').id
        following: @get('following').id
        created_at: @get('created_at')
        updated_at: @get('updated_at')
