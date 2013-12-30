SpkrBar.Views.SpeakerList = Backbone.View.extend
    template: "#speaker-list-templ"

    initialize: (options) ->
        @shouldRender = false

        @speakerViews = []

        @collection.each (speaker) =>
            newView = new SpkrBar.Views.Speaker
                model: speaker
            @speakerViews.push(newView)

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
        $('.speaker-list').html ""

        _(@speakerViews).each (view) =>
            $('.speaker-list').append view.render().el

    userLoggedIn: ->
        user != null

    context: ->
        {}
