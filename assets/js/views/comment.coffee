SpkrBar.Views.Comment = Backbone.View.extend
    className: "comment"
    template: "#comment-templ"

    events:
        "click .reply-comment": "onClickReply"
        "click .edit-comment": "onClickEdit"
        "click .delete-comment": "onClickDelete"
        "click .submit-comment": "onClickSubmit"

    initialize: (options) ->
        @talk = options.talk
        @parent = options.parent
        @mode = 'read'
        @childComments = []

        @listenTo(@model, "change", @render)
        @listenTo(@model.get('commenter'), "change", @render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()

        @

    afterRender: ->
        _(@childComments).each (comView) =>
            @$el.find('.comment-list[data-id=' + @model.id + ']').append comView.render().el

        @delegateEvents()

    userLoggedIn: ->
        user != null

    userOwnsComment: ->
        user.id == @model.get('commenter').id

    context: ->
        userLoggedIn: @userLoggedIn()
        userOwnsComment: @userOwnsComment()
        id: @model.id
        created_at: _.str.capitalize(moment(@model.get('created_at')).fromNow())
        commenter: @model.get('commenter').get('full_name')
        comment: @model.get('comment')

    onClickReply: (el) ->
        commentId = $(el.currentTarget).data('id')

        if commentId != @model.id
            return false

        if @mode == 'reply'
            @$el.find('.edit-reply-area[data-id=' + commentId + ']').toggle()
        else
            @$el.find('.edit-reply-area[data-id=' + commentId + ']').show()
            @mode = 'reply'

        @$el.find('.comment-area[data-id=' + commentId + ']').val ""
        @$el.find('.submit-comment[data-id=' + commentId + ']').text "Reply"

        el.stopPropagation()

    onClickEdit: (el) ->
        commentId = $(el.currentTarget).data('id')

        if commentId != @model.id
            return true

        if @mode == 'edit'
            @$el.find('.edit-reply-area[data-id=' + commentId + ']').toggle()
        else
            @$el.find('.edit-reply-area[data-id=' + commentId + ']').show()
            @mode = 'edit'

        @$el.find('.comment-area[data-id=' + commentId + ']').val @model.get('comment')
        @$el.find('.submit-comment[data-id=' + commentId + ']').text "Save"

        el.stopPropagation()

    onClickDelete: (el) ->
        commentId = $(el.currentTarget).data('id')

        if commentId != @model.id
            return true

        if @model.get('children').length != 0
            @model.set 'comment', "[DELETED]"
            @model.save()
        else
            @parent.deleteComment(@)

        el.stopPropagation()

    onClickSubmit: (el) ->
        commentId = $(el.currentTarget).data('id')

        if commentId != @model.id
            return true

        if @mode == 'edit'
            @model.set 'comment', @$el.find('.comment-area[data-id=' + @model.id + ']').val()
            @model.save()
        else
            newComment = new SpkrBar.Models.TalkComment
                talk: @talk
                parent: @model
                commenter: user
                comment: @$el.find('.comment-area[data-id=' + @model.id + ']').val()

            newComment.save null, 
                success: => 
                    commentView = new SpkrBar.Views.Comment
                        parent: @
                        talk: @talk
                        model: newComment
                        commenter: user
                    @childComments.push commentView
                    @render()

            @model.fetch()

        el.stopPropagation()

    deleteComment: (commentView) ->
        @childComments = _(@childComments).without commentView
        commentView.model.destroy()
        @render()
