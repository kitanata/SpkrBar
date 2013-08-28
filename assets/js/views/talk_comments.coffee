SpkrBar.Views.TalkComments = Backbone.View.extend
    className: "talk-comments"
    template: "#talk-comments-templ"

    events:
        "click .add-talk-link": 'onAddTalkLink'
        "click .delete-talk-link": 'onDeleteTalkLink'

    initialize: (options) ->
        @talk = options.talk
        @listenTo(@collection, "change add remove", @render)

    onAddTalkLink: ->
        name = $('#new-talk-link-name').val()
        url = $('#new-talk-link-url').val()

        newLink = new SpkrBar.Models.TalkLink
            talk: @talk.id
            name: name
            url: url
        newLink.save()
        @collection.add newLink

    onDeleteTalkLink: (el) ->
        linkId = $(el.currentTarget).data('id')
        deadLink = @collection.find (x) => x.id == linkId

        deadLink.destroy
            success: =>
                @collection.remove deadLink

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    userOwnsContent: ->
        if not user then return false
        user.id == @talk.get('user')

    context: ->
        links: @collection.map (x) -> {'id': x.id, 'name': x.get('name'), 'url': x.get('url')}
        user_owned: @userOwnsContent()
