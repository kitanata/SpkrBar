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

    getUserId: ->
        if @get('user') != null
            return @get('user').id
        else
            return null

    toJSON: (options) ->
        created_at: @get('created_at')
        updated_at: @get('updated_at')
        user: @getUserId()
        talk: @get('talk').id
