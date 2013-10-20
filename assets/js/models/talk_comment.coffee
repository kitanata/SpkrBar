SpkrBar.Models.TalkComment = Backbone.RelationalModel.extend
    defaults:
        commenter: null
        talk: null
        comment: ""
        created_at: ""
        updated_at: ""
        parent: null
        children: []

    urlRoot: "/rest/talk_comment"

    relations: [
        {
            type: Backbone.HasOne
            key: 'commenter'
            relatedModel: 'SpkrBar.Models.User'
            reverseRelation: {
                key: 'comment'
            }
        },
        {
            type: Backbone.HasOne
            key: 'parent'
            relatedModel: 'SpkrBar.Models.TalkComment'
            reverseRelation: {
                key: 'children'
            }
        }
    ]

    getParentId: ->
        if @get('parent') != null
            console.log @get('parent').id
            return @get('parent').id
        else
            return null

    toJSON: (options) ->
        comment: @get('comment')
        created_at: @get('created_at')
        updated_at: @get('updated_at')
        commenter: @get('commenter').id
        talk: @get('talk').id
        parent: @getParentId()
        children: @get('children').map (x) -> x.id
