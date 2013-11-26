SpkrBar.Views.EventDetail = Backbone.View.extend
    template: "#event-detail-templ"

    initialize: (options) ->
        @shouldRender = false

        @engagementViews = []
        @speakerViews = []

        @model.fetchRelated 'engagements',
            success: (engagement) =>
                newView = new SpkrBar.Views.EngagementDetail
                    model: engagement
                @engagementViews.push(newView)
                @invalidate()

        @model.fetchRelated 'speakers',
            success: (speaker) =>
                newView = new SpkrBar.Views.Speaker
                    model: speaker
                @speakerViews.push(newView)
                @invalidate()

        @listenTo(@model, "change", @invalidate)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
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
        _(@engagementViews).each (enView) =>
            year = moment(enView.model.get('date')).year()
            $('.talk-list-' + year).html("")

        _(@engagementViews).each (enView) =>
            year = moment(enView.model.get('date')).year()
            $('.talk-list-' + year).append enView.render().el

        $('.speaker-list').html ""
        _(@speakerViews).each (spView) =>
            $('.speaker-list').append spView.render().el

        L.Icon.Default.imagePath = '/static/img/'

        map = L.map('map').setView [39.95, -96.95], 4

        layer = L.tileLayer 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'

        layer.addTo map

        locations = []
        @model.get('engagements').each (x) ->
            locations.push x.get('location')

        locations = _.uniq(locations)

        _(locations).each (location) ->
            if location == null
                return

            addr = location.get('address').replace(' ', '+')
            city = location.get('city')
            state = location.get('state')

            query = _.str.join(',', addr, city, state)

            url = "http://nominatim.openstreetmap.org/search?q=" + query + "&format=json"

            $.get url, (data) =>
                if data.length != 0
                    location.set('lat', data[0].lat)
                    location.set('lon', data[0].lon)
                    popUp = _.str.join(' ', 
                        '<h4>', location.get('name'),
                        '</h4><br />', addr, 
                        '<br />', city, ',', state, location.get('zip_code')
                        )
                    marker = L.marker [data[0].lat, data[0].lon]
                    marker.addTo map
                    marker.bindPopup popUp

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
