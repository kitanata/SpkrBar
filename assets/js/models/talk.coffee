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
        }
    ]

    urlRoot: "/rest/talk"
