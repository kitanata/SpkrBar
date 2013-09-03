SpkrBar.Models.Comment = Backbone.Model.extend
    defaults:
        user: 0
        name: ""
        comment: ""
        parent: 0
        children: []
        datetime: ""

    urlRoot: -> "/comment"
