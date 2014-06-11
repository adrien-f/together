TogetherApp = angular.module 'TogetherApp', ['ngRoute', 'ngResource', 'angularMoment', 'ui.bootstrap']

TogetherApp.factory 'Playlist', ['$resource', ($resource) ->
  return $resource('/api/:userId/playlists/:playlistSlug', null, {
    update: {method: 'PUT'}
  })
]

TogetherApp.config ['$httpProvider', ($httpProvider) ->
  $httpProvider.defaults.headers.common['X-CSRFToken'] = $('meta[name=csrf-token]').attr('content');
]

TogetherApp.factory 'alertService', ['$rootScope', '$timeout', ($rootScope, $timeout) ->
  $rootScope.alerts = []
  alertService =
    add: (type, msg) ->
      alert_id = Math.floor((Math.random() * 100) + 1)
      $rootScope.alerts.push {type: type, msg: msg, alert_id: alert_id, close: -> alertService.closeAlert(this)}
      $timeout =>
        @closeAlertId(alert_id)
      , 3000
    closeAlert: (alert) ->
      @closeAlertIdx $rootScope.alerts.indexOf(alert)
    closeAlertId: (id) ->
      for alert in $rootScope.alerts
        if alert?.alert_id == id
          @closeAlert(alert)
    closeAlertIdx: (index) ->
      $rootScope.alerts.splice index, 1
]

TogetherApp.factory 'playlistService', ['$window', '$rootScope', ($window, $rootScope) ->
  $rootScope.videoPlaylist = []
  $rootScope.playlistEmpty = false
  $rootScope.playerPlaying = false
  playlistService =
    addVideo: (video) ->
      $rootScope.videoPlaylist.push(video)
      if $rootScope.videoPlaylist.length == 1
        @playVideo(video)
    onStateChange: (event) ->
      $rootScope.$apply ->
        if event.data == YT.PlayerState.PLAYING
          $rootScope.playerPlaying = true
        if event.data == YT.PlayerState.PAUSED
          $rootScope.playerPlaying = false
    next: ->
      currentIndex = $rootScope.videoPlaylist.indexOf($rootScope.videoPlaying)
      next = $rootScope.videoPlaylist[currentIndex + 1]
      if next != undefined
        @playVideo(next)
      else
        @playVideo($rootScope.videoPlaylist[0])
    playVideo: (video, reset=false) ->
      if reset
        $rootScope.videoPlaylist = [video]
      $rootScope.videoPlaying = video
      @youtubePlayer.loadVideoById(video.youtube_id)

  return playlistService
]

TogetherApp.run ($window, playlistService) ->
  tag = document.createElement('script');
  tag.src = "//www.youtube.com/iframe_api";
  firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
  $window.onYouTubeIframeAPIReady = ->
    playlistService.youtubePlayer = new YT.Player 'ytplayer', {
      height: '200',
      width: '356',
      playerVars: {controls: 0},
      events: {
        'onStateChange': playlistService.onStateChange
      }
    }


TogetherApp.config ['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->
  $locationProvider.html5Mode true
  $routeProvider
  .when '/', {
    templateUrl: 'playlists.html'
    controller: 'PlaylistsCtrl'
  }
  .when '/playlist/:playlistSlug', {
    templateUrl: 'playlist.html',
    controller: 'PlaylistCtrl'
  }
  .when '/404', {
    templateUrl: '404.html'
  }
]

TogetherApp.controller 'PlaylistsCtrl', ['$scope', 'Playlist', '$location', ($scope, Playlist, $location) ->
  $scope.playlists = Playlist.query {userId: window.user.id}

  $scope.newPlaylist = ->
    playlist = new Playlist
    playlist.name = $scope.newPlaylistName
    playlist.$save({userId: window.user.id})
    .then (new_playlist) ->
      $location.path("/playlist/#{new_playlist.slug}")
    , (error) ->
      console.log(error)

]

TogetherApp.controller 'PlaylistCtrl', ['$scope', '$routeParams', 'Playlist', 'alertService', '$http', 'playlistService', '$modal', '$location', ($scope, $routeParams, Playlist, alertService, $http, playlistService, $modal, $location) ->

  $scope.results = []
  $scope.searchQuery = ""

  $scope.playlist = Playlist.get {
      userId: window.user.id,
      playlistSlug: $routeParams.playlistSlug
  }, ->
    return
  , (response) ->
    if response.status == 404
      $location.path("/404")


  $scope.searchVideo = ->
    if $scope.searchQuery == "" or $scope.searchQuery.length < 5
      alertService.add('warning', 'The search query cannot be empty or less than 5 characters.')
      return
    parser = document.createElement('a')
    parser.href = $scope.searchQuery
    if parser.hostname == 'www.youtube.com' or parser.hostname == 'youtube.com'
      $scope.addVideo(parser.href)
      return
    $scope.youtubeSearchLoading = true
    $http.post('/api/youtube/search?query=' + $scope.searchQuery, {})
    .success (results) ->
      $scope.youtubeSearchLoading = false
      $scope.youtubeSearchSuccess = true
      $scope.results = results.items
    .error (error) ->
      $scope.youtubeSearchLoading = false
      $scope.youtubeSearchError = true

  $scope.closeSearch = ->
    $scope.results = []
    $scope.searchQuery = ""

  $scope.addVideo = (videoId) ->
    Playlist.update {userId: window.user.id, playlistSlug: $routeParams.playlistSlug}, {videoId: videoId}
      .$promise.then (playlistElement) ->
        alertService.add('success', 'Video added to playlist.')
        $scope.playlist.elements.push(playlistElement)
      , (error) ->
        alertService.add('danger', error.message)

  $scope.removeVideo = (videoId) ->
    $http.delete("/api/#{window.user.id}/playlists/#{$routeParams.playlistSlug}/videos/#{videoId}")
      .then (result) ->
        for element, index in $scope.playlist.elements
          if element.id == videoId
            $scope.playlist.elements.splice index, 1

  $scope.playVideo = (video) ->
    playlistService.playVideo(video, true)

  $scope.queueVideo = (video) ->
    playlistService.addVideo(video)

  $scope.settings = ->
    $modal.open {
      templateUrl: 'playlist_settings.html',
      controller: 'PlaylistSettingsCtrl',
      scope: $scope
    }
]

TogetherApp.controller 'PlaylistSettingsCtrl', ['$scope', 'Playlist', '$location', ($scope, Playlist, $location) ->
  $scope.playlistName = angular.copy($scope.playlist.name)
  $scope.saveSettings = ->
    Playlist.save {userId: window.user.id, playlistSlug: $scope.playlist.slug}, {
      name: $scope.playlistName
    }, (playlist) ->
      $scope.$close();
      $location.path("/playlist/#{playlist.slug}")
]

TogetherApp.controller 'PlayerCtrl', ['$scope', 'playlistService', ($scope, playlistService) ->

    $scope.pausePlay = ->
      if playlistService.youtubePlayer.getPlayerState() == YT.PlayerState.PAUSED
        playlistService.youtubePlayer.playVideo()
      else if playlistService.youtubePlayer.getPlayerState() == YT.PlayerState.PLAYING
        playlistService.youtubePlayer.pauseVideo()

    $scope.nextVideo = ->
      playlistService.next()
]
