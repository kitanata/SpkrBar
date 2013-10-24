SpkrBar.Models.User = Backbone.RelationalModel.extend
    defaults:
        username: ""
        full_name: ""
        email: ""
        following: []
        followers: []
        tags: []
        links: []

    relations: [
        {
            type: Backbone.HasMany
            key: 'tags'
            relatedModel: 'SpkrBar.Models.UserTag'
        },
        {
            type: Backbone.HasMany
            key: 'links'
            relatedModel: 'SpkrBar.Models.UserLink'
        },
        {
            type: Backbone.HasMany
            key: 'followers'
            relatedModel: 'SpkrBar.Models.User'
        },
        {
            type: Backbone.HasMany
            key: 'following'
            relatedModel: 'SpkrBar.Models.User'
        },
        {
            type: Backbone.HasMany
            key: 'talks'
            relatedModel: 'SpkrBar.Models.Talk'
        },
        {
            type: Backbone.HasMany
            key: 'engagements'
            relatedModel: 'SpkrBar.Models.Engagement'
        }
    ]

    urlRoot: "/user"
