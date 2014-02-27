SpkrBar.Views.TalkThumbnail = Backbone.View.extend
    className: "talk_event"
    template: "#talk-thumbnail-templ"

    events:
        "click .endorse-talk": "onClickEndorseTalk"

    initialize: (options) ->
        @model.fetchRelated('tags')
        @model.fetchRelated('speaker')
        @model.fetchRelated('endorsements')

        @listenTo(@model, "change", @invalidate)
        @listenTo(@model.get('speaker'), "change", @invalidate)
        @listenTo(@model.get('tags'), "change", @invalidate)
        @listenTo(@model.get('endorsements'), "add remove change reset", @invalidate)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
        if not @shouldRender
            setTimeout =>
                @beforeRender()
                @render()
                @afterRender()
                @shouldRender = false
            , 500
            @shouldRender = true

    beforeRender: ->

    afterRender: ->
        @delegateEvents()

    userLoggedIn: ->
        user != null

    userOwnsContent: ->
        speaker = @model.get('speaker')
        user != null and speaker != null and user.id == speaker.id

    mapTalkTags: ->
        @model.get('tags').map (x) -> 
            return {name: x.get('name')}

    mapTalkAbstract: ->
        _.str.truncate(
            _.str.stripTags(
                markdown.toHTML(
                    @model.get('abstract')
                )
            ), 300)

    context: ->
        id: @model.id
        name: _.str.truncate(@model.get('name'), 38)
        speaker_name: @model.get('speaker').get('full_name')
        speaker_photo: @model.get('speaker').get('photo')
        abstract: @mapTalkAbstract()
        tags: @mapTalkTags()
        url: '/talk/' + @model.id
        userEndorsed: @model.userEndorsed()
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()

    onClickEndorseTalk: (el) ->
        newEndorsement = new SpkrBar.Models.TalkEndorsement
            talk: @model
            user: user
        newEndorsement.save null,
            success: =>
                @model.get('endorsements').add newEndorsement
