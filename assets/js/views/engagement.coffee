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
        @

    userOwnsEngagement: ->
        user.id == @model.get('user_id')

    context: ->
        id: @model.id
        event_name: @model.get('event_name')
        room: @model.get('room')
        date: moment(@model.get('date')).format('LL')
        time: moment(@model.get('time'), "HH:mm:ss").format('hh:mm A')
        location_name: @model.get('location').name
        address: @model.get('location').address
        city: @model.get('location').city
        state: @model.get('location').state
        zip_code: @model.get('location').zip_code
        user_owned: @userOwnsEngagement()
        active: @model.get('active')
        show_buttons: true
