class mainController
    talksHandler: ->
        console.log "talks"

    mainHandler: ->
        console.log "main"

SpkrBar.Routers.Main = Backbone.Marionette.AppRouter.extend
    controller: new mainController()

    appRoutes:
        "talks": "talksHandler"
        "": "mainHandler"
