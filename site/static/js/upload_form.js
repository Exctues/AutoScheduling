var URL_LOCALHOST = "http://127.0.0.1:8000/";


function handleFileChange() {
    let file = document.getElementById("file").files[0];
    document.getElementById("fileMessage").innerText = file.name;
    document.getElementById("keyInput").value = "CSVs/" + file.name;
}

function sendCSV() {
    let file = document.getElementById("file").files[0];
    console.info(file);
    // let file = $("#file").files[0];

    //datatype can be "multipart/form-data"
    $.ajax({
        url: URL_LOCALHOST + "upload/csv/",
        data: file,
        dataType: "json",
        type: "GET",
        contentType: "multipart/form-data",
        processData: false,
        async: false,
        headers: {
            'Content-Type': "multipart/form-data",
            'Access-Control-Allow-Origin': '*'
        },
        success: function (data, status, xhr) {
            console.log("this is received data:\n");
            console.log(data);
            console.log('\n');
            console.log('Length of data is ' + data.length);
            console.log('Length of x is ' + data['0'][0]);
            let outer = "";
            for (let x in data) {
                console.info("NEXT ELEMENT IS\n");
                console.info(data[x]);
                outer += data[x] + "<br>"
            }
            document.getElementById('Schedule').innerHTML = outer;
        },

        error: function (data, status, xhr) {
            console.error('Error_data: ', data);
            console.error('Error_status: ', status);
            console.error('Error_xhr: ', xhr);
        }
    })
}

function sendLoginAndPassword() {
    let user = $("#inputUsername").val();
    let pass = $("#inputPassword").val();

    let userData = JSON.stringify({
        username: user,
        password: pass
    });

    $.ajax({
            url: URL_LOCALHOST + "login/",
            type: "POST",
            headers: {
                'Content-Type': "application/json",
            },
            contentType: "application/json; charset=utf-8",
            async: false,
            data: userData,
            success: function (html_data, status, xhr) {
                window.location = URL_LOCALHOST + "upload/";
            },
            error: function (data, status, xhr) {
                console.error('Error_data: ', data);
                console.error('Error_status: ', status);
                console.error('Error_xhr: ', xhr);
                alert("Invalid credentials, please try again");
            }
        }
    );
}

function register() {
    let email = $("#inputEmail").val();
    let user = $("#inputUserName").val();
    let pass = $("#inputPassword").val();

    let userData = JSON.stringify({
        email: email,
        username: user,
        password: pass
    });

    $.ajax({
            url: URL_LOCALHOST + "register/",
            type: "POST",
            headers: {
                'Content-Type': "application/json",
            },
            contentType: "application/json; charset=utf-8",
            async: false,
            data: userData,
            success: function (html_data, status, xhr) {
                window.location = URL_LOCALHOST + "login/";
                alert("You have been successfully regitered");
            },
            error: function (data, status, xhr) {
                console.error('Error_data: ', data);
                console.error('Error_status: ', status);
                console.error('Error_xhr: ', xhr);
                alert("User already exists, please try again");
            }
        }
    );
}

function getSchedule() {
    var list = [];
    $("tr.item").each(function () {

        var course_name = $(this).find("td[id='course_name']")[0].innerText;
        var lesson_type = $(this).find("td[id='lesson_type']")[0].innerText;
        var faculty = $(this).find("td[id='faculty']")[0].innerText;
        var group = $(this).find("td[id='group']")[0].innerText;
        var day = $(this).find("#day option:selected").text();
        var time = $(this).find("#time option:selected").text();
        var auditoroium = $(this).find("#auditorium option:selected").text();
        //[{"Course_name": "Discrete Math and Logic", "Lesson_type": "Lecture", "Faculty": "Nikolay Shilov", "Group": "B18", "Day": "Wednesday", "Time": "18:55-20:25", "Auditorium": "109"}
        list.push({
            "Course_name": course_name,
            "Lesson_type": lesson_type,
            "Faculty": faculty,
            "Group": group,
            "Day": day,
            "Time": time,
            "Auditorium": auditoroium
        })
    });
    return JSON.stringify({
        schedule: list
    });
}

function saveSchedule() {

    userData = getSchedule();

    $.ajax({
            url: URL_LOCALHOST + 'save_schedule/' + a + '/',
            type: "POST",
            headers: {
                'Content-Type': "application/json",
            },
            contentType: "application/json; charset=utf-8",
            async: false,
            data: userData,
            success: function (data, textStatus) {
                alert('Schedule have been successfully saved');
            }
            ,
            error: function (data, status, xhr) {
                console.log(data);
                var error1 = data.responseText;
                alert('Could not save schedule:' + error1);
            }
        }
    );
}

function sendSchedule() {

    userData = getSchedule();

    $.ajax({
            url: window.location.pathname,
            type: "POST",
            headers: {
                'Content-Type': "application/json",
            },
            contentType: "application/json; charset=utf-8",
            async: false,
            data: userData,
            success: function (data, textStatus) {
                var url = URL_LOCALHOST + data;
                var win = window.open(url, '_blank');
                if (win) {
                    win.focus();
                } else {
                    alert('Please allow popups for this website');
                }
            }
            ,
            error: function (data, status, xhr) {
                console.log(data);
                var error1 = data.responseText;
                alert('Please correct the schedule and try again:' + error1);
            }
        }
    );
}