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
const songArt = document.getElementById('songArt');
const imageBack = document.querySelector('.image-back');
const searchInput = document.getElementById('searchInput');

let currentRotation = 0;
let isSpinning = false;
let animationFrameId;
let currentTrack = 0;

// Rotation Functions
function updateRotation() {
  if (isSpinning) {
    currentRotation += 1.8;
    imageBack.style.transform = `rotate(${currentRotation}deg)`;
    animationFrameId = requestAnimationFrame(updateRotation);
  }
}

function searchAlbum(albumTitle) {
  let searchInput = document.getElementById("searchInput");
  searchInput.value = ""; // Clear input before typing effect

  let i = 0;
  function typeNextChar() {
      if (i < albumTitle.length) {
          searchInput.value += albumTitle[i]; // Add next letter
          i++;
          setTimeout(typeNextChar, 100); // Adjust speed here (milliseconds per letter)
      } else {
          searchInput.dispatchEvent(new Event("input")); // Trigger search after full text
      }
  }

  typeNextChar();
}


function getCurrentRotation(el) {
  const matrix = window.getComputedStyle(el).getPropertyValue('transform');
  if (matrix !== 'none') {
    const values = matrix.split('(')[1].split(')')[0].split(',');
    const a = values[0], b = values[1];
    const angle = Math.round(Math.atan2(b, a) * (180 / Math.PI));
    return angle < 0 ? angle + 360 : angle;
  }
  return 0;
}

function slowDown() {
  if (currentRotation > 0) {
    currentRotation -= 0.5;
    imageBack.style.transform = `rotate(${currentRotation}deg)`;
    animationFrameId = requestAnimationFrame(slowDown);
  } else {
    cancelAnimationFrame(animationFrameId);
  }
}

function updateMetadata() {
  if ('mediaSession' in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: songTitle.textContent,
      artist: songArtist.textContent,
      album: songAlbum.textContent,
      artwork: [
        { src: songArt.src, sizes: '512x512', type: 'image/jpeg' }
      ]
    });
  }
}

// Track Functions
function loadTrack(index) {
  const track = playlistItems[index];
  audioPlayer.src = track.getAttribute('data-src');
  audioPlayer.play();
  currentRotation = getCurrentRotation(imageBack);
  isSpinning = true;
  cancelAnimationFrame(animationFrameId);
  updateRotation();
  playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
  songTitle.textContent = track.getAttribute('songTitle');
  songTitle2.textContent = `${track.getAttribute('songArtist')} - ${track.getAttribute('songTitle')}`;
  songAlbum.textContent = track.getAttribute('songAlbum');
  songArtist.textContent = track.getAttribute('songArtist');
  songArt.src = track.getAttribute('songArt');
  updateMetadata()
}

function playPause() {
  if (audioPlayer.paused) {
    audioPlayer.play();
    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
    isSpinning = true;
    cancelAnimationFrame(animationFrameId);
    updateRotation();
  } else {
    audioPlayer.pause();
    playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
    isSpinning = false;
    slowDown();
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

// Search Functionality
function searchPlaylist() {
  const query = searchInput.value.toLowerCase();
  playlistItems.forEach(item => {
    const trackDiv = item.closest('.track');
    const title = item.getAttribute('songTitle').toLowerCase();
    const artist = item.getAttribute('songArtist').toLowerCase();
    const album = item.getAttribute('songAlbum').toLowerCase();
    if (title.includes(query) || artist.includes(query) || album.includes(query)) {
      trackDiv.style.display = '';
    } else {
      trackDiv.style.display = 'none';
    }
  });
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
searchInput.addEventListener('input', searchPlaylist);

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

if ('mediaSession' in navigator) {
  navigator.mediaSession.metadata = new MediaMetadata({
    title: songTitle.textContent, // Using the existing `songTitle` variable
    artist: songArtist.textContent, // Using the existing `songArtist` variable
    album: songAlbum.textContent, // Using the existing `songAlbum` variable
    artwork: [
      { src: songArt.src, sizes: '512x512', type: 'image/jpeg' } // Using the existing `songArt` variable
    ]
  });

  navigator.mediaSession.setActionHandler('play', function() {
    playPause()
  });

  navigator.mediaSession.setActionHandler('pause', function() {
    playPause()
  });

  navigator.mediaSession.setActionHandler('previoustrack', function() {
    prevTrack()
  });

  navigator.mediaSession.setActionHandler('nexttrack', function() {
    nextTrack()
  });
}
