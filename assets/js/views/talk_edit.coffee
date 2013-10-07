SpkrBar.Views.TalkEdit = Backbone.View.extend
    className: "talk-edit"
    template: "#talk-edit-templ"

    events:
        "click #submit-talk": "onSaveTalk"

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
        $.colorbox
            html: @$el.html()
            width: "780px"
            height: "500px"

        $("#talk-abstract").markItUp();
 
    onSaveTalk: ->

