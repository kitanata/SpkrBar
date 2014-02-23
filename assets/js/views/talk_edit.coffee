SpkrBar.Views.TalkEdit = Backbone.View.extend
    className: "talk-edit"
    template: "#talk-edit-templ"

    initialize: (options) ->
        if @model
            @listenTo(@model, "change", @render)
            @controlLabel "Edit Talk"
        else
            @controlLabel = "Add Talk"

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @afterRender()
        @

    context: ->
        label: @controlLabel
        name: if @model then @model.get('name') else ""
        abstract: if @model then @model.get('abstract') else ""

    afterRender: ->
        @$el.find("#talk-abstract").markItUp(SpkrBar.markdownSettings);
        @$el.find("#submit-talk").on 'click', =>
            @onSaveTalk()

    onSaveTalk: ->
        name = @$el.find('#talk-name').val()
        about = @$el.find('#talk-abstract').val()

        unless @model        
            @model = new SpkrBar.Models.Talk()
            @model.set 'speaker', user

        @model.set 'name', name
        @model.set 'abstract', about

        @model.save null, 
            success: =>
                $.colorbox.close()
