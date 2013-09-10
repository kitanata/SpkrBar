SpkrBar.Views.TalkDetail = Backbone.View.extend
    template: "#talk-detail-templ"

    initialize: (options) ->
        @engagementViews = []

        @talkTags = new SpkrBar.Collections.TalkTags()

        @fetchTalkTags => 
            @fetchTalkDetailModel => 
                @handleSubmitTalk()

    fetchTalkTags: (next) ->
        @talkTags.fetch
            success: => 
                next()

    fetchTalkDetailModel: (next) ->
        engagements = @model.get 'engagements'

        _(engagements).each (x) =>
            engagementModel = new SpkrBar.Models.Engagement
                id: x
            engagementModel.fetch
                success: =>
                    newView = new SpkrBar.Views.Engagement
                        model: engagementModel
                        talk: @model

                    $('#engagement-list-region').append newView.render().el
                    @engagementViews.push(newView)

        tagIds = @model.get('tags')
        tags = new Backbone.Collection(@talkTags.filter (x) => x.id in tagIds)

        talkTagsView = new SpkrBar.Views.TalkTags
            collection: tags
            talk: @model

        $('#talk-tags').append talkTagsView.render().el

        talkLinks = new SpkrBar.Collections.TalkLinks
            talk_id: @model.id
        talkLinks.fetch
            success: =>
                talkLinksView = new SpkrBar.Views.TalkLinks
                    collection: talkLinks
                    talk: @model

                $('#talk-links').append talkLinksView.render().el

        next()

    handleSubmitTalk: () ->
        $('.submit-talk').colorbox({inline: true, width:"400px"})

        nowTemp = new Date()
        now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0)

        $('#date').datepicker
            format: 'mm/dd/yyyy'

        $('#date').datepicker 'update', now

        $('#date').on 'changeDate', () ->
            $('#date').datepicker('hide')

        $('#time').timepicker
            template: false,
            showInputs: false,
            minuteStep: 5

        $('#submit-engagement').on 'click', =>
            eventName = $('#event-list').val()
            talkId = $('#talk-id').val()
            date = $('#date').val()
            time = $('#time').val()

            hours = parseInt(time[0..1])
            minutes = time[3..4]
            meridian = time[6..7]

            if meridian == "PM"
                hours += 12

            date = new Date(date[6..9], date[3..4], date[0..1], hours, minutes)

            selEvent = events.find (x) ->
                checkName = x.get('owner').name + ' ' + x.get('start_date')[0..3]
                if x.get('name')
                    checkName += ' - ' + x.get('name')
                eventName == checkName

            if selEvent
                newEngagement = new SpkrBar.Models.Engagement
                    talk: talkId
                    event: selEvent.id
                    date: date
                    from_speaker: true
                    vetoed: false

                window.engage = newEngagement

                newEngagement.save null,
                    success: =>
                        $.colorbox.close()

                        newView = new SpkrBar.Views.Engagement
                            model: newEngagement
                            talk: @talkDetailModel

                        $('#engagement-list-region').append newView.render().el
                        @engagementViews.push(newView)

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    userLoggedIn: ->
        user.id != 0

    userOwnsContent: ->
        user.id == @model.get('user')

    userEndorsed: ->
        user.id in @model.get('endorsements')

    userRated: ->
        user.id in @model.get('ratings')

    context: ->
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()
        userEndorsed: @userEndorsed()
        numEndorsements: @model.get('endorsements').length
        published: @model.get('published')
        speaker: @model.get('speaker')
        speakerUrl: @model.get('speaker_url')
        name: @model.get('name')
        abstract: @model.get('abstract')
        photo: @model.get('photo')
        slides: @model.get('slides')
        videos: @model.get('videos')
        photos: @model.get('photos')
        comments: @model.get('comments')
