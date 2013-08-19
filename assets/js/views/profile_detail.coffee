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

        notifications = new SpkrBar.Collections.Notifications
            user_id: user.id
        notifications.fetch
            success: =>
                notifications.each (x) ->
                    if not x.get('dismissed')
                        newNote = $.pnotify
                            title: x.get('title')
                            text: x.get('message')
                            hide: false
                            closer_hover: false
                            sticker: false
                            icon: false
                            after_close: (el) =>
                                x.set 'dismissed', true
                                x.save()

                        $('#notifications').append(newNote)
