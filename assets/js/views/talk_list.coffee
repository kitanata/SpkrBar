SpkrBar.Views.TalkList = Backbone.View.extend
    template: "#talk-list-templ"

    initialize: (options) ->
        @shouldRender = false

        @upcomingViews = []
        @recentViews = []

        @upcoming = options.upcoming
        @recent = options.recent

        @upcoming.each (engagement) =>
            newView = new SpkrBar.Views.EngagementDetail
                model: engagement
            @upcomingViews.push(newView)

        @recent.each (engagement) =>
            newView = new SpkrBar.Views.EngagementDetail
                model: engagement
            @recentViews.push(newView)

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
        $('.upcoming').html ""
        $('.recent').html ""

        _(@upcomingViews).each (view) =>
            $('.upcoming').append view.render().el

        _(@recentViews).each (view) =>
            $('.recent').append view.render().el

    userLoggedIn: ->
        user != null

    context: ->
        hasUpcoming: @upcomingViews.length != 0
