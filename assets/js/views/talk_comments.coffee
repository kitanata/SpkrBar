SpkrBar.Views.TalkComments = Backbone.View.extend
    className: "talk-comments"
    template: "#talk-comments-templ"

    events:
        "click .comment-create": 'onCommentCreate'

    initialize: (options) ->
        @talk = options.talk

        @commentViews = []
        @collection.each (x) =>
            comment = new SpkrBar.Models.Comment
                id: x.get('comment')
            comment.fetch 
                success: =>
                    view = new SpkrBar.Views.Comment
                        talk: @talk
                        model: comment
                    @commentViews.push view
                    @render()

    onCommentCreate: ->
        commentText = $('.comment-text').val()

        if commentText
            comment = new SpkrBar.Models.Comment
                user: user.id
                comment: commentText
                datetime: (new Date(Date.now())).toISOString()
            comment.save null,
                success: =>
                    talk_comment = new SpkrBar.Models.TalkComment
                        talk: @talk.id
                        comment: comment.id
                    talk_comment.save null, success: =>
                        @collection.add talk_comment
                        @comments.add comment

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

    context: ->
        can_comment: @canComment()
