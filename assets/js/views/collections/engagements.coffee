SpkrBar.Views.Collections.EngagementsThumb = Backbone.Marionette.CollectionView.extend
    itemView: SpkrBar.Views.Items.EngagementThumb

SpkrBar.Views.Collections.EngagementsSpan6 = Backbone.Marionette.CompositeView.extend
    template: Handlebars.compile($("#engagement-span6-comp-templ").html())
    itemView: SpkrBar.Views.Items.EngagementSpan6
    itemViewContainer: ".talk-list"
