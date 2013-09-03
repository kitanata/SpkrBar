SpkrBar.Views.Items.EngagementSpan6 = Backbone.Marionette.ItemView.extend
    template: Handlebars.compile($("#engagement-span6-templ").html())

    events:
        "click #delete-engagement": "onDeleteEngagement"

    initialize: ->
        @listenTo(@model, "change", @render)

    onDeleteEngagement: ->
        @model.destroy
            success: =>
                @remove()

    userAttending: ->
        if not spkrbar.user then return false
        spkrbar.user.id in @model.get('attendees')

    userEndorsed: ->
        if not spkrbar.user then return false
        spkrbar.user.id in @model.get('endorsements')

    userIsEventPlanner: ->
        if not spkrbar.user then return false
        spkrbar.user.get('is_event_planner')

    userOwnsEngagement: ->
        if not spkrbar.user then return false
        spkrbar.user.id == @model.get('user_id')

    willShowButtons: ->
        @userOwnsEngagement() or @userAttending() or not @userIsEventPlanner()

    formattedDate: ->
        moment(@model.get('date')).format('LLL')

    serializeData: ->
        id: @model.id
        talk_id: @model.get('talk')
        talk_url: @model.get('talk_url')
        talk_name: @model.get('talk_name')
        speaker_name: @model.get('speaker_name')
        event_url: @model.get('event_url')
        event_name: @model.get('event_name')
        city: @model.get('city')
        state: @model.get('state')
        date: @formattedDate()
        tags: _(@model.get('tags')).map (x) -> {'name': x}
        abstract: @model.get('abstract')
        confirmed: @model.get('confirmed')
        user_attending: @userAttending()
        user_endorsed: @userEndorsed()
        user_event_planner: @userIsEventPlanner()
        user_owned: @userOwnsEngagement()
        show_buttons: @willShowButtons()
