$(document).ready(function() {

    $(".upvote").on("click", function() {
        upvote($(this));
    });

    // updater.poll();
    updater.fetch_playlist();
    updater.fetch_songs();
    updater.start();
});

function upvote(songId) {
    message = {"id": songId};
    updater.socket.send(JSON.stringify(message))
}

function addSong(songId) {
    $.ajax({
        url: "/addSong", 
        data: JSON.stringify({"id": songId}), 
        type: "POST",
        success: (response) => {
            console.log("success");
            updater.displayPlaylist(response)},
    });
}

var updater = {
    errorSleepTime: 500,
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/displaySongs";
        console.log(url);
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = (event) => {
            console.log(event);
            updater.displayPlaylist(JSON.parse(event.data));
        }
    },

    fetch_playlist: function() {
        $.ajax({
            url: "/playlist",
            type: "GET",
            success: (response) => {
                updater.displayPlaylist(response)
            },
            error: updater.onError
        })
    },

    fetch_songs: function() {
        $.ajax({
            url: "/songs",
            type: "GET",
            success: (response) => {
                updater.displayCatalogue(response)
            },
            error: updater.onError
        })
    },

    displayPlaylist: (response) => {
        console.log("here")
        var songList = response.songs;
        var $songList = $('#song-list');
        $songList.empty();
        
        songList.forEach((song) => {
            var listItem = $('<div>');
            var songName = $('<li>').text(`${song.title} - ${song.upvotes}`);
            var upvoteButton = $('<button>').addClass('.upvote').text('Upvote').attr('data-song-name', song);
            upvoteButton.click( () => {upvote(song.id)})
            listItem.append(songName, upvoteButton);
            $songList.append(listItem);
        });
    },

    displayCatalogue: (response) => {
        var songList = response.songs;
        var $songList = $('#catalogue');
        $songList.empty();
        
        songList.forEach((song) => {
            var listItem = $('<div>');
            var songName = $('<li>').text(`${song.title}`);
            var addButton = $('<button>').addClass('.addSong').text('Add Song').attr('data-song-name', song);
            addButton.click( () => {addSong(song.id)})
            listItem.append(songName, addButton);
            $songList.append(listItem);
        });
    }
}