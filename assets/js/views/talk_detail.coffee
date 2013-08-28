class SpkrBar.Views.TalkDetail
    constructor: (talk_id) ->
        @engagementViews = []

        @talkDetailModel = new SpkrBar.Models.Talk
            id: talk_id
        @talkDetailModel.fetch
            success: =>
                engagements = @talkDetailModel.get 'engagements'

                _(engagements).each (x) =>
                    engagementModel = new SpkrBar.Models.Engagement
                        id: x
                    engagementModel.fetch
                        success: =>
                            newView = new SpkrBar.Views.Engagement
                                model: engagementModel
                                talk: @talkDetailModel

                            $('#engagement-list-region').append newView.render().el
                            @engagementViews.push(newView)

                talkTags = new SpkrBar.Collections.TalkTags
                    talk_id: @talkDetailModel.id
                talkTags.fetch
                    success: =>
                        talkTagsView = new SpkrBar.Views.TalkTags
                            collection: talkTags
                            talk: @talkDetailModel

                        $('#talk-tags').append talkTagsView.render().el

                talkLinks = new SpkrBar.Collections.TalkLinks
                    talk_id: @talkDetailModel.id
                talkLinks.fetch
                    success: =>
                        talkLinksView = new SpkrBar.Views.TalkLinks
                            collection: talkLinks
                            talk: @talkDetailModel

                        $('#talk-links').append talkLinksView.render().el

                talkComments = new SpkrBar.Collections.TalkComments
                    talk_id: @talkDetailModel.id
                talkComments.fetch
                    success: =>
                        talkCommentsView = new SpkrBar.Views.TalkComments
                            collection: talkComments
                            talk: @talkDetailModel

                        $('#talk-comments').append talkCommentsView.render().el

        @handleSubmitTalk()

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

        events = new SpkrBar.Collections.Events()
        events.fetch
            success: =>
                $('#event-list').typeahead
                    source: events.map (x) ->
                        eventName = x.get('owner').name + ' ' + x.get('start_date')[0..3]
                        if x.get('name')
                            eventName += ' - ' + x.get('name')
                        eventName

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
                    attendees: []
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

                    error: (model, xhr, options) =>
