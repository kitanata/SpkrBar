class SpkrBar.Views.ProfileDetail
    constructor: () ->
        $('.expert-area li .delete-profile-tag').click (el) =>
            itemId = $(el.currentTarget).data('id')
            postTo = '/profile/edit/tag/' + itemId + '/delete'

            $.post postTo, =>
                $('.expert-area li[data-id=' + itemId + ']').remove()

        $('.expert-area li .delete-profile-tag').click (el) =>
            itemId = $(el.currentTarget).data('id')
            postTo = '/profile/edit/tag/' + itemId + '/delete'

            $.post postTo, =>
                $('.expert-area li[data-id=' + itemId + ']').remove()


        $('.profile-link .delete-profile-link').click (el) =>
            itemId = $(el.currentTarget).data('id')
            postTo = '/profile/edit/link/' + itemId + '/delete'

            $.post postTo, =>
                $('.profile-link[data-id=' + itemId + ']').remove()

        $('.profile-link-form #id_type').change (el) =>
            type = $(el.currentTarget).val()

            if type in ['GITHUB', 'FACEBOOK', 'TWITTER']
                $('.profile-link-form #id_url').attr('placeholder', 'URL or Username')
            else
                $('.profile-link-form #id_url').attr('placeholder', 'http://')


        @noteViews = []
        @showNotes = true

        @notifications = new SpkrBar.Collections.Notifications
            user_id: user.id
        @notifications.fetch
            success: =>
                @notifications.each (x) =>
                    if not x.get('dismissed')
                        newNote = @createNotificationView(x)
                        $('#notifications').append(newNote)
                        @noteViews.push x

        $('#show-notifications').click =>
            if @showNotes
                @notifications.each (x) =>
                    if not _(@noteViews).contains(x)
                        newNote = @createNotificationView(x)
                        $('#notifications').append(newNote)
                        @noteViews.push x
            else
                $.pnotify_remove_all()
                @noteViews = []

            @showNotes = !@showNotes

    bindEngagementNotificationEvents: ->
        $('#confirm-engagement').click (el) =>
            id = $(el.currentTarget).data('id')
            console.log $(el.currentTarget).parent().parent()
            engagement = new SpkrBar.Models.Engagement
                id: id
            engagement.fetch()
            engagement.confirmed = true
            engagement.save()

        $('#decline-engagement').click (el) =>
            id = $(el.currentTarget).data('id')
            engagement = new SpkrBar.Models.Engagement
                id: id
            engagement.destroy()

    createNotificationView: (note) ->
        $.pnotify
            title: note.get('title')
            text: note.get('message')
            hide: false
            closer_hover: false
            sticker: false
            icon: false
            after_close: (el) =>
                note.set 'dismissed', true
                note.save()
            after_open: =>
                @bindEngagementNotificationEvents()
