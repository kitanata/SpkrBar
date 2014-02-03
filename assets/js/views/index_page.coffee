SpkrBar.Views.IndexPage = Backbone.View.extend
    template: "#index-templ"

    events:
        "click .invite-register": "onClickInviteRegister"
        "click .yearly-register": "onClickYearlyRegister"
        "click .forever-register": "onClickForeverRegister"
        "click .speaker-register": "onClickSpeakerRegister"

    initialize: (options) ->
        @shouldRender = false

        @talkViews = []

        @collection.each (talk) =>
            newView = new SpkrBar.Views.TalkThumbnail
                model: talk
            @talkViews.push(newView)

        @invalidate()

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
        $('.talk-list').html ""

        _(@talkViews).each (view) =>
            $('.talk-list').append view.render().el

    userLoggedIn: ->
        user != null

    context: ->
        {}

    onClickInviteRegister: ->
        console.log "Invite Register"

    onClickYearlyRegister: ->
        regModel = new SpkrBar.Models.Register()

        editor = new SpkrBar.Views.RegisterUser
            model: regModel
            plan: "yearly"

        $.colorbox
            html: editor.render().el
            width: "500px"
            height: "540px"

    onClickForeverRegister: ->
        regModel = new SpkrBar.Models.Register()

        editor = new SpkrBar.Views.RegisterUser
            model: regModel
            plan: "forever"

        $.colorbox
            html: editor.render().el
            width: "500px"
            height: "540px"

    onClickSpeakerRegister: ->
        regModel = new SpkrBar.Models.Register()

        editor = new SpkrBar.Views.RegisterUser
            model: regModel

        $.colorbox
            html: editor.render().el
            width: "500px"
            height: "440px"
