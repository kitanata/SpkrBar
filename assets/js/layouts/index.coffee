SpkrBar.Layouts.Index = Backbone.Marionette.Layout.extend
  template: Handlebars.compile($("#index-templ").html())

  regions:
    callout: "#callout"
    upcoming: "#upcoming"
    past: "#past"
