SpkrBar.Views.RegisterUser = Backbone.View.extend
    className: "register-user"
    template: "#register-user-templ"

    events:
        "click #user-type-speaker": "onClickSpeaker"
        "click #user-type-yearly": "onClickYearly"
        "click #user-type-forever": "onClickForever"
        "click #register-submit": "onRegisterSubmit"

    initialize: (options) ->
        @alertTempl = Handlebars.compile($('#register-alert-templ').html())
        @listenTo(@model, "change", @render)

        @mode = "prereg"
        @plan = "speaker"

        if options.plan == 'forever' or options.plan == 'yearly'
            @plan = options.plan


    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()
        @

    context: ->
        forever_plan: (@plan == 'forever')
        yearly_plan: (@plan == 'yearly')
        is_event_planner: (@plan == 'forever' or @plan == 'yearly')
        email: @model.get 'email'
        password: @model.get 'password'
        confirm: @model.get 'confirm'
        full_name: @model.get 'full_name'
        about_me: @model.get 'about_me'

    afterRender: ->
        Backbone.Validation.bind this, 
            valid: (view, attr) =>
                @$el.find('#' + attr + '-error').text ''
                $.colorbox.resize()
            invalid: (view, attr, error) =>
                @$el.find('#' + attr + '-error').text '(' + error + ')'
                $.colorbox.resize()
        $.colorbox.resize()

    onClickSpeaker: ->    
        @plan = 'speaker'

    onClickYearly: ->
        @plan = 'yearly'

    onClickForever: ->
        @plan = 'forever'

    onRegisterSubmit: ->
        @model.set
            email: @$el.find('#email').val()
            password: @$el.find('#password').val()
            confirm: @$el.find('#confirm').val()
            full_name: @$el.find('#full_name').val()
            about_me: @$el.find('#about_me').val()
            plan_name: @plan

        console.log @plan

        if @plan == "speaker"
            @model.set 'is_event_planner', false
        else
            @model.set 'is_event_planner', true

        if @model.isValid(true)
            @model.save null,
                success: =>
                    window.location = '/'
                error: (model, xhr, options) =>
                    error = JSON.parse(xhr.responseText)
                    if error.error == "email_taken"
                        html = @alertTempl({error: "An account with that email has already been registered."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
                    else if error.error == "password_match"
                        html = @alertTempl({error: "Your passwords do not match."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
