SpkrBar.Views.TalkEdit = Backbone.View.extend
    className: "talk-edit"
    template: "#talk-edit-templ"

    initialize: (options) ->

        unless @model
            @editing = false
            @model = new SpkrBar.Models.Talk()
            @model.set 'speaker', user

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
        @model.set 'name', @$el.find('#talk-name').val()
        @model.set 'abstract', @$el.find('#talk-abstract').val()

        console.log @model

        @model.save null, 
            success: =>
                $.colorbox.close()
