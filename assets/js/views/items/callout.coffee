SpkrBar.Views.Items.Callout = Backbone.Marionette.ItemView.extend
    template: Handlebars.compile($("#callout-templ").html())

    serializeData: ->
        userIsAnonymous: if window.user then false else true