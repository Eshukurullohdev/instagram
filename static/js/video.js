document.addEventListener("DOMContentLoaded", () => {
  const progressBar = document.querySelectorAll(".progress-bar");
  
  const right_story = document.querySelector(".right_story_name");
  const loader = document.querySelectorAll(".loader");
  const pause = document.querySelector(".pause");
  const volume = document.querySelector(".volume");
  let video = document.querySelector("video");
  let file_extension = document.querySelector(".file_e").textContent;
  if (!video) video = null;
  let number = 0;
  let lastTime = null;
  let animation;
  let currentProgressBar = 0;

  loader.forEach((loader) => {
    loader.style.display = "none";
  });

  if (file_extension == "video") {
    const updateProgressBarVideo = () => {
      const progressBarFoiz = (video.currentTime / video.duration) * 100;
      progressBar[0].style.width = `${progressBarFoiz}%`;
      if (video.currentTime >= video.duration) {
        window.location.href = `/story/detail/${right_story.textContent}/`;
      }
    };

    video.addEventListener("timeupdate", () => {
      updateProgressBarVideo();
    });

    pause.addEventListener("click", () => {
      if (pause.classList.contains("fa-pause")) {
        video.pause();
        pause.classList.remove("fa-pause");
        pause.classList.add("fa-play");
      } else {
        video.play();
        pause.classList.add("fa-pause");
        pause.classList.remove("fa-play");
      }
    });

    volume.addEventListener("click", () => {
      video.muted = !video.muted;
      if (volume.classList.contains("fa-volume-xmark")) {
        volume.classList.remove("fa-volume-xmark");
        volume.classList.add("fa-volume-high");
      } else {
        volume.classList.add("fa-volume-xmark");
        volume.classList.remove("fa-volume-high");
      }
    });
  } else {
    const updateProgressBar = (timestamp) => {
      if (!lastTime) lastTime = timestamp; // Initial timestamp
      const progress = timestamp - lastTime;

      // Increment number by 0.5 every 16ms (~60fps)
      progressBar.forEach((bar) => {
        if (progress > 8) {
          number += 0.5;
          bar.firstElementChild.style.width = `${number}px`;
          lastTime = timestamp;
        }
      });

      if(number === progressBar[currentProgressBar].parentElement.clientWidth){
        currentProgressBar++;
        number = 0;
      }

      if (currentProgressBar !== progressBar.length) {       
        if (
          number < progressBar[currentProgressBar].parentElement.clientWidth
        ) {
          animation = requestAnimationFrame(updateProgressBar); 
        }
      } else {
        setTimeout(() => {
          if (right_story === null) {
            window.location.href = "/";
          } else {
            window.location.href = `/story/detail/${right_story.textContent}/`;
          }
        }, 500);
      }
    };

    requestAnimationFrame(updateProgressBar);
    pause.addEventListener("click", () => {
      if (animation !== null) {
        cancelAnimationFrame(animation);
        animation = null;
        pause.classList.remove("fa-pause");
        pause.classList.add("fa-play");
      } else {
        animation = requestAnimationFrame(updateProgressBar);
        pause.classList.remove("fa-play");
        pause.classList.add("fa-pause");
      }
    });
  }
});
