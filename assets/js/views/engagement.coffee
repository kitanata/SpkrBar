SpkrBar.Views.Engagement = Backbone.View.extend
    className: "engagement"
    template: "#engagement-templ"

    events:
        "click #delete-engagement": "onDeleteEngagement"

    initialize: ->
        @listenTo(@model, "change", @render)

    onDeleteEngagement: () ->
        @model.destroy
            success: =>
                @remove()

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        if not @model.get('confirmed')
            @$el.addClass('muted')
        @

    userAttending: ->
        if not user then return false
        user.id in @model.get('attendees')

    userEndorsed: ->
        if not user then return false
        user.id in @model.get('endorsements')

    userIsEventPlanner: ->
        if not user then return false
        user.get('is_event_planner')

    userOwnsEngagement: ->
        if not user then return false
        user.id == @model.get('user_id')

    willShowButtons: ->
        @userOwnsEngagement() or @userAttending() or not @userIsEventPlanner()

    context: ->
        id: @model.id
        talk_id: @model.get('talk')
        talk_url: @model.get('talk_url')
        talk_name: @model.get('talk_name')
        speaker_name: @model.get('speaker_name')
        event_url: @model.get('event_url')
        event_name: @model.get('event_name')
        city: @model.get('city')
        state: @model.get('state')
        date: @model.get('formatted_date')
        time: @model.get('formatted_time')
        tags: _(@model.get('tags')).map (x) -> {'name': x}
        abstract: @model.get('abstract')
        confirmed: @model.get('confirmed')
        user_attending: @userAttending()
        user_endorsed: @userEndorsed()
        user_event_planner: @userIsEventPlanner()
        user_owned: @userOwnsEngagement()
        show_buttons: @willShowButtons()
