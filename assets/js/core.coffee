$('a.btn').tooltip()

$('.expert-area li .delete-tag').click (el) =>
    itemId = $(el.currentTarget).data('id')
    postTo = '/profile/edit/tag/' + itemId + '/delete/'

    $.post postTo, =>
        $('.expert-area li[data-id=' + itemId + ']').remove()
