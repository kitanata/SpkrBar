SpkrBar.Models.Location = Backbone.RelationalModel.extend
    defaults:
        name: ""
        address: ""
        city: ""
        state: ""
        zip_code: "00000"

    initialize: ->

    urlRoot: "/rest/location"

    validation:
        name:
            required: true
        address:
            required: true
        city:
            required: true
        state:
            required: true
        zip_code:
            required: true
            length: 5
