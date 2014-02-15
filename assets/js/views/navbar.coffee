SpkrBar.Views.NavBar = Backbone.View.extend
    template: "#navbar-templ"

    events:
        "click #add-talk-navbar": "onClickAddTalk"
        "click #register-user-navbar": "onClickRegisterUser"

    initialize: (options) ->
        if user
            @listenTo(user, 'change', @render)

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

    userLoggedIn: ->
        user != null

    userIsStaff: ->
        user != null and user.is_staff == true

    userOwnsContent: ->
        user != null and user.id == @model.get('speaker').id

    userIsEventPlanner: ->
        user != null and user.get('is_event_manager')

    userProfileLink: ->
        if user == null
            ""
        else
            user.get('url')

    context: ->
        userLoggedIn: @userLoggedIn()
        userIsStaff: @userIsStaff()
        userIsEventPlanner: @userIsEventPlanner()
        profileLink: @userProfileLink()

    onClickAddTalk: ->
        editor = new SpkrBar.Views.TalkEdit
            model: null

        $.colorbox
            html: editor.render().el
            width: "700px"
            height: "520px"

    onClickRegisterUser: ->
        regModel = new SpkrBar.Models.Register()

        editor = new SpkrBar.Views.RegisterUser
            model: regModel

        $.colorbox
            html: editor.render().el
            width: "500px"
            height: "440px"
        $.colorbox.resize()
