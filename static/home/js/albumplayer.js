// Get elements
const audioPlayer = document.getElementById('audioPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const playlist = document.getElementById('playlist');
const playlistItems = [...playlist.getElementsByTagName('li')];
const seekBar = document.getElementById('seekBar');
const volumeBar = document.getElementById('volumeBar');
const currentTime = document.getElementById('currentTime');
const duration = document.getElementById('duration');
const songTitle = document.getElementById('songTitle');
const songTitle2 = document.getElementById('songTitle2');
const songAlbum = document.getElementById('songAlbum');
const songArtist = document.getElementById('songArtist');

let currentTrack = 0;

// Track Functions
function loadTrack(index) {
  const track = playlistItems[index];
  audioPlayer.src = track.getAttribute('data-src');
  audioPlayer.play();
  playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
  songTitle.textContent = track.getAttribute('songTitle');
  songTitle2.textContent = `${track.getAttribute('songArtist')} - ${track.getAttribute('songTitle')}`;
}

function playPause() {
  if (audioPlayer.paused) {
    audioPlayer.play();
    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
  } else {
    audioPlayer.pause();
    playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
  }
}

function nextTrack() {
  currentTrack = (currentTrack + 1) % playlistItems.length;
  loadTrack(currentTrack);
}

function prevTrack() {
  currentTrack = (currentTrack - 1 + playlistItems.length) % playlistItems.length;
  loadTrack(currentTrack);
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

// Event Listeners
playPauseBtn.addEventListener('click', playPause);
nextBtn.addEventListener('click', nextTrack);
prevBtn.addEventListener('click', prevTrack);
audioPlayer.addEventListener('ended', nextTrack);
playlist.addEventListener('click', e => {
  if (e.target && e.target.nodeName === 'LI') {
    currentTrack = playlistItems.indexOf(e.target);
    loadTrack(currentTrack);
  }
});

audioPlayer.onloadedmetadata = () => {
  duration.textContent = formatTime(audioPlayer.duration);
  seekBar.max = audioPlayer.duration;
};

audioPlayer.ontimeupdate = () => {
  currentTime.textContent = formatTime(audioPlayer.currentTime);
  seekBar.value = audioPlayer.currentTime;
};

seekBar.oninput = () => {
  audioPlayer.currentTime = seekBar.value;
};

volumeBar.oninput = () => {
  audioPlayer.volume = volumeBar.value;
};

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".see-more");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const expandable = this.previousElementSibling; // Get the related expandable div
            expandable.classList.toggle("active");

            // Change button text dynamically
            if (expandable.classList.contains("active")) {
                this.textContent = "See less...";
            } else {
                this.textContent = "See more...";
            }
        });
    });
});
