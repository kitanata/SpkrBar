SpkrBar.Views.Comment = Backbone.View.extend
    className: "comments"
    template: "#comment-templ"

    events:
        "click .comment-reply": 'onCommentReply'
        "click .comment-reply-create": 'onCommentReplyCreate'
        "click .comment-delete": 'onCommentDelete'
        "click .comment-report": 'onCommentReport'

    initialize: (options) ->
        @talk = options.talk

        children = @model.get('children')

        @commentViews = []
        _(children).each (x) =>
            comment = new SpkrBar.Models.Comment
                id: x
            comment.fetch 
                success: =>
                    view = new SpkrBar.Views.Comment
                        talk: @talk
                        model: comment
                    @commentViews.push view
                    @render()

    onCommentReply: ->
        console.log @model.id
        $(".reply-area[data-id='#{@model.id}']").toggle()

    onCommentReplyCreate: (el) ->
        comId = $(el.currentTarget).data('id')
        commentText = $('.comment-text[data-id=' + comId + ']').val()
        parent = @comments.find (x) => x.id == comId

        comment = new SpkrBar.Models.Comment
            user: user.id
            comment: commentText
            datetime: (new Date(Date.now())).toISOString()
            parent: parent.id

        comment.save null,
            success: =>
                parent.fetch() #refetch the parent to assign children

    onCommentDelete: (el) ->
        comId = $(el.currentTarget).data('id')
        comToDelete = @comments.find (x) => x.id == comId
        talkComToDelete = @collection.find (x) => x.get('comment') == comId

        if talkComToDelete
            talkComToDelete.destroy
                success: =>
                    @collection.remove talkComToDelete

        if comToDelete
            comToDelete.destroy
                success: =>
                    @comments.remove comToDelete

    onCommentReport: ->
        console.log "Report Comment"

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))

        commentArea = @$el.find('.comment-root')

        _(@commentViews).each (x) =>
            commentArea.append(x.render().el)

        @

    canComment: ->
        if user then true else false

    userOwnsContent: ->
        if not user then return false
        user.id == @talk.get('user')

    canDeleteComment: ->
        @userOwnsContent() or @model.get('user') == user.id

    context: ->
        id: @model.id
        name: @model.get('name')
        comment: @model.get('comment')
        datetime: moment(@model.get('datetime')).fromNow()
        can_delete: @canDeleteComment()
        can_comment: @canComment()
