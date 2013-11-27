SpkrBar.Views.SearchPage = Backbone.View.extend
    template: "#search-templ"

    initialize: (options) ->
        @shouldRender = false

        @talkViews = []
        @speakerViews = []
        @eventViews = []

        @talks = options.talks
        @speakers = options.speakers
        @events = options.events

        @talks.each (talk) =>
            newView = new SpkrBar.Views.TalkThumbnail
                model: talk
            @talkViews.push(newView)

        @speakers.each (speaker) =>
            newView = new SpkrBar.Views.Speaker
                model: speaker
            @speakerViews.push(newView)

        @events.each (event) =>
            newView = new SpkrBar.Views.EventThumbnail
                model: event
            @eventViews.push(newView)

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
        $('.speaker-list').html ""
        $('.event-list').html ""

        _(@talkViews).each (view) =>
            $('.talk-list').append view.render().el

        _(@speakerViews).each (view) =>
            $('.speaker-list').append view.render().el

        _(@eventViews).each (view) =>
            $('.event-list').append view.render().el

    userLoggedIn: ->
        user != null

    hasTalks: ->
        @talks.size() != 0

    hasSpeakers: ->
        @speakers.size() != 0

    hasEvents: ->
        @events.size() != 0

    hasResults: ->
        @hasEvents() or @hasTalks() or @hasSpeakers()

    context: ->
        hasResults: @hasResults()
        hasSpeakers: @hasSpeakers()
        hasTalks: @hasTalks()
        hasEvents: @hasEvents()
