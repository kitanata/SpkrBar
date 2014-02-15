SpkrBar.Models.User = Backbone.RelationalModel.extend
    defaults:
        full_name: ""
        about_me: ""
        photo: ""
        tags: []
        links: []
        plan_name: "speaker"
        is_event_manager: false

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
            key: 'engagements'
            relatedModel: 'SpkrBar.Models.Engagement'
        }
    ]

    urlRoot: "/rest/user"

    toJSON: ->
        email: @get('email')
        full_name: @get('full_name')
        plan_name: @get('plan_name')
        is_event_manager: @get('is_event_manager')
        about_me: @get('about_me')
        following: @get('following').map (x) -> x.id
        followers: @get('followers').map (x) -> x.id
        tags: @get('tags').map (x) -> x.id
        links: @get('links').map (x) -> x.id
        talks: @get('talks').map (x) -> x.id
        engagements: @get('engagements').map (x) -> x.id

    getFullName: ->
        return @get('full_name')

    setFullName: (fullName) ->
        words = _.str.words(fullName)

        last = ""
        if words.length >= 2
            last = words[1]

            if words.length > 2
                [last = last + " " + w for w in words[2...]]

        @set('first_name', words[0])
        @set('last_name', last)

    userFollowingMe: ->
        followerIds = @get('followers').map (x) ->
            if x.get('user')
                x.get('user').id
            else
                null
        user != null and _(followerIds).contains(user.id)
