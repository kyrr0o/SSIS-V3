$(document).ready(function () {
  function previewPhotoInput(input, preview) {
    const chosenFile = input[0].files[0];
    if (chosenFile) {
      const reader = new FileReader();
      reader.addEventListener('load', function () {
        preview.attr('src', reader.result);
      });
      reader.readAsDataURL(chosenFile);
    }
  }

  $("#formFile").change(function () {
    previewPhotoInput($("#formFile"), $("#photo-preview"));
  });

  $("#editFormFile").change(function () {
    previewPhotoInput($("#editFormFile"), $("#edit_photo_preview"));
  });


  $("#addStudentForm").on("submit", function (event) {
    const preview2 = document.querySelector('#photo-preview');
    $('body').append('<div class="loading-overlay"> <div class="spinner-border me-3" style="width: 3rem; height: 3rem;"> <span class="visually-hidden">Loading...</span></div><h2> Adding Student \n This should only take a minute... </h2></div>');
    $.ajax({
      type: "POST",
      url: "/student/add",
      data: new FormData($(this)[0]),
      contentType : false,
      processData: false,
    }).done(function (data) {
      $('.loading-overlay').remove();
      if (data.error) {
        $("#erroraddstdmsg").text(data.error).show();
        preview2.setAttribute('src' , urlimg)

      } else {
        alert("Successfully added student");
        window.location.href = "/student";
      }
    });
    event.preventDefault();
  });

  $(".delete-Student").click(function () {
    var studentId = $(this).data("student-id");

    $("#deleteStudentForm").click(function () {
      $('body').append('<div class="loading-overlay"> <div class="spinner-border me-3" style="width: 3rem; height: 3rem;"> <span class="visually-hidden">Loading...</span></div><h2> Deleting Student \n This should only take a minute... </h2></div>');
      $.ajax({
        type: "POST",
        url: "/student/delete",
        data: { csasdsda: studentId },
      }).done(function (data) {
        $('.loading-overlay').remove();
        if (data.error) {
          $("#errordeletstdemsg").text(data.error).show();
        } else {
          alert("Sucessfully deleted student: " + studentId);
          window.location.href = "/student";
        }
      });
    });
  });

  $(".edit-Student").on("click", function () {
    var id = $(this).data("student-id");
    var firstname = $(this).data("student-firstname");
    var lastname = $(this).data("student-lastname");
    var course_code = $(this).data("student-course");
    var year = $(this).data("student-year");
    var gender = $(this).data("student-gender");
    var picture = $(this).data("student-picture")

    const preview = document.querySelector('#edit_photo_preview');
    if(picture != 'None') {
      preview.setAttribute('src', picture)
    }
    else{
      preview.setAttribute('src' , urlimg)
    }

    $("#edit_student_id").val(id);
    $("#edit_student_first_name").val(firstname);
    $("#edit_student_last_name").val(lastname);
    $("#edit_student_course_code").val(course_code);
    $("#edit_student_year").val(year);
    $("#edit_student_gender").val(gender);

    $("#editStudentForm").on("submit", function (event) {
      var formData = new FormData(this);
      formData.append('pastid', id);
      $('body').append('<div class="loading-overlay"> <div class="spinner-border me-3" style="width: 3rem; height: 3rem;"> <span class="visually-hidden">Loading...</span></div><h2> Editing Student \n This should only take a minute... </h2></div>');
      $.ajax({
        type: "POST",
        url: "/student/edit",
        data: formData,
        contentType : false,
        processData: false,
      }).done(function (data) {
        $('.loading-overlay').remove();
        if (data.error) {
          $("#erroreditstdmsg").text(data.error).show();
          preview.setAttribute('src' , urlimg)
        } else {
          alert("Successfully edited student");
          window.location.href = "/student";
        }
      });
      event.preventDefault();
    });
  });

  $("#gobackstudent").on("click", function () {
    window.location.href = "/student";
  });
});
