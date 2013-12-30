SpkrBar.Views.IndexPage = Backbone.View.extend
    template: "#index-templ"

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
