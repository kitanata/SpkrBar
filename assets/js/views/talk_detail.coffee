SpkrBar.Views.TalkDetail = Backbone.View.extend
    template: "#talk-detail-templ"

    events:
        "click .add-talk-tag": 'onAddTalkTag'
        "click .delete-talk-tag": 'onDeleteTalkTag'
        "click .add-talk-link": 'onAddTalkLink'
        "click .delete-talk-link": 'onDeleteTalkLink'
        "click #add-slides": "onClickAddSlides"
        "click #add-videos": "onClickAddVideos"
        "click #add-photos": "onClickAddPhotos"
        "click #edit-talk": "onClickEditTalk"
        "click #delete-talk": "onClickDeleteTalk"
        "click #create-engagement": "onClickCreateEngagement"
        "click .publish-talk": "onClickPublishTalk"
        "click .delete-slide": "onClickDeleteSlide"
        "click .delete-video": "onClickDeleteVideo"

    initialize: (options) ->
        @engagementViews = []

        @allTags = new SpkrBar.Collections.TalkTags()
        @tags = new Backbone.Collection()
        @links = new Backbone.Collection()
        @slides = new Backbone.Collection()
        @videos = new Backbone.Collection()

        @listenTo(@tags, "change add remove reset", @render)
        @listenTo(@links, "change add remove", @render)
        @listenTo(@slides, "change add remove", @render)
        @listenTo(@videos, "change add remove", @render)
        @listenTo(@model, "change", @render)

        @fetchTalkTags => 
            @fetchTalkDetailModel => 
                @handleSubmitTalk()

    fetchTalkTags: (next) ->
        @allTags.fetch
            success: => 
                next()

    fetchTalkDetailModel: (next) ->
        engagements = @model.get 'engagements'
        links = @model.get 'links'
        slides = @model.get 'slides'
        videos = @model.get 'videos'

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
        @tags.reset(@allTags.filter (x) => x.id in tagIds)

        _(links).each (x) =>
            linkModel = new SpkrBar.Models.TalkLink
                id: x
            linkModel.fetch
                success: =>
                    @links.push linkModel

        _(slides).each (x) =>
            slideModel = new SpkrBar.Models.TalkSlideDeck
                id: x
            slideModel.fetch
                success: =>
                    @slides.push slideModel

        _(videos).each (x) =>
            videoModel = new SpkrBar.Models.TalkVideo
                id: x
            videoModel.fetch
                success: =>
                    @videos.push videoModel

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
        user.id == @model.get('speaker').id

    userEndorsed: ->
        user.id in @model.get('endorsements')

    userRated: ->
        user.id in @model.get('ratings')

    showTags: ->
        @tags.length != 0 or @userOwnsContent()

    showLinks: ->
        @links.length != 0 or @userOwnsContent()

    context: ->
        userLoggedIn: @userLoggedIn()
        userOwnsContent: @userOwnsContent()
        userEndorsed: @userEndorsed()
        numEndorsements: @model.get('endorsements').length
        published: @model.get('published')
        speakerName: @model.get('speaker').full_name
        speakerUrl: @model.get('speaker').url
        name: @model.get('name')
        abstract: @model.get('abstract')
        photo: @model.get('speaker').photo
        slides: @slides.map (x) -> {'id': x.id, 'embed_code': x.get('embed_code')}
        videos: @videos.map (x) -> {'id': x.id, 'embed_code': x.get('embed_code')}
        comments: @model.get('comments')
        showTags: @showTags()
        showLinks: @showLinks()
        tags: @tags.map (x) -> {'id': x.id, 'tag': x.get('name')}
        links: @links.map (x) -> {'id': x.id, 'name': x.get('name'), 'url': x.get('url')}

    onAddTalkTag: ->
        name = $('#new-talk-tag-name').val()

        tag = @allTags.find (x) => x.get('name') == name

        addTagToModel = (tag) =>
            tags = @model.get('tags')
            tags.push tag.id
            @tags.add tag
            @model.set 'tags', tags
            @model.save()

        if tag
            addTagToModel(tag)
        else
            newTags = new SpkrBar.Models.TalkTag
                name: name

            newTag.save null, 
                success: =>
                    addTagToModel(newTag)
                    @allTags.add newTag

    onDeleteTalkTag: (el) ->
        tagId = $(el.currentTarget).data('id')
        tags = _(@model.get('tags')).reject (x) => x == tagId
        @model.set 'tags', tags
        @model.save()

        deadTag = @tags.find (x) => x.id == tagId
        @tags.remove(deadTag)

    onAddTalkLink: ->
        name = $('#new-talk-link-name').val()
        url = $('#new-talk-link-url').val()

        newLink = new SpkrBar.Models.TalkLink
            talk: @model.id
            name: name
            url: url
        newLink.save null, 
            success: =>
                links = @model.get 'links'
                links.push newLink.id
                @model.set 'links', links
                @model.save()
                @links.add newLink

    onDeleteTalkLink: (el) ->
        linkId = $(el.currentTarget).data('id')
        deadLink = @links.find (x) => x.id == linkId

        deadLink.destroy
            success: =>
                @links.remove deadLink
                links = _(@model.get 'links').reject (x) -> x == linkId
                @model.set 'links', links
                @model.save()

    onClickAddSlides: ->
        $.colorbox
            html: $('#link-slides-popup').clone()
            width: "400px"

    onClickDeleteSlide: (el) ->
        slideId = $(el.currentTarget).data('id')

        slide = @slides.find (x) => x.id == slideId
        @slides.remove slide
        slide.destroy()

    onClickAddVideos: ->
        $.colorbox
            html: $('#link-video-popup').clone()
            width: "400px"

    onClickDeleteVideo: (el) ->
        vidId = $(el.currentTarget).data('id')

        video = @videos.find (x) => x.id == vidId
        @videos.remove video
        video.destroy()

    onClickAddPhotos: ->
        $.colorbox
            html: $('#upload-photo-popup').clone()
            width: "400px"

    onClickEditTalk: ->
        $.colorbox
            html: $('#edit-talk-popup').clone()
            width: "400px"

    onClickDeleteTalk: ->
        $.colorbox
            html: $('#delete-talk-popup').clone()
            width: "400px"

    onClickPublishTalk: ->
        @model.set 'published', !(@model.get 'published')
        @model.save()

    onClickCreateEngagement: ->
        createEngagementView = new SpkrBar.Views.CreateEngagement
            talk: @model

        $.colorbox
            html: createEngagementView.render().el
            width: "514px"
