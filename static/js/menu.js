let count = 0;

$(document).ready(() => {
    $("#nav-placeholder").load('/home');
});

const sendData = () => {
    $('#progress').toggleClass("d-none");

    $.ajax({
        url: "/change/protocol",
        contentType: "application/json;charset=utf-8",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({
            'protocol': $("#routing option:selected").val(),
            'networks': $('input[name="network[]"]').map(function () { return this.value; }).get(),
        }),
        success: function (data) {
            if (data['msg'] == "SUCCESS") {
                console.log('Correcto ', data['msg']);
                $('#progress').toggleClass("d-none");
                $('#changed').text("Protocolo cambiado correctamente.")
            }
            else if (data['msg'] == "FAIL") {
                console.log('Incorrecto ', data['msg']);
                $('#progress').toggleClass("d-none");
                $('#changed').text("Error al cambiar el protocolo.")
            }
        }
    });
}

const loadTemplate = url => {
    $("#nav-placeholder").load(url);
}

const changeState = () => {
    $("#protocol_state").val($("#routing option:selected").text());
}

const deleteUser = user_name => {
    if (confirm("¿Está seguro que quiere eliminar a " + user_name + "?")) {
        $.ajax({
            url: "/delete/user/",
            type: "POST",
            dataType: "json",
            data: user_name,
            success: function (data) {
                if (data['status'] === "SUCCESS") {
                    alert("Se elimino correctamente!");
                } else {
                    alert("Error! ", data['msg']);
                }
                window.location.reload();
            }
        });
    }
}

const deleteDevice = device_name => {
    if (confirm("¿Está seguro que quiere eliminar a " + device_name + "?")) {
        $.ajax({
            url: "/delete/device/",
            type: "POST",
            dataType: "json",
            data: device_name,
            success: function (data) {
                if (data['status'] === "SUCCESS") {
                    alert("Se elimino correctamente!");
                } else {
                    alert("Error! ", data['msg']);
                }
                window.location.reload();
            }
        });
    }
}

function editRow(id) {
    if ($('#text' + id).prop("readonly") == false) {
        $('#text' + id).prop("readonly", true);
        $('#icon' + id).attr("title", "Edit");
        $('#icon' + id).text('edit');
    } else {
        $('#text' + id).prop("readonly", false);
        $('#text' + id).focus();
        $('#icon' + id).attr("title", "Save");
        $('#icon' + id).text('playlist_add_check');
    }
}

const deleteRow = id => {
    $('#' + id).remove();
}

const addRow = () => {
    count++;

    $('#netTable').append("<tr id=" + count + ">" +
        "<td> <input class='form-control' type='text' id=text" + count + " name='network[]' required> </td>" +
        "<td class='col-sm-2'>" +
        "<a href='#edit' class='ps-4 pe-3' data-toggle='modal' onclick='editRow(" + count + ")'>" +
        "<i id=icon" + count + " class='material-icons icon-blue edit' data-toggle='tooltip' title='Save'>playlist_add_check</i></a>" +
        "<a href='#delete' class='delete' data-toggle='modal' onclick='deleteRow(" + count + ")'>" +
        "<i class='material-icons icon-blue' data-toggle='tooltip' title='Delete'>delete</i></a>" +
        "</td>" +
        "</tr>");
}