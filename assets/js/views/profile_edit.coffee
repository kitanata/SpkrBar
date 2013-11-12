SpkrBar.Views.ProfileEdit = Backbone.View.extend
    className: "profile-edit"
    template: "#profile-edit-templ"

    initialize: (options) ->
        @listenTo(@model, "change", @render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()
        @

    context: ->
        name: @model.getFullName()
        about: @model.get('about_me')

    afterRender: ->
        @$el.find("#about-me").markItUp(SpkrBar.markdownSettings);
        @$el.find("#submit-profile").on 'click', =>
            @onSaveProfile()

    onSaveProfile: ->
        @model.setFullName $('#profile-name').val()
        @model.set 'about_me', $('#about-me').val()

        @model.save null, 
            success: =>
                $.colorbox.close()
