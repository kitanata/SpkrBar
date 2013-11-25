SpkrBar.Views.NavBar = Backbone.View.extend
    template: "#navbar-templ"

    events:
        "click #add-talk-navbar": "onClickAddTalk"

    initialize: (options) ->
        @listenTo(user, 'change', @render)

    render: ->
        console.log "Render"
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
        console.log "Invalidate"
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

    userLoggedIn: ->
        user != null

    userIsStaff: ->
        user != null and user.is_staff == true

    userOwnsContent: ->
        user != null and user.id == @model.get('speaker').id

    context: ->
        userLoggedIn: @userLoggedIn()
        userIsStaff: @userIsStaff()
        profileLink: user.get('url')

    onClickAddTalk: ->
        editor = new SpkrBar.Views.TalkEdit
            model: null

        $.colorbox
            html: editor.render().el
            width: "700px"
            height: "520px"
