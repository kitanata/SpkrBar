SpkrBar.Views.Notification = Backbone.View.extend
    className: "notification"
    template: "#notification-templ"

    events:
        "click .dismiss": "onDismiss"
        "click #confirm-engagement": "onConfirmEngagement"
        "click #decline-engagement": "onDeclineEngagement"

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    context: ->
        title: @model.get('title')
        message: @model.get('message')

    hide: ->
        @$el.fadeOut 400, "swing"

    show: ->
        @$el.fadeIn 400, "swing"

    onDismiss: ->
        @model.set('dismissed', true)
        @model.save()
        @hide()

    onConfirmEngagement: (el) ->
        id = $(el.currentTarget).data('id')
        engagement = new SpkrBar.Models.Engagement
            id: id
        engagement.fetch()
        engagement.confirmed = true
        engagement.save()
        @hide()

    onDeclineEngagement: (el) ->
        id = $(el.currentTarget).data('id')
        engagement = new SpkrBar.Models.Engagement
            id: id
        engagement.destroy()
        @hide()
