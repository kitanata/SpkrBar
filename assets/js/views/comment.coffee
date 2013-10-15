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
        @commenter = options.commenter
        @mode = 'read'
        @commentViews = []

        @listenTo(@model, "change", @render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()

        @

    afterRender: ->
        _(@commentViews).each (comView) =>
            @$el.find('.comment-list').append comView.render().el

    userLoggedIn: ->
        user != null

    userOwnsComment: ->
        user.id == @commenter.id

    context: ->
        userLoggedIn: @userLoggedIn()
        userOwnsComment: @userOwnsComment()
        id: @model.id
        created_at: @model.get('created_at')
        commenter: @commenter.get('full_name')
        comment: @model.get('comment')

    onClickReply: ->
        if @mode == 'reply'
            @$el.find('.edit-reply-area').toggle()
        else
            @$el.find('.edit-reply-area').show()
            @mode = 'reply'

        @$el.find('.comment-area').val ""
        @$el.find('.submit-comment').text "Reply"

    onClickEdit: ->
        if @mode == 'edit'
            @$el.find('.edit-reply-area').toggle()
        else
            @$el.find('.edit-reply-area').show()
            @mode = 'edit'

        @$el.find('.comment-area').val @model.get('comment')
        @$el.find('.submit-comment').text "Save"

    onClickDelete: ->
        @parent.deleteComment(@)

    onClickSubmit: ->
        if @mode == 'edit'
            @model.set 'comment', @$el.find('.comment-area').val()
            @model.save()
        else
            newComment = new SpkrBar.Models.TalkComment
                talk: @talk.id
                parent: @model.id
                commenter: user.id
                comment: @$el.find('.comment-area').val()

            newComment.save null, 
                success: => 
                    commentView = new SpkrBar.Views.Comment
                        parent: @
                        talk: @parent.model
                        model: newComment
                        commenter: user
                    @commentViews.push commentView

            @model.fetch()
