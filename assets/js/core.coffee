class SpkrBarApp

    constructor: ->
        if userId
          @user = new SpkrBar.Models.User
            id: userId
          @user.fetch()
        else
          @user = null

        @app = new Backbone.Marionette.Application()

        @app.addInitializer (options) =>
            new SpkrBar.Routers.Main()
            Backbone.history.start
                pushState: true

        @app.addRegions
            mainRegion: "#main"

        @bootstrapApp =>
            console.log "Starting Marionette"
            @app.start()

    bootstrapApp: (next) ->
        console.log "BootstrapApp"
        @engagementCollection = new SpkrBar.Collections.Engagements()
        @engagementCollection.fetch
            success: =>
                @buildViews()
                next()

    buildViews: ->
        console.log "BuildViews"
        @mainLayout = new SpkrBar.Layouts.Main()
        @mainLayout.render()

        @indexLayout = new SpkrBar.Layouts.Index()
        @indexLayout.render()

        @generalLayout = new SpkrBar.Layouts.General()
        @generalLayout.render()

        @calloutView = new SpkrBar.Views.Items.Callout()
        @calloutView.render()

        @showIndexView()

    showIndexView: ->
        now = (new Date(Date.now())).toISOString()

        upcoming = @engagementCollection.filter (x) => 
            now < x.get('date')
        upcoming = _(upcoming).sortBy (x) ->
            x.get('date')

        past = @engagementCollection.filter (x) ->
            now > x.get('date')
        past = _(past).sortBy (x) ->
            x.get('date')
        past.reverse()

        @upcomingEngagementsView = new SpkrBar.Views.Collections.EngagementsSpan6
            collection: (new SpkrBar.Collections.Engagements upcoming[0...4])
        @upcomingEngagementsView.render()

        @pastEngagementsView = new SpkrBar.Views.Collections.EngagementsSpan6
            collection: (new SpkrBar.Collections.Engagements past[0...4])
        @pastEngagementsView.render()

        @app.mainRegion.show(@mainLayout)
        @mainLayout.content.show(@indexLayout)
        @indexLayout.callout.show(@calloutView)
        @indexLayout.upcoming.show(@upcomingEngagementsView)
        @indexLayout.past.show(@pastEngagementsView)


window.spkrbar = new SpkrBarApp()