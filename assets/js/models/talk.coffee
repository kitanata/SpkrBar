SpkrBar.Models.Talk = Backbone.RelationalModel.extend
    defaults:
        speaker: null
        created_at: ""
        updated_at: ""
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
            autoFetch: true
        }
    ]

    urlRoot: "/rest/talk"

    toJSON: (options) ->
        speaker: @get('speaker').id
        name: @get('name')
        abstract: @get('abstract')
        comments: @get('comments')
        endorsements: @get('endorsements')
        engagements: @get('engagements')
        links: @get('links')
        tags: @get('tags')
        slides: @get('slides')
        videos: @get('videos')
        published: @get('published')
        created_at: @get('created_at')
        updated_at: @get('updated_at')
