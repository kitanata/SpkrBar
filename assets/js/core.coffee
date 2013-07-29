$('a.btn').tooltip()

$('.expert-area li .delete-profile-tag').click (el) =>
    itemId = $(el.currentTarget).data('id')
    postTo = '/profile/edit/tag/' + itemId + '/delete/'

    $.post postTo, =>
        $('.expert-area li[data-id=' + itemId + ']').remove()


$('.expert-area li .delete-talk-tag').click (el) =>
    itemId = $(el.currentTarget).data('id')
    postTo = '/talk/tag/' + itemId + '/delete/'

    $.post postTo, =>
        $('.expert-area li[data-id=' + itemId + ']').remove()


$('.profile-link .delete-profile-link').click (el) =>
    itemId = $(el.currentTarget).data('id')
    postTo = '/profile/edit/link/' + itemId + '/delete/'

    $.post postTo, =>
        $('.profile-link[data-id=' + itemId + ']').remove()
