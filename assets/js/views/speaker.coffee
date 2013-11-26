SpkrBar.Views.Speaker = Backbone.View.extend
    className: "speaker"
    template: "#speaker-detail-templ"

    events:
        "click .follow-user": "onClickFollowUser"
        "click .unfollow-user": "onClickUnfollowUser"

    initialize: (options) ->
        @model.fetchRelated('tags')

        @listenTo(@model, "change", @invalidate)
        @listenTo(@model.get('tags'), "change", @invalidate)

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
        user != null and user == @model

    mapBiography: ->
        _.str.truncate(
            _.str.stripTags(
                markdown.toHTML(
                    @model.get('about_me')
                )
            ), 300)

    context: ->
        id: @model.id
        name: @model.get('full_name')
        about: @mapBiography()
        photo: @model.get('photo')
        url: '/profile/' + @model.get('id')
        tags: @model.get('tags').map (x) -> {id: x.id, name: x.get('name')}
        followedByUser: @model.userFollowingMe()
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()

    onClickFollowUser: ->
        @model.get('followers').add user
        @model.save()
        @invalidate()

    onClickUnfollowUser: ->
        @model.get('followers').remove user
        @model.save()
        @invalidate()
