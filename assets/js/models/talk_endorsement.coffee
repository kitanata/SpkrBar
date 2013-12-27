SpkrBar.Models.TalkEndorsement = Backbone.RelationalModel.extend
    defaults:
        user: null
        talk: null
        created_at: ""
        updated_at: ""

    urlRoot: "/rest/talk_endorsement"

    relations: [
        {
            type: Backbone.HasOne
            key: 'user'
            relatedModel: 'SpkrBar.Models.User'
            reverseRelation: {
                key: 'endorsements'
            }
        }
    ]

    toJSON: (options) ->
        created_at: @get('created_at')
        updated_at: @get('updated_at')
        user: @get('user').id
        talk: @get('talk').id
