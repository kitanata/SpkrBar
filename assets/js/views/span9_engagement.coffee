SpkrBar.Views.Span9Engagement = Backbone.View.extend
    className: "span9-engagement"
    template: "#span9-engagement-templ"

    events:
        "click .icon":          "open",
        "click .button.edit":   "openEditDialog",
        "click .button.delete": "destroy"

    initialize: ->
        this.listenTo(this.model, "change", this.render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    context: ->
        show_buttons: false
        talk_url: @model.get('talk_url')
        talk_name: @model.get('talk_name')
        speaker_name: @model.get('speaker_name')
        event_url: @model.get('event_url')
        event_name: @model.get('event_name')
        city: @model.get('city')
        state: @model.get('state')
        date: @model.get('date')
        time: @model.get('time')
        tags: _(@model.get('tags')).map (x) -> {'name': x}
        abstract: @model.get('abstract')
