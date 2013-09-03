SpkrBar.Layouts.Talks = Backbone.Marionette.Layout.extend
  template: Handlebars.compile($("#talks-layout-templ").html())

  regions:
    l6m: "#l6m"
    l3m: "#l3m"
    l30d: "#l30d"
    n30d: "#n30d"
    n3m: "#n3m"
    n6m: "#n6m"
    subnav: "#subnav"
