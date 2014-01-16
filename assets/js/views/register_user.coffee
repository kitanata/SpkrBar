SpkrBar.Views.RegisterUser = Backbone.View.extend
    className: "register-user"
    template: "#register-user-templ"

    events:
        "click #register-submit": "onRegisterSubmit"

    initialize: (options) ->
        @listenTo(@model, "change", @render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()
        @

    context: ->
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

    onRegisterSubmit: ->
        @model.set 'email', @$el.find('#email').val()
        @model.set 'password', @$el.find('#password').val()
        @model.set 'confirm', @$el.find('#confirm').val()
        @model.set 'full_name', @$el.find('#full_name').val()
        @model.set 'about_me', @$el.find('#about_me').val()

        console.log @model.isValid(true)

        if @model.isValid(true)
            @model.save null,
                success: =>
                    $.colorbox.close()
