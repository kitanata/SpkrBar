SpkrBar.Views.ProfileDetail = Backbone.View.extend
    template: "#profile-detail-templ"

    events:
        "click .profile-photo-upload": "onClickProfilePhotoUpload"
        "click #edit-profile": "onClickEditProfile"
        "click #add-profile-tag": "onClickAddProfileTag"
        "keypress #new-profile-tag-name": "onKeyAddProfileTag"
        "click .delete-profile-tag": "onClickDeleteProfileTag"

    initialize: (options) ->
        @shouldRender = false

        @listenTo(@model, "change", @invalidate)
        @listenTo(@model.get('links'), "change add remove reset", @invalidate)
        @listenTo(@model.get('tags'), "change add remove reset", @invalidate)
        @listenTo(@model.get('followers'), "change add remove reset", @invalidate)
        @listenTo(@model.get('following'), "change add remove reset", @invalidate)
        @listenTo(@model.get('talks'), "change add remove reset", @invalidate)
        @listenTo(@model.get('engagements'), "change add remove reset", @invalidate)

        @allTags = new SpkrBar.Collections.UserTags()
        @allTags.fetch()

        @model.fetchRelated('links')
        @model.fetchRelated('tags')
        @model.fetchRelated('followers')
        @model.fetchRelated('following')
        @model.fetchRelated('talks')
        @model.fetchRelated('engagements')

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

    showTalks: ->
        @model.get('talks').length != 0 or @userOwnsContent()

    mapFollowUser: (follow) ->
        url: follow.get('url')
        name: follow.get('full_name')
        first_name: _.str.words(follow.get('full_name'), ' ')[0]
        photo: follow.get('photo')

    mapEngagements: ->
        engs = @model.get('engagements').map (x) -> 
            'name': x.get('event_name')
            'url': _.str.slugify(x.get('event_name'))

        _.uniq engs, false, (x) -> x.name

    mapTalks: ->
        @model.get('talks').map (x) ->
            'name': x.get('name')
            'abstract': _.str.stripTags(markdown.toHTML(x.get('abstract')))
            'url': '/talk/' + x.get('id')
            'endorsed': x.userEndorsed()

    context: ->
        name: @model.getFullName()
        about: markdown.toHTML(@model.get('about_me'))
        photo: @model.get('photo')
        showTags: @showTags()
        showLinks: @showLinks()
        showTalks: @showTalks()
        tags: @model.get('tags').map (x) -> {'id': x.id, 'tag': x.get('name')}
        links: @model.get('links').map (x) -> {'id': x.id, 'name': x.get('name'), 'url': x.get('url')}
        talks: @mapTalks()
        engagements: @mapEngagements()
        numFollowing: @model.get('following').length
        numFollowers: @model.get('followers').length
        followers: @model.get('followers').map @mapFollowUser
        following: @model.get('following').map @mapFollowUser
        userOwnsContent: @userOwnsContent()

    onClickProfilePhotoUpload: ->
        console.log "Upload the photo"

    onClickEditProfile: ->
        editor = new SpkrBar.Views.ProfileEdit
            model: @model

        $.colorbox
            html: editor.render().el
            width: "700px"
            height: "520px"

    onKeyAddProfileTag: (el) ->
        if el.which == 13
            @onClickAddProfileTag(el)

            $('#new-profile-tag-name').val ''

    onClickAddProfileTag: ->
        tag_name = $('#new-profile-tag-name').val()

        tag = @allTags.find (x) => x.get('name') == name

        addTagToModel = (tag) =>
            @model.get('tags').add tag
            @model.save()

        if tag
            addTagToModel(tag)
        else
            newTag = new SpkrBar.Models.UserTag
                name: tag_name

            newTag.save null, 
                success: =>
                    addTagToModel(newTag)
                    @allTags.add newTag


    onClickDeleteProfileTag: (el) ->
        tagId = $(el.currentTarget).data('id')
        tag = @model.get('tags').find (x) => x.id == tagId
        @model.get('tags').remove tag
        @model.save()


    oldconst: ->
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
