SpkrBar.Views.ProfileDetail = Backbone.View.extend
    template: "#profile-detail-templ"

    events:
        "click #edit-profile": "onClickEditProfile"
        "click #add-profile-tag": "onClickAddProfileTag"
        "click .profile-photo-upload": "onClickUploadPhoto"
        "change .profile-photo-upload-file": "onChangePhotoUploadFile"
        "keypress #new-profile-tag-name": "onKeyAddProfileTag"
        "click .delete-profile-tag": "onClickDeleteProfileTag"
        "keypress #new-profile-link-url": "onKeyAddProfileLink"
        "change #new-profile-link-type": "onChangeProfileLinkType"
        "click .add-talk": "onClickAddTalk"
        "click .add-profile-link": "onClickAddProfileLink"
        "click .delete-profile-link": "onClickDeleteProfileLink"
        "click .follow-user": "onClickFollowUser"
        "click .unfollow-user": "onClickUnfollowUser"

    initialize: (options) ->
        @shouldRender = false

        @listenTo(@model, "change", @invalidate)
        @listenTo(@model.get('links'), "change add remove reset", @invalidate)
        @listenTo(@model.get('tags'), "change add remove reset", @invalidate)
        @listenTo(@model.get('followers'), "change add remove reset", @invalidate)
        @listenTo(@model.get('following'), "change add remove reset", @invalidate)
        @listenTo(@model.get('talks'), "add remove reset", @buildTalkViews)
        @listenTo(@model.get('engagements'), "change add remove reset", @invalidate)

        @allTags = new SpkrBar.Collections.UserTags()
        @allTags.fetch()

        @model.fetchRelated('links')
        @model.fetchRelated('tags')

        @model.fetchRelated 'followers',
            success: (x) =>
                x.fetchRelated 'user',
                    success: =>
                        @invalidate()

        @model.fetchRelated 'following',
            success: (x) =>
                x.fetchRelated 'following',
                    success: =>
                        @invalidate()

        @model.fetchRelated('engagements')

        @model.fetchRelated 'talks', 
            success: =>
                @model.get('talks').trigger('add')

        @talkViews = []

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    invalidate: ->
        if not @shouldRender
            setTimeout =>
                @beforeRender()
                @render()
                @afterRender()
                @shouldRender = false
            , 500
            @shouldRender = true

    beforeRender: ->

    afterRender: ->
        _(@talkViews).each (talkView) =>
            $('.talk-list').append talkView.render().el

        addthis.toolbox('.addthis_toolbox')

    buildTalkViews: ->
        @talkViews = []
        $('.talk-list').html('')

        @model.get('talks').each (x) =>
            newView = new SpkrBar.Views.ProfileTalk
                model: x
            @talkViews.push(newView)
        @invalidate()

    userOwnsContent: ->
        user != null and user.id == @model.id

    showTags: ->
        @model.get('tags').length != 0 or @userOwnsContent()

    showLinks: ->
        @model.get('links').length != 0 or @userOwnsContent()

    hasTalks: ->
        @model.get('talks').length != 0

    showTalks: ->
        @hasTalks() or @userOwnsContent()

    mapFollowingUser: (follow) ->
        if follow.get('user') != null
            url: follow.get('user').get('url')
            name: follow.get('user').get('full_name')
            first_name: _.str.words(follow.get('user').get('full_name'), ' ')[0]
            photo: follow.get('user').get('photo')
        else
            url: ""
            name: ""
            first_name: ""
            photo: ""

    mapFollowedUser: (follow) ->
        if follow.get('following') != null
            url: follow.get('following').get('url')
            name: follow.get('following').get('full_name')
            first_name: _.str.words(follow.get('following').get('full_name'), ' ')[0]
            photo: follow.get('following').get('photo')
        else
            url: ""
            name: ""
            first_name: ""
            photo: ""

    mapEngagements: ->
        engs = @model.get('engagements').map (x) -> 
            'name': x.get('event_name')
            'url': _.str.slugify(x.get('event_name'))

        _.uniq engs, false, (x) -> x.name

    mapLinks: ->
        typemap =
            "FAC": "My Facebook Profile"
            "TWI": "My Twitter Stream"
            "LIN": "My LinkedIn Profile"
            "LAN": "My Lanyrd Page"
            "GIT": "My Github Contributions"
            "BLO": "My Blog"
        
        @model.get('links').map (x) ->
            type = x.get('type_name')

            if type == 'WEB'
                return {
                    'id': x.id,
                    'name': x.get('other_name'),
                    'url': x.get('url_target')
                }
            else
                return {
                    'id': x.id,
                    'name': typemap[type],
                    'url': x.get('url_target')
                }

    userLoggedIn: ->
        user != null

    context: ->
        name: @model.get('full_name')
        about: markdown.toHTML(@model.get('about_me'))
        photo: @model.get('photo')
        showTags: @showTags()
        showLinks: @showLinks()
        showTalks: @showTalks()
        hasTalks: @hasTalks()
        tags: @model.get('tags').map (x) -> {'id': x.id, 'tag': x.get('name')}
        links: @mapLinks()
        csrf: csrftoken
        engagements: @mapEngagements()
        numFollowing: @model.get('following').length
        numFollowers: @model.get('followers').length
        followers: @model.get('followers').map @mapFollowingUser
        following: @model.get('following').map @mapFollowedUser
        userOwnsContent: @userOwnsContent()
        followedByUser: @model.userFollowingMe()
        userLoggedIn: @userLoggedIn()

    onClickEditProfile: ->
        editor = new SpkrBar.Views.ProfileEdit
            model: @model

        $.colorbox
            html: editor.render().el
            width: "700px"
            height: "520px"

    onClickAddTalk: ->
        $('#add-talk-navbar').click()

    onClickUploadPhoto: (ev) ->
        $('.profile-photo-upload-file').val ""
        $('.profile-photo-upload-file').click()

        ev.preventDefault()

    onChangePhotoUploadFile: (ev) ->
        filename = $('.profile-photo-upload-file').val()

        if filename
            $('.submit-photo-upload').click()
            
        ev.preventDefault()

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
            "FAC": "facebook.com/"
            "GIT": "github.com/"
            "TWI": "twitter.com/"

        parseShittyUrl = (text) ->
            if text[0..6] == 'http://'
                text = text[7..]

            if text[0..2] == 'www'
                text = text[4..]

            if text[0] == '.'
                text = text[1..]

            "http://www." + text

        if linkType in ["FAC", "GIT", "TWI"]
            if urlTarget[0] == '@'
                urlTarget = urlTarget[1..]
                link.set 'url_target', "http://www." + url_map[linkType] + urlTarget
            else if urlTarget[0..6] != 'http://'
                link.set 'url_target', "http://www." + url_map[linkType] + urlTarget
            else
                link.set 'url_target', parseShittyUrl(urlTarget)
        else
            link.set 'url_target', parseShittyUrl(urlTarget)

        link.save null,
            success: =>
                @model.get('links').add link
                @model.save()


    onClickDeleteProfileLink: (el) ->
        linkId = $(el.currentTarget).data('id')
        link = @model.get('links').find (x) => x.id == linkId
        @model.get('links').remove link
        link.destroy()
        @model.save()

    onClickFollowUser: ->
        following = new SpkrBar.Models.UserFollowing
            user: user
            following: @model
        following.save null,
            success: =>
                @model.get('followers').add following
        @invalidate()

    onClickUnfollowUser: ->
        following = @model.get('followers').find (x) => 
            x.get('user').id == user.id
        @model.get('followers').remove following

        following.destroy()
        @invalidate()
