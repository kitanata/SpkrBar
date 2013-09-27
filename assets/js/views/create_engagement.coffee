SpkrBar.Views.CreateEngagement = Backbone.View.extend
    className: "create-engagement"
    template: "#create-engagement-templ"

    events:
        "click #loc-reset": "onClickLocationReset"
        "click #submit-engagement": "onClickSubmit"
        "change #loc-name": "onChangedLocationName"

    initialize: (options) ->
        @talk = options.talk
        @locations = options.locations
        @curLocation = null
        @parent = options.parent

        @model = new SpkrBar.Models.Engagement()

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))

        dateControl = @$el.find('#date').datepicker
            format: 'yyyy-mm-dd'

        @$el.find('#date').on 'changeDate', =>
            @$el.find('#date').datepicker('hide')

        @timePicker = @$el.find('#time').timepicker
          template: false,
          showInputs: false,
          minuteStep: 5

        @$el.find("#loc-name").typeahead
            source: @locations.map (x) -> x.get('name')
            updater: (item) =>
                @curLocation = @locations.find (x) -> x.get('name') == item
                if @curLocation
                    @$el.find('#loc-address').val(@curLocation.get('address'))
                    @$el.find('#loc-city').val(@curLocation.get('city'))
                    @$el.find('#loc-state').val(@curLocation.get('state'))
                    @$el.find('#loc-zip').val(@curLocation.get('zip_code'))
                item

        @

    context: ->
        {}

    onClickLocationReset: ->
        @$el.find('#loc-name').val('')
        @resetFields()

    onChangedLocationName: (el) ->
        text = $(el.currentTarget).val()
        location = @locations.find (x) => 
            x.get('name') == text

        unless location
            @resetFields()

    resetFields: ->
            @$el.find('#loc-address').val('');
            @$el.find('#loc-city').val('');
            @$el.find('#loc-state').val('');
            @$el.find('#loc-zip').val('');

    onClickSubmit: ->
        @model.set 'talk', @talk.id
        @model.set 'event_name', @$el.find('#event-name').val()
        @model.set 'room', @$el.find('#room').val()
        @model.set 'date', @$el.find('#date').val()

        time = moment(@timePicker.val(), 'h:mm a').format('HH:mm:ss')
        @model.set 'time', time

        if @curLocation
            @model.set 'location', @curLocation.id
            @validateAndSaveModel()
        else
            newLocation = new SpkrBar.Models.Location
                name: @$el.find('#loc-name').val();
                address: @$el.find('#loc-address').val();
                city: @$el.find('#loc-city').val();
                state: @$el.find('#loc-state').val();
                zip_code: @$el.find('#loc-zip').val();

            if newLocation.isValid(true)
                newLocation.save null,
                    success: ->
                        @curLocation = newLocation
                        @locations.add @curLocation
                        @model.set 'location', @curLocation.id
                        @validateAndSaveModel()
            else
                @showValidationAlert()

    validateAndSaveModel: ->
        if @model.isValid(true)
            @model.save null, 
                success: =>
                    $.colorbox.close()
                    @parent.engagements.add @model
        else
            @showValidationAlert()

    showValidationAlert: ->
        @$el.find('#req-alert').show().text("All the fields are required.")
        $.colorbox.resize()

