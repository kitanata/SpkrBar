$('a.btn').tooltip()

$('.expert-area li .delete-profile-tag').click (el) =>
    itemId = $(el.currentTarget).data('id')
    postTo = '/profile/edit/tag/' + itemId + '/delete/'

    $.post postTo, =>
        $('.expert-area li[data-id=' + itemId + ']').remove()


$('.expert-area li .delete-talk-tag').click (el) =>
    itemId = $(el.currentTarget).data('id')
    talkId = $(el.currentTarget).data('talk')
    postTo = '/talk/' + talkId + '/tag/' + itemId + '/delete/'

    $.post postTo, =>
        $('.expert-area li[data-id=' + itemId + ']').remove()


$('.profile-link .delete-profile-link').click (el) =>
    itemId = $(el.currentTarget).data('id')
    postTo = '/profile/edit/link/' + itemId + '/delete/'

    $.post postTo, =>
        $('.profile-link[data-id=' + itemId + ']').remove()

$('.profile-link-form #id_type').change (el) =>
    type = $(el.currentTarget).val()

    if type in ['GITHUB', 'FACEBOOK', 'TWITTER']
        $('.profile-link-form #id_url').attr('placeholder', 'URL or Username')
    else
        $('.profile-link-form #id_url').attr('placeholder', 'http://')

$('.talk-link .delete-talk-link').click (el) =>
    itemId = $(el.currentTarget).data('id')
    talkId = $(el.currentTarget).data('talk')
    postTo = '/talk/' + talkId + '/link/' + itemId + '/delete/'

    $.post postTo, =>
        $('.talk-link[data-id=' + itemId + ']').remove()
