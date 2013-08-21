SpkrBar.Views.TalkTags = Backbone.View.extend
    className: "talk-tags"
    template: "#talk-tags-templ"

    events:
        "click .add-talk-tag": 'onAddTalkTag'
        "click .delete-talk-tag": 'onDeleteTalkTag'

    initialize: (options) ->
        @talk = options.talk
        @listenTo(@collection, "change add remove", @render)

    onAddTalkTag: ->
        name = $('#new-talk-tag-name').val()

        newTag = new SpkrBar.Models.TalkTag
            talk: @talk.id
            name: name
        newTag.save()
        @collection.add newTag

    onDeleteTalkTag: (el) ->
        tagId = $(el.currentTarget).data('id')
        deadTag = @collection.find (x) => x.id == tagId

        deadTag.destroy
            success: =>
                @collection.remove deadTag

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    userOwnsContent: ->
        if not user then return false
        user.id == @talk.get('user')


    context: ->
        tags: @collection.map (x) -> {'id': x.id, 'tag': x.get('name')}
        user_owned: @userOwnsContent()
