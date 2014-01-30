SpkrBar.Views.EventManagerPage = Backbone.View.extend
    template: "#event-manager-templ"
    className: "event-manager"

    events:
        "click .item": "onClickEventUploadItem"
        "click .create": "onClickCreateEventUpload"
        "click .to-upload": "onClickToUpload"
        "click .start-upload": "onClickStartUpload"
        "click .confirm-upload": "onClickConfirmUpload"
        "click .confirm-billing": "onClickConfirmBilling"

    initialize: (options) ->
        @shouldRender = false

        @talkViews = []

        @createEventImportTemplate = Handlebars.compile($("#create-event-import-templ").html())
        @downloadTemplateTemplate = Handlebars.compile($("#download-template-templ").html())
        @uploadTemplateTemplate = Handlebars.compile($("#upload-template-templ").html())
        @uploadingTemplate = Handlebars.compile($("#uploading-templ").html())
        @validationFailedTemplate = Handlebars.compile($("#validation-failed-templ").html())
        @uploadPreviewTemplate = Handlebars.compile($("#upload-preview-templ").html())
        @confirmBillingTemplate = Handlebars.compile($("#confirm-billing-templ").html())
        @importStartedTemplate = Handlebars.compile($("#import-started-templ").html())
        @importFinishedTemplate = Handlebars.compile($("#import-finished-templ").html())

        @invalidate()

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    onClickEventUploadItem: ->
        @$el.find('.dashboard').html @createEventImportTemplate({})

    onClickCreateEventUpload: ->
        @$el.find('.dashboard').html @downloadTemplateTemplate({})

    onClickToUpload: ->
        @$el.find('.dashboard').html @uploadTemplateTemplate({})

    onClickStartUpload: ->
        @$el.find('.dashboard').html @uploadPreviewTemplate({})

    onClickConfirmUpload: ->
        @$el.find('.dashboard').html @confirmBillingTemplate({})

    onClickConfirmBilling: ->
        @$el.find('.dashboard').html @importFinishedTemplate({})

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
        $('.talk-list').html ""

        _(@talkViews).each (view) =>
            $('.talk-list').append view.render().el

    userLoggedIn: ->
        user != null

    context: ->
        {}

    onClickInviteRegister: ->
        console.log "Invite Register"

    onClickYearlyRegister: ->
        console.log "Yearly Register"

    onClickForeverRegister: ->
        console.log "Forever Register"

    onClickSpeakerRegister: ->
        regModel = new SpkrBar.Models.Register()

        editor = new SpkrBar.Views.RegisterUser
            model: regModel

        $.colorbox
            html: editor.render().el
            width: "500px"
            height: "440px"
