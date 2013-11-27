SpkrBar.Views.EventThumbnail = Backbone.View.extend
    className: "event"
    template: "#event-thumbnail-templ"

    initialize: (options) ->
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

    mapTalkTags: ->
        @model.get('tags').map (x) -> 
            count: x[0]
            name: x[1]

    context: ->
        name: @model.get('name')
        num_talks: @model.get('numtalks')
        url: "/event/" + _.str.slugify(@model.get('name'))
        earliest_date: @model.get('earliest_date')
        earliest_time: @model.get('earliest_time')
        latest_date: @model.get('latest_date')
        latest_time: @model.get('latest_time')
        tags: @mapTalkTags()
