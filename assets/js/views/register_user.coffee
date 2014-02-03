SpkrBar.Views.RegisterUser = Backbone.View.extend
    className: "register-user"
    template: "#register-user-templ"

    events:
        "click #register-submit": "onRegisterSubmit"

    initialize: (options) ->
        @alertTempl = Handlebars.compile($('#register-alert-templ').html())
        @listenTo(@model, "change", @render)

        if options.plan == 'forever'
            @model.set 'plan_name', "forever"
            @model.set 'is_event_planner', true
        else if options.plan == 'yearly'
            @model.set 'plan_name', 'yearly'
            @model.set 'is_event_planner', true


    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()
        @

    context: ->
        forever_plan: (@model.get('plan_name') == 'forever')
        yearly_plan: (@model.get('plan_name') == 'yearly')
        is_event_planner: @model.get 'is_event_planner'
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

    onRegisterSubmit: ->
        @model.set
            email: @$el.find('#email').val()
            password: @$el.find('#password').val()
            confirm: @$el.find('#confirm').val()
            full_name: @$el.find('#full_name').val()
            about_me: @$el.find('#about_me').val()

        console.log @model.isValid(true)

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
