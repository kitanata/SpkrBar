SpkrBar.Views.CreateEngagement = Backbone.View.extend
    className: "create-engagement"
    template: "#create-engagement-templ"

    initialize: (options) ->
        @talk = options.talk

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))

        @$el.find('#date').datepicker
            format: 'mm/dd/yyyy'

        @$el.find('#date').on 'changeDate', =>
            @$el.find('#date').datepicker('hide')

        @$el.find('#time').timepicker
          template: false,
          showInputs: false,
          minuteStep: 5

        @

    context: ->
        {}
