class SpkrBar.Views.TalkDetail
    constructor: () ->
        $('.expert-area li .delete-talk-tag').click (el) =>
            itemId = $(el.currentTarget).data('id')
            talkId = $(el.currentTarget).data('talk')
            postTo = '/talk/' + talkId + '/tag/' + itemId + '/delete/'

            $.post postTo, =>
                $('.expert-area li[data-id=' + itemId + ']').remove()

        $('.talk-link .delete-talk-link').click (el) =>
            itemId = $(el.currentTarget).data('id')
            talkId = $(el.currentTarget).data('talk')
            postTo = '/talk/' + talkId + '/link/' + itemId + '/delete/'

            $.post postTo, =>
                $('.talk-link[data-id=' + itemId + ']').remove()

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

        events = []

        #- for event in events
        #    name = "{{event}}"
        #    events.push(name)

        $('#event-list').typeahead
            source: events
