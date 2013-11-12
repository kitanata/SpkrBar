SpkrBar.Models.User = Backbone.RelationalModel.extend
    defaults:
        username: ""
        first_name: ""
        last_name: ""
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

    urlRoot: "/rest/user"

    toJSON: ->
        username: @get('username')
        email: @get('email')
        first_name: @get('first_name')
        last_name: @get('last_name')
        about_me: @get('about_me')
        following: @get('following').map (x) -> x.id
        followers: @get('followers').map (x) -> x.id
        tags: @get('tags').map (x) -> x.id
        links: @get('links').map (x) -> x.id
        talks: @get('talks').map (x) -> x.id
        engagements: @get('engagements').map (x) -> x.id

    getFullName: ->
        return @get('first_name') + " " + @get('last_name')

    setFullName: (fullName) ->
        words = _.str.words(fullName)

        last = ""
        if words.length >= 2
            last = words[1]

            if words.length > 2
                [last = last + " " + w for w in words[2...]]

        @set('first_name', words[0])
        @set('last_name', last)
