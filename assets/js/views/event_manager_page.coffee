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
        "click .confirm-billing": "onClickConfirmBilling"
        "click #invite-btn": "onClickInviteSpeakers"
        "click #billing-btn": "onClickBillingDetails"
        "click #loc-reset": "onClickLocationReset"
        "change #loc-name": "onChangedLocationName"

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
        @billingDetailsTemplate = Handlebars.compile($("#billing-details-templ").html())

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
            console.log state

            if state == "AT_REST"
                @$el.find('.dashboard').html @downloadTemplateTemplate({})
            else if state == "TEMPLATE_DOWNLOADED"
                @renderUploadTemplate()
            else if state == "VALIDATION_FAILED"
                @renderFailedValidation()

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

    validateAndSaveModel: ->
        if @model.isValid(true)
            @model.save null, 
                success: =>
                    @eventImports.add @model
                    @$el.find('.dashboard').html @downloadTemplateTemplate({})
        else
            @showValidationAlert()

    onClickNewImport: ->
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

    onClickEventUploadItem: (el) ->
        itemId = $(el.currentTarget).data 'id'

        $('.item').removeClass('active')
        $(el.currentTarget).addClass('active')

        @model = @eventImports.find (x) => x.id == itemId
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
        @model.set 'state', 'AT_REST'
        @model.save null,
            success: =>
                @$el.find('.dashboard').html @downloadTemplateTemplate({})

    onClickToUpload: ->
        @model.set 'state', 'TEMPLATE_DOWNLOADED'
        @model.save null,
            success: =>
                @renderUploadTemplate()

    onClickDoUpload: ->
        $('#file-choice').click()

    onClickStartUpload: ->
        logPostFrame = =>
            done = $('#post-frame').contents().find('.check-done').text()
            if _.str.trim(done) == "SUCCESS"
                $('#post-frame').attr('src', 'about:blank')
                @model.fetch
                    success: =>
                        @$el.find('.dashboard').html @uploadPreviewTemplate({})
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
        @$el.find('.dashboard').html @uploadPreviewTemplate({})

    onClickConfirmUpload: ->
        @$el.find('.dashboard').html @confirmBillingTemplate({})

    onClickConfirmBilling: ->
        @$el.find('.dashboard').html @importFinishedTemplate({})

    onClickBillingDetails: ->
        num_payments = (@eventImports.filter (x) -> x.get('billed')).length
        billed = num_payments != 0
        upgrade_offer = 2400 - Math.min((num_payments * 400), 1200)
        offer_savings = (3000 - upgrade_offer)

        billingDetails = @billingDetailsTemplate
            forever_plan: (user.get('plan_name') == "forever")
            yearly_plan: (user.get('plan_name') == "yearly")
            billed: billed
            upgrade_offer: upgrade_offer
            offer_savings: offer_savings

        console.log billingDetails

        @$el.find('.dashboard').html billingDetails

    onClickInviteSpeakers: ->
        console.log "Invite Speakers"

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

    userLoggedIn: ->
        user != null

    planName: ->
        if user.get('plan_name') == 'yearly'
            "The Yearly Plan"
        else if user.get('plan_name') == 'forever'
            "The Forever Plan"

    context: ->
        imports: @eventImports.map (x) -> 
            id: x.id
            name: x.get('name')
        plan_name: @planName()

