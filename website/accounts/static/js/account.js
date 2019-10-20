$(document).ready(function(){
  var browserBtn = document.getElementById('id_picture');
  var profileImg = document.getElementById('profile_img');

    browserBtn.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            profileImg.src = URL.createObjectURL(this.files[0]); // set src to file url
        }
    });


});
