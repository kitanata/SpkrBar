SpkrBar.Models.Talk = Backbone.RelationalModel.extend
    defaults:
        speaker: null
        name: ""
        abstract: ""
        published: false
        endorsements: []
        engagements: []
        comments: []
        tags: []
        links: []
        slides: []
        videos: []

    relations: [
        {
            type: Backbone.HasMany
            key: 'tags'
            relatedModel: 'SpkrBar.Models.TalkTag'
        },
        {
            type: Backbone.HasMany
            key: 'engagements'
            relatedModel: 'SpkrBar.Models.Engagement'
            reverseRelation: {
                key: 'talk'
            }
        },
        {
            type: Backbone.HasMany
            key: 'comments'
            relatedModel: 'SpkrBar.Models.TalkComment'
            collectionType: 'SpkrBar.Collections.TalkComments'
            reverseRelation: {
                key: 'talk'
            }
        },
        {
            type: Backbone.HasOne
            key: 'speaker'
            relatedModel: 'SpkrBar.Models.User'
            reverseRelation: {
                key: 'talks'
            }
        },
        {
            type: Backbone.HasMany
            key: 'endorsements'
            relatedModel: 'SpkrBar.Models.TalkEndorsement'
        }
    ]

    urlRoot: "/rest/talk"

    userEndorsed: ->
        if user == null
            return false
        else
            users_endorsed = @get('endorsements').map (x) -> 
                if x.get('user')
                    x.get('user').id
                else
                    null
            _(users_endorsed).contains(user.id)

    toJSON: (options) ->
        speaker: @get('speaker').id
        name: @get('name')
        abstract: @get('abstract')
        comments: @get('comments')
        endorsements: @get('endorsements')
        engagements: @get('engagements').map (x) -> x.id
        links: @get('links')
        tags: @get('tags').map (x) -> x.id
        slides: @get('slides')
        videos: @get('videos')
        published: @get('published')
        created_at: @get('created_at')
        updated_at: @get('updated_at')
