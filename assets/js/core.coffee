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

        @talksLayout = new SpkrBar.Layouts.Talks()
        @talksLayout.render()

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
            model: new Backbone.Model
                title: "Upcoming Speaking Engagements"
        @upcomingEngagementsView.render()

        @pastEngagementsView = new SpkrBar.Views.Collections.EngagementsSpan6
            collection: (new SpkrBar.Collections.Engagements past[0...4])
            model: new Backbone.Model
                title: "Recent Speaking Engagements"
        @pastEngagementsView.render()

        @app.mainRegion.show(@mainLayout)
        @mainLayout.content.show(@indexLayout)
        @indexLayout.callout.show(@calloutView)
        @indexLayout.upcoming.show(@upcomingEngagementsView)
        @indexLayout.past.show(@pastEngagementsView)

    showTalksView: ->
        now = new Date(Date.now()).getTime()

        groups = [
            ['-', 180, 90, "l6m"],
            ['-', 90, 30, "l3m"],
            ['-', 30, 0, "l30d"],
            ['+', 0, 30, "n30d"],
            ['+', 30, 90, "n3m"],
            ['+', 90, 180, "n6m"]]

        titles = 
            l6m: "Last 6 Months"
            l3m: "Last 3 Months"
            l30d: "Last 30 Days"
            n30d: "Next 30 Days"
            n3m: "Next 3 Months"
            n6m: "Next 6 Months"

        engagementGroups = @engagementCollection.groupBy (x) =>
            group = _(groups).find (y) ->
                if y[0] == '-'
                    startDate = now - (y[1] * 24 * 60 * 60 * 1000)
                    endDate = now - (y[2] * 24 * 60 * 60 * 1000)
                else
                    startDate = now + (y[1] * 24 * 60 * 60 * 1000)
                    endDate = now + (y[2] * 24 * 60 * 60 * 1000)

                start = (new Date(startDate)).toISOString()
                end = (new Date(endDate)).toISOString()
                test = x.get('date')

                if test > start and test < end
                    true
                else
                    false
            if group
                group[3]

        @app.mainRegion.show(@mainLayout)
        @mainLayout.content.show(@talksLayout)

        for group, engagements of engagementGroups
            if group != "undefined"
                view = new SpkrBar.Views.Collections.EngagementsSpan6
                    collection: (new SpkrBar.Collections.Engagements engagements)
                    model: new Backbone.Model
                        title: titles[group]
                view.render()
                @talksLayout[group].show(view)

window.spkrbar = new SpkrBarApp()