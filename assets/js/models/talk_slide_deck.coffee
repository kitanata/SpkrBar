SpkrBar.Models.TalkSlideDeck = Backbone.Model.extend
    defaults:
        source: "SPEAKERDECK"
        embed_data: ""
        aspect: 1.33333333333333
        embed_code: ""
        
    urlRoot: "/rest/talk_slide"
