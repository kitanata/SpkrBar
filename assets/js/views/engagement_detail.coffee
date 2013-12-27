SpkrBar.Views.EngagementDetail = Backbone.View.extend
    className: "talk_event"
    template: "#engagement-detail-templ"

    events:
        "click .endorse-talk": "onClickEndorseTalk"

    initialize: (options) ->
        @model.fetchRelated 'talk', 
            success: =>
                @model.get('talk').fetchRelated('tags')
                @model.get('talk').fetchRelated('endorsements')

        @model.fetchRelated('speaker')
        @model.fetchRelated('location')

        @listenTo(@model, "change", @invalidate)
        @listenTo(@model.get('talk'), "change", @invalidate)
        @listenTo(@model.get('talk').get('tags'), "change", @invalidate)
        @listenTo(@model.get('talk').get('endorsements'), "add remove change reset", @invalidate)

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
        @delegateEvents()

    userLoggedIn: ->
        user != null

    userOwnsContent: ->
        speaker = @model.get('speaker')
        user != null and speaker != null and user.id == speaker.id

    mapTalkTags: ->
        @model.get('talk').get('tags').map (x) -> 
            return {name: x.get('name')}

    mapTalkAbstract: ->
        _.str.truncate(
            _.str.stripTags(
                markdown.toHTML(
                    @model.get('talk').get('abstract')
                )
            ), 300)

    context: ->
        id: @model.id
        name: _.str.truncate(@model.get('talk').get('name'), 38)
        event_name: @model.get('event_name')
        event_url: "/event/" + _.str.slugify(@model.get('event_name'))
        speaker_name: @model.get('speaker').getFullName()
        speaker_photo: @model.get('speaker').get('photo')
        abstract: @mapTalkAbstract()
        tags: @mapTalkTags()
        url: '/talk/' + @model.get('talk').id
        room: @model.get('room')
        date: moment(@model.get('date')).format('LL')
        time: moment(@model.get('time'), "HH:mm:ss").format('hh:mm A')
        location_name: @model.get('location').get('name')
        address: @model.get('location').get('address')
        city: @model.get('location').get('city')
        state: @model.get('location').get('state')
        zip_code: @model.get('location').get('zip_code')
        userEndorsed: @model.get('talk').userEndorsed()
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()

    onClickEndorseTalk: (el) ->
        newEndorsement = new SpkrBar.Models.TalkEndorsement
            talk: @model.get('talk')
            user: user
        newEndorsement.save null,
            success: =>
                @model.get('talk').get('endorsements').add newEndorsement
