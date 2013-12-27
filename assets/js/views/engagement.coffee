SpkrBar.Views.Engagement = Backbone.View.extend
    className: "engagement"
    template: "#engagement-templ"

    events:
        "click #delete-engagement": "onDeleteEngagement"

    initialize: (options) ->
        @model.fetchRelated('location')
        @talk = options.talk
        @listenTo(@model, "change", @render)

    onDeleteEngagement: ->
        console.log "onDeleteEngagement"
        @talk.get('engagements').remove(@model)
        @model.destroy
            success: =>
                @remove()

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

        @delegateEvents()

    userOwned: ->
        user != null and user.id == @talk.get('speaker').id

    eventUrl: ->
        "/event/" + _.str.slugify(@model.get('event_name'))

    context: ->
        id: @model.id
        event_name: @model.get('event_name')
        event_url: @eventUrl()
        room: @model.get('room')
        date: moment(@model.get('date')).format('LL')
        time: moment(@model.get('time'), "HH:mm:ss").format('hh:mm A')
        location_name: @model.get('location').get('name')
        address: @model.get('location').get('address')
        city: @model.get('location').get('city')
        state: @model.get('location').get('state')
        zip_code: @model.get('location').get('zip_code')
        userOwned: @userOwned()
