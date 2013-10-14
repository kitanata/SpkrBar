SpkrBar.Views.Comment = Backbone.View.extend
    className: "comment"
    template: "#comment-templ"

    events:
        "click .reply-comment": "onClickReply"
        "click .edit-comment": "onClickEdit"
        "click .delete-comment": "onClickDelete"
        "click .submit-comment": "onClickSubmit"

    initialize: (options) ->
        @parent = options.parent
        @commenter = options.commenter

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    userLoggedIn: ->
        user != null

    userOwnsComment: ->
        user.id == @commenter.id

    context: ->
        userLoggedIn: @userLoggedIn()
        userOwnsComment: @userOwnsComment()
        id: @model.id
        commenter: @commenter.get('full_name')
        comment: @model.get('comment')

    toggleReplyArea: ->
        @$el.find('.edit-reply-area').toggle()

    onClickReply: ->
        @toggleReplyArea()
        @$el.find('.submit-comment').text "Reply"

    onClickEdit: ->
        @toggleReplyArea()
        @$el.find('.comment-area').val @model.get('comment')
        @$el.find('.submit-comment').text "Save"

    onClickDelete: ->
        @parent.deleteComment(@)

    onClickSubmit: ->
        console.log "submit"
