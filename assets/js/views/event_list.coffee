SpkrBar.Views.EventList = Backbone.View.extend
    template: "#event-list-templ"

    initialize: (options) ->
        @shouldRender = false

        @eventViews = []

        @collection.each (event) =>
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
        $('.event-list').html ""

        _(@eventViews).each (view) =>
            $('.event-list').append view.render().el

    context: ->
        {}
