$(document).ready(function () {
    $('#gobackcollege').on("click", function() {
        window.location.href = "/college"
    });

    $("#addCollegeForm").on("submit", function (event) {
        $.ajax({
            data: {
                code: $("#college_code").val(),
                name: $("#college_name").val(),
            },
            type: "POST",
            url: "/college/add",
        }).done(function (data) {
            if (data.error) {
                $("#errorcollegeaddmsg").text(data.error).show();
            }
            else {
                alert("Successfully added college")
                window.location.href = "/college"
            }
        });
        event.preventDefault();
    });


    $(".delete-College").click(function ( ) {
        var collegeCode = $(this).data("college-code")

        $("#deleteCollegeForm").click(function () {
            $.ajax({
                type : "POST",
                url: "college/delete",
                data: {
                    code : collegeCode
                }
            }).done( function (data) {
                if (data.error) {
                    $("#errorcoldeletemsg").text(data.error).show();
                }
                else {
                    alert("Succesfully deleted coursE:" + collegeCode)
                    window.location.href = "/college"
                }
            });
        });
    });

    $('.edit-College').on("click", function(event) {
        var collegecode = $(this).data('college-code')
        var collegename = $(this).data('college-name')

        $('#edit_college_code').val(collegecode)
        $('#edit_college_name').val(collegename)

        $("#editCollegeForm").on("submit", function (event) {
            $.ajax({
                data: {
                    code : collegecode,
                    edit_college_code: $("#edit_college_code").val(),
                    edit_college_name: $("#edit_college_name").val(),
                },
                type: "POST",
                url: "/college/edit",
            }).done(function (data) {
                if (data.error) {
                    $("#errorcollegeeditmsg").text(data.error).show();
                }
                else {
                    alert("Successfully edited college")
                    window.location.href = "/college"
                }
            });
            event.preventDefault();
        });
        


    });


});