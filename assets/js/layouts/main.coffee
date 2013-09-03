SpkrBar.Layouts.Main = Backbone.Marionette.Layout.extend
  template: Handlebars.compile($("#main-layout-templ").html())

  events:
    "click img.logo": "onClickLogo"
    "click a.talks": "onClickTalks"
    "click a.speakers": "onClickSpeakers"
    "click a.events": "onClickEvents"
    "click a.add-talk": "onClickAddTalk"
    "click a.add-event": "onClickAddEvent"
    "click a.blog": "onClickBlog"
    "click a.login": "onClickLogin"
    "click a.register": "onClickRegister"
    "click a.profile": "onClickProfile"
    "click a.invite": "onClickInvite"

  regions:
    content: "#content"

  userIsSpeaker: ->
    if not window.user then return false
    window.user.get('is_speaker')

  userIsEventPlanner: ->
    if not window.user then return false
    window.user.get('is_event_planner')

  userIsSuperuser: ->
    if not window.user then return false
    window.user.get('is_superuser')

  serializeData: ->
    userIsAnonymous: if window.user then false else true
    userIsSpeaker: @userIsSpeaker()
    userIsEventPlanner: @userIsEventPlanner()
    userIsSuperuser: @userIsSuperuser()

  onClickLogo: ->
    spkrbar.showIndexView()

  onClickTalks: ->
    spkrbar.mainLayout.content.show(spkrbar.generalLayout)

  onClickSpeakers: ->
    console.log "speakers"

  onClickEvents: ->
    console.log "events"

  onClickAddTalk: ->
    console.log "Add talk"

  onClickAddEvent: ->
    console.log "Add Event"

  onClickBlog: ->
    console.log "Blog"

  onClickLogin: ->
    console.log "Login"

  onClickRegister: ->
    console.log "Register"

  onClickProfile: ->
    console.log "Profile"

  onClickInvite: ->
    console.log "Invite"
