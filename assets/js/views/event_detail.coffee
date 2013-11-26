SpkrBar.Views.EventDetail = Backbone.View.extend
    template: "#event-detail-templ"

    initialize: (options) ->
        @shouldRender = false

        @engagementViews = []

        @model.fetchRelated 'engagements',
            success: (engagement) =>
                newView = new SpkrBar.Views.EngagementDetail
                    model: engagement
                @engagementViews.push(newView)
                @invalidate()

        @listenTo(@model, "change", @invalidate)

    render: ->
        console.log "Render"
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
        console.log "Invalidate"
        if not @shouldRender
            setTimeout =>
                @beforeRender()
                @render()
                @afterRender()
                @shouldRender = false
            , 500
            @shouldRender = true

    beforeRender: ->

    afterRender: ->
        console.log "AfterRender"

        _(@engagementViews).each (enView) =>
            year = moment(enView.model.get('date')).year()
            $('.talk-list-' + year).html("")

        _(@engagementViews).each (enView) =>
            year = moment(enView.model.get('date')).year()
            $('.talk-list-' + year).append enView.render().el

        L.Icon.Default.imagePath = '/static/img/'

        map = L.map('map').setView [39.95, -82.95], 6

        layer = L.tileLayer 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'

        layer.addTo map

        url = "http://nominatim.openstreetmap.org/search/{{city_querystring}}?format=json"
        $.get url, (data) =>
            if data.length != 0
                map.setView [data[0].lat, data[0].lon], 12

                url = "http://nominatim.openstreetmap.org/search/{{querystring}}?format=json"
                $.get url, (data) =>
                    if data.length != 0
                        marker = L.marker [data[0].lat, data[0].lon]
                        marker.addTo map
                        marker.bindPopup '<h4>{{event.location.name}}</h4><br />{{event.location.address}}<br />{{event.location.city}}, {{event.location.state}} {{event.location.zip_code}}'
                        marker.openPopup()

    userLoggedIn: ->
        user != null

    userOwnsContent: ->
        user != null and user.id == @model.get('speaker').id

    mapEngagements: ->
        years = @model.get('engagements').groupBy (x) ->
            moment(x.get('date')).year()
        _(_(years).keys()).map (x) =>
            name: @model.get('name') + ' - ' + x
            year: x

    context: ->
        id: @model.id
        name: @model.get('name')
        num_speakers: @model.get('num_speakers')
        num_engagements: @model.get('num_engagements')
        tags: _(@model.get('tags')).map (x) -> {count: x[0], name: x[1]}
        engagements: @mapEngagements()
