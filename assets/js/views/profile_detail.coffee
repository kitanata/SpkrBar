SpkrBar.Views.ProfileDetail = Backbone.View.extend
    template: "#profile-detail-templ"

    initialize: (options) ->
        @shouldRender = false

        @listenTo(@model.get('links'), "change add remove reset", @invalidate)
        @listenTo(@model.get('tags'), "change add remove reset", @invalidate)
        @listenTo(@model.get('followers'), "change add remove reset", @invalidate)
        @listenTo(@model.get('following'), "change add remove reset", @invalidate)

        @model.fetchRelated('links')
        @model.fetchRelated('tags')
        @model.fetchRelated('followers')
        @model.fetchRelated('following')

    render: ->
        console.log "Render"
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
        console.log "Invalidate"
        if not @shouldRender
            setTimeout =>
                @beforeRender()
                @render()
                @afterRender()
                @shouldRender = false
            , 500
            @shouldRender = true

    beforeRender: ->
        console.log @model

    afterRender: ->

    userOwnsContent: ->
        user != null and user.id == @model.id

    showTags: ->
        @model.get('tags').length != 0 or @userOwnsContent()

    showLinks: ->
        @model.get('links').length != 0 or @userOwnsContent()

    mapFollowUser: (follow) ->
        url: follow.get('url')
        name: follow.get('full_name')
        first_name: follow.get('first_name')
        photo: follow.get('photo')

    context: ->
        name: @model.get('full_name')
        about: @model.get('about_me')
        photo: @model.get('photo')
        showTags: @showTags()
        showLinks: @showLinks()
        tags: @model.get('tags').map (x) -> {'id': x.id, 'tag': x.get('name')}
        links: @model.get('links').map (x) -> {'id': x.id, 'name': x.get('name'), 'url': x.get('url')}
        numFollowing: @model.get('following').length
        numFollowers: @model.get('followers').length
        followers: @model.get('followers').map @mapFollowUser
        following: @model.get('following').map @mapFollowUser
        userOwnsContent: @userOwnsContent()
        
    oldconst: ->
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
                    newNote = new SpkrBar.Views.Notification
                        model: x
                    @noteViews.push newNote

                    $('#notifications').append(newNote.render().el)

                    if not x.get('dismissed')
                        newNote.show()

        $('#show-notifications').click =>
            if @showNotes
                _(@noteViews).each (view) ->
                    view.show()
            else
                _(@noteViews).each (view) ->
                    view.hide()

            @showNotes = !@showNotes
