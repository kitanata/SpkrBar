SpkrBar.Views.ProfileDetail = Backbone.View.extend
    template: "#profile-detail-templ"

    events:
        "click .profile-photo-upload": "onClickProfilePhotoUpload"
        "click #edit-profile": "onClickEditProfile"
        "click #add-profile-tag": "onClickAddProfileTag"
        "keypress #new-profile-tag-name": "onKeyAddProfileTag"
        "click .delete-profile-tag": "onClickDeleteProfileTag"
        "keypress #new-profile-link-url": "onKeyAddProfileLink"
        "change #new-profile-link-type": "onChangeProfileLinkType"
        "click .add-profile-link": "onClickAddProfileLink"
        "click .delete-profile-link": "onClickDeleteProfileLink"

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


    onChangeProfileLinkType: (el) ->
        linkType = $("#new-profile-link-type").val()

        $("#new-profile-link-other").hide()

        if linkType == "WEB"
            $("#new-profile-link-other").show()

        if linkType in ["WEB", "LIN", "LAN", "BLO"]
            $("#new-profile-link-url").attr 'placeholder', 'http://'
        else
            $("#new-profile-link-url").attr 'placeholder', 'username or http://'


    onKeyAddProfileLink: (el) ->
        if el.which == 13
            @onClickAddProfileLink(el)


    onClickAddProfileLink: (el) ->
        linkType = $("#new-profile-link-type").val()
        urlTarget = $("#new-profile-link-url").val()

        link = new SpkrBar.Models.UserLink
            user: user
            type_name: linkType

        if linkType == "WEB"
            link.set 'other_name', $("#new-profile-link-other").val()
            link.set 'urlTarget', urlTarget

        url_map = 
            "FAC": "facebook"
            "GIT": "github"
            "TWI": "twitter"

        parseShittyUrl = (text) ->
            if text[0..6] == 'http://'
                text = text[7..]

            if text[0..3] == 'www'
                text = text[4..]

            if text[0] == '.'
                text = text[1..]

            "http://www." + text

        if linkType in ["FAC", "GIT", "TWI"]
            text = urlTarget

            if text[0] == '@'
                text = text[1..]
                link.set 'url_target', "http://www." + url_map[linkType] + "/" + text
            else
                link.set 'url_target', parseShittyUrl(text)
        else
            link.set 'url_target', parseShittyUrl(text)

        link.save()
        @model.get('links').add link
        @model.save()


    onClickDeleteProfileLink: (el) ->
        linkId = $(el.currentTarget).data('id')
        link = @model.get('links').find (x) => x.id == linkId
        @model.get('links').remove link
        link.destroy()
        @model.save()


    oldconst: ->
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
