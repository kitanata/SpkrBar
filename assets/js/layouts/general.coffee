SpkrBar.Layouts.General = Backbone.Marionette.Layout.extend
  template: Handlebars.compile($("#general-layout-templ").html())

  regions:
    content: "#content"
    subnav: "#subnav"
