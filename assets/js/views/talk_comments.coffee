SpkrBar.Views.TalkComments = Backbone.View.extend
    className: "talk-comments"
    template: "#talk-comments-templ"

    events:
        "click .comment-reply": 'onCommentReply'
        "click .comment-delete": 'onCommentDelete'
        "click .comment-report": 'onCommentReport'

    initialize: (options) ->
        @talk = options.talk
        @listenTo(@collection, "change add remove", @render)

    onCommentReply: ->

    onCommentDelete: ->

    onCommentReport: ->

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    canComment: ->
        if user then true else false

    userOwnsContent: ->
        if not user then return false
        user.id == @talk.get('user')

    canDeleteComment: (comment) ->
        @userOwnsContent() or comment.user == user

    mapComment: (comment) ->
        'id': comment.id
        'name': comment.name
        'comment': comment.comment
        'datetime': comment.datetime
        'children': [@mapComment(child) for child in comment.children]
        'can_delete': @canDeleteComment(comment)

    context: ->
        comments: @collection.map (x) => @mapComment(x.get('comment'))
        can_comment: @canComment()
