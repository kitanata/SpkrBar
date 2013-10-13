SpkrBar.Views.TalkEdit = Backbone.View.extend
    className: "talk-edit"
    template: "#talk-edit-templ"

    initialize: (options) ->
        @listenTo(@model, "change", @render)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()
        @

    context: ->
        name: @model.get('name')
        abstract: @model.get('abstract')

    afterRender: ->
        @$el.find("#talk-abstract").markItUp(SpkrBar.markdownSettings);
        @$el.find("#submit-talk").on 'click', =>
            @onSaveTalk()

    onSaveTalk: ->
        @model.set 'name', $('#talk-name').val()
        @model.set 'abstract', $('#talk-abstract').val()

        @model.save null, 
            success: =>
                $.colorbox.close()
