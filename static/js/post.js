document.addEventListener("DOMContentLoaded", () => {
  let hideButtons = document.querySelectorAll(".post__top-right .fa-xmark");
  hideButtons.forEach((button) => {
    button.addEventListener("click", () => {
      let postID = button.getAttribute("data-post-id");

      // postni olish
      let post = document.querySelector(`[data-post-id="${postID}"]`);
      // <div class='post' data-post-id='2'>
      // <div class='post' data-post-id='3'>
      let postParent = post.closest(".post");

      if (postParent) {
        postParent.style.display = "none";
      }
    });
  });
});
