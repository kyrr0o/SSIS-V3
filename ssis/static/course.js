$(document).ready(function () {
    $("#addCourseForm").on("submit", function (event) {
        $.ajax({
            data: {
                code: $("#code").val(),
                name: $("#name").val(),
                college_code: $("#college_code").val()
            },
            type: "POST",
            url: "/course/add",
        }).done(function (data) {
            if (data.error) {
                $("#erroraddmsg").text(data.error).show();
            }
            else {
                alert("Successfully added course")
                window.location.href = "/course"
            }
        });
        event.preventDefault();
    });
    
    $(".delete-Course").click(function () {
        var courseCode = $(this).data("course-code");
    

        $("#deleteCourseForm").click(function () {
            $.ajax({
                type: "POST",
                url: "/course/delete",
                data: { csasdsda: courseCode }
            }).done(function (data) {
                if (data.error) {
                    $("#errordeletemsg").text(data.error).show();
                }
                else {
                    alert("Sucessfully deleted course: " + courseCode)
                    window.location.href = "/course"
    
                }
            });    
        });


      });

    $('.edit-Course').on("click", function(event) {
        var coursecode = $(this).data('course-code')
        var coursename = $(this).data('course-name')
        var course_college = $(this).data('course-college')

        $('#edit_course_code').val(coursecode)
        $('#edit_course_name').val(coursename)
        $('#edit_course_college').val(course_college)

        $("#editCourseForm").on("submit", function (event) {
            $.ajax({
                data: {
                    code : coursecode,
                    edit_course_code: $("#edit_course_code").val(),
                    edit_course_name: $("#edit_course_name").val(),
                    edit_course_college: $("#edit_course_college").val()
                },
                type: "POST",
                url: "/course/edit",
            }).done(function (data) {
                if (data.error) {
                    $("#erroreditmsg").text(data.error).show();
                }
                else {
                    alert("Successfully edited course")
                    window.location.href = "/course"
                }
            });
            event.preventDefault();
        });
        


    });

   

    $('#gobackcourse').on("click", function() {
        window.location.href = "/course"


    });


});
