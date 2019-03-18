var URL_LOCALHOST = "http://localhost:8000/upload/csv/";



function handleFileChange() {
    let file = document.getElementById("file").files[0];
    document.getElementById("fileMessage").innerText = file.name;
    document.getElementById("keyInput").value = "CSVs/" + file.name;
}

function sendCSV(){
    let file = document.getElementById("file").files[0];
    console.info(file);
    // let file = $("#file").files[0];

    //datatype can be "multipart/form-data"
    $.ajax({
        url: URL_LOCALHOST,
        data: file,
        dataType: "json",
        type: "GET",
        contentType: "multipart/form-data",
        processData: false,
        async: false,
        headers: {
                'Content-Type': "multipart/form-data",
            },
        success: function (data, status, xhr){
            console.log("this is received data:\n");
            console.log(data);
            console.log('\n');
            console.log('Length of data is '+ data.length);
            console.log('Length of x is '+ data['0'][0]);
            let outer="";
            for(let x in data){
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
            url: URL_LOCALHOST + "user/login",
            type: "POST",
            headers: {
                'Content-Type': "application/json",



            },
            contentType: "application/json; charset=utf-8",
            async: false,
            data: userData,

            success: function (html_data, status, xhr) {
                let token = xhr.getResponseHeader("Authorization");

                window.localStorage.setItem("Authorization", token);

                window.localStorage.setItem('page', html_data);

                document.open();
                document.write(html_data);
                document.close();


            },

            error: function (data, status, xhr) {
                console.error('Error_data: ', data);
                console.error('Error_status: ', status);
                console.error('Error_xhr: ', xhr);
            }

        }
    );
}