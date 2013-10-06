SpkrBar.Views.Engagement = Backbone.View.extend
    className: "engagement"
    template: "#engagement-templ"

    events:
        "click #delete-engagement": "onDeleteEngagement"

    initialize: (options) ->
        @location = options.location
        @talk = options.talk
        @listenTo(@model, "change", @render)

    onDeleteEngagement: () ->
        @model.destroy
            success: =>
                @remove()

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    userOwned: ->
        user.id == @talk.get('speaker').id

    eventUrl: ->
        "/event/" + _.str.slugify(@model.get('event_name'))

    context: ->
        id: @model.id
        event_name: @model.get('event_name')
        event_url: @eventUrl()
        room: @model.get('room')
        date: moment(@model.get('date')).format('LL')
        time: moment(@model.get('time'), "HH:mm:ss").format('hh:mm A')
        location_name: @location.get('name')
        address: @location.get('address')
        city: @location.get('city')
        state: @location.get('state')
        zip_code: @location.get('zip_code')
        userOwned: @userOwned()
