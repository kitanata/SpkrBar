class mainController
    talksHandler: ->
        spkrbar.showTalksView()

    mainHandler: ->
        spkrbar.showIndexView()

SpkrBar.Routers.Main = Backbone.Marionette.AppRouter.extend
    controller: new mainController()

    appRoutes:
        "talks": "talksHandler"
        "": "mainHandler"
