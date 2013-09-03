$('a.btn').tooltip()

window.app = new Backbone.Marionette.Application()

app.addInitializer (options) =>
    new SpkrBar.Routers.Main()
    Backbone.history.start
        pushState: true

app.addRegions
    mainRegion: "#main"

mainLayout = new SpkrBar.Layouts.Main()
mainLayout.render()

indexLayout = new SpkrBar.Layouts.Index()
indexLayout.render()

calloutView = new SpkrBar.Views.Callout()
calloutView.render()

app.mainRegion.show(mainLayout)
mainLayout.content.show(indexLayout)
indexLayout.callout.show(calloutView)

app.start()
