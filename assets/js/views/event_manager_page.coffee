SpkrBar.Views.EventManagerPage = Backbone.View.extend
    template: "#event-manager-templ"
    className: "event-manager"

    events:
        "click .new-import": "onClickNewImport"
        "click .item": "onClickEventUploadItem"
        "click .cancel": "onClickCancel"
        "click .create": "onClickCreateEventUpload"
        "click .to-download": "onClickToDownload"
        "click .to-upload": "onClickToUpload"
        "click .do-upload": "onClickDoUpload"
        "click .start-upload": "onClickStartUpload"
        "click .to-preview": "onClickToPreview"
        "click .confirm-upload": "onClickConfirmUpload"
        "click .upgrade-plan": "onClickUpgradePlan"
        "click .downgrade-plan": "onClickDowngradePlan"
        "click #loc-reset": "onClickLocationReset"
        "change #loc-name": "onChangedLocationName"

    initialize: (options) ->
        @shouldRender = false

        @talkViews = []

        @stripeHandler = StripeCheckout.configure
            key: 'pk_test_XuZFBi6ffYp4PwK5VhX4Zz5K'
            image: 'https://www.spkrbar.com/static/img/logo.png'
            token: (token, args) =>
                @finalizeImport(token.id)

        @createEventImportTemplate = Handlebars.compile($("#create-event-import-templ").html())
        @downloadTemplateTemplate = Handlebars.compile($("#download-template-templ").html())
        @uploadTemplateTemplate = Handlebars.compile($("#upload-template-templ").html())
        @uploadingTemplate = Handlebars.compile($("#uploading-templ").html())
        @validationFailedTemplate = Handlebars.compile($("#validation-failed-templ").html())
        @uploadPreviewTemplate = Handlebars.compile($("#upload-preview-templ").html())
        @confirmBillingTemplate = Handlebars.compile($("#confirm-billing-templ").html())
        @importStartedTemplate = Handlebars.compile($("#import-started-templ").html())
        @importFinishedTemplate = Handlebars.compile($("#import-finished-templ").html())

        @locations = new SpkrBar.Collections.Locations()
        @locations.fetch()

        @eventImports = new SpkrBar.Collections.EventImports()
        @eventImports.fetch()

        @listenTo(@eventImports, "add remove reset", @invalidate)

        @invalidate()

    render: ->
        source = $(@template).html()
        template = Handlebars.compile(source)

        @$el.html(template(@context()))
        @

    beforeRender: ->

    afterRender: ->
        @updateDashboard()

    updateDashboard: ->
        if @model
            state = @model.get('state')

            if state == "AT_REST"
                @$el.find('.dashboard').html @downloadTemplateTemplate({})
            else if state == "TEMPLATE_DOWNLOADED"
                @renderUploadTemplate()
            else if state == "VALIDATION_FAILED"
                @renderFailedValidation()
            else if state == "VALIDATION_SUCCESSFUL"
                @renderUploadPreview()
            else if state == "IMPORT_STARTED"
                @renderImportStarted()
            else if state == "IMPORT_FINISHED"
                @renderImportFinished()
            else
                @renderNewImportTemplate()
        else
            @renderNewImportTemplate()

    renderNewImportTemplate: ->
        @$el.find('.dashboard').html @createEventImportTemplate({})

        @$el.find("#loc-name").typeahead
            source: @locations.map (x) -> x.get('name')
            updater: (item) =>
                @curLocation = @locations.find (x) -> x.get('name') == item
                if @curLocation
                    @$el.find('#loc-address').val(@curLocation.get('address'))
                    @$el.find('#loc-city').val(@curLocation.get('city'))
                    @$el.find('#loc-state').val(@curLocation.get('state'))
                    @$el.find('#loc-zip').val(@curLocation.get('zip_code'))
                item

        @$el.find('.new-import').addClass('active')

    renderUploadTemplate: ->
        html = @uploadTemplateTemplate
            csrf_token: csrftoken
            upload_id: @model.id

        @$el.find('.dashboard').html html

    renderFailedValidation: ->
        importErrors = new SpkrBar.Collections.EventImportErrors
            import: @model

        importErrors.fetch
            success: =>
                html = @validationFailedTemplate
                    errors: importErrors.map (x) -> x.get('description')
                @$el.find('.dashboard').html html

    renderUploadPreview: ->
        importSummary = new SpkrBar.Collections.EventImportSummary
            import: @model

        importSummary.fetch
            success: =>
                html = @uploadPreviewTemplate
                    summary: importSummary.map (x) ->
                        name: x.get('name')
                        description: x.get('description')
                @$el.find('.dashboard').html html

    renderImportStarted: ->
        @$el.find('.dashboard').html @importStartedTemplate({})

    renderImportFinished: ->
        link_slug = _.str.slugify(@model.get('name'))

        if user.get('plan_name') == 'yearly'
            event_link = '/event/' + link_slug
        else if user.get('plan_name') == 'forever'
            event_link = 'https://' + link_slug + '.spkrbar.com'

        @$el.find('.dashboard').html @importFinishedTemplate({link: event_link})

    validateAndSaveModel: ->
        if @model.isValid(true)
            @model.save null, 
                success: =>
                    @eventImports.add @model
                    @$el.find('.dashboard').html @downloadTemplateTemplate({})
        else
            @showValidationAlert()

    onClickNewImport: ->
        @renderNewImportTemplate()

    onClickEventUploadItem: (el) ->
        $('.item').removeClass('active')
        $(el.currentTarget).addClass('active')

        itemId = $(el.currentTarget).data 'id'

        if itemId != undefined
            @model = @eventImports.find (x) => x.id == itemId
        else
            @model = null

        @updateDashboard()

    onClickCancel: ->
        @$el.find('.dashboard').html ""

    onClickCreateEventUpload: ->
        @model = new SpkrBar.Models.EventImport()

        @model.set 'user', user 
        @model.set 'name', @$el.find('#event-name').val()

        if @curLocation
            @model.set 'location', @curLocation.id
            @validateAndSaveModel()
        else
            newLocation = new SpkrBar.Models.Location
                name: @$el.find('#loc-name').val();
                address: @$el.find('#loc-address').val();
                city: @$el.find('#loc-city').val();
                state: @$el.find('#loc-state').val();
                zip_code: @$el.find('#loc-zip').val();

            if newLocation.isValid(true)
                newLocation.save null,
                    success: =>
                        @curLocation = newLocation
                        @locations.add @curLocation
                        @model.set 'location', @curLocation
                        @validateAndSaveModel()
            else
                @showValidationAlert()

    onClickToDownload: ->
        if @model.get('state') == 'IMPORT_FINISHED'
            @$el.find('.dashboard').html @downloadTemplateTemplate({})
        else
            @model.set 'state', 'AT_REST'
            @model.save null,
                success: =>
                    @$el.find('.dashboard').html @downloadTemplateTemplate({})

    onClickToUpload: ->
        if @model.get('state') == 'IMPORT_FINISHED'
            @renderUploadTemplate()
        else
            @model.set 'state', 'TEMPLATE_DOWNLOADED'
            @model.save null,
                success: =>
                    @renderUploadTemplate()

    onClickDoUpload: ->
        $('#file-choice').click()

    onClickStartUpload: ->
        if not $('#file-choice').val()
            $('#file-choice').click()
            return 

        logPostFrame = =>
            done = $('#post-frame').contents().find('.check-done').text()
            if _.str.trim(done) == "SUCCESS"
                $('#post-frame').attr('src', 'about:blank')
                @model.fetch
                    success: =>
                        @renderUploadPreview()
            else if _.str.trim(done) == "FAILED"
                $('#post-frame').attr('src', 'about:blank')
                @model.fetch
                    success: =>
                        @renderFailedValidation()
            else
                setTimeout logPostFrame, 500
        logPostFrame()

        $('#submit-upload').click()

    onClickToPreview: ->
        @renderUploadPreview()

    onClickUpgradePlan: ->
        user.set 'plan_name', 'forever'
        user.save null,
            success: =>
                @onClickConfirmUpload()

    onClickDowngradePlan: ->
        user.set 'plan_name', 'yearly'
        user.save null,
            success: =>
                @onClickConfirmUpload()

    onClickConfirmUpload: ->
        num_payments = (@eventImports.filter (x) -> x.get('billed')).length
        billed = num_payments != 0
        upgrade_offer = 2400 - Math.min((num_payments * 400), 1200)
        offer_savings = (3000 - upgrade_offer)

        html = @confirmBillingTemplate
            forever_plan: (user.get('plan_name') == "forever")
            yearly_plan: (user.get('plan_name') == "yearly")
            billed: @model.get('billed')
            upgrade_offer: upgrade_offer
            offer_savings: offer_savings

        @$el.find('.dashboard').html html

        $('.confirm-billing').off 'click', null
        if user.get('plan_name') == "forever"
            billed = user.get('billed')

            if billed
                $('.confirm-billing').on 'click', (ev) =>
                    @finalizeImport(0)
            else
                $('.confirm-billing').on 'click', (ev) =>
                    amount = upgrade_offer * 100
                    description = 'The Forever Plan ($' + upgrade_offer + '.00)'
                    @stripeHandler.open
                        name: 'SpkrBar.com'
                        description: description
                        amount: amount

                    ev.preventDefault()
        else if user.get('plan_name') == "yearly"
            billed = @model.get('billed')

            if billed
                $('.confirm-billing').on 'click', (ev) =>
                    @finalizeImport(0)
            else
                $('.confirm-billing').on 'click', (ev) =>
                    @stripeHandler.open
                        name: 'SpkrBar.com'
                        description: 'The Yearly Plan ($600.00)'
                        amount: 60000

                    ev.preventDefault()

    finalizeImport: (token) ->
        confirmRequest = $.post '/rest/import/' + @model.id + '/confirm', {'token': token}

        confirmRequest.done =>
            @model.fetch 
                success: =>
                    @renderImportFinished()

        confirmRequest.fail ->
            $.colorbox
                html: "<h1 class='alert alert-error' style='margin:20px; width:300px'>Sorry. We couldn't charge your card. Please try again.</h1>"
            $.colorbox.resize()

    invalidate: ->
        if not @shouldRender
            setTimeout =>
                @beforeRender()
                @render()
                @afterRender()
                @shouldRender = false
            , 500
            @shouldRender = true

    onClickLocationReset: ->
        @$el.find('#loc-name').val('')
        @resetFields()

    onChangedLocationName: (el) ->
        text = $(el.currentTarget).val()
        location = @locations.find (x) => 
            x.get('name') == text

        unless location
            @resetFields()

    resetFields: ->
            @$el.find('#loc-address').val('');
            @$el.find('#loc-city').val('');
            @$el.find('#loc-state').val('');
            @$el.find('#loc-zip').val('');

    context: ->
        imports: @eventImports.map (x) -> 
            id: x.id
            name: x.get('name')
        forever: user.get('forever_access')
