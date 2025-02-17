$(document).ready(function () {
    // Получаем CSRF-токен из meta
    let csrfToken = $('meta[name="csrf-token"]').attr('content');

    // Настроим глобальный обработчик CSRF-токена для всех AJAX-запросов
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfToken  // Передаем CSRF-токен в заголовке
            //'Content-Type': 'application/json',
        }
    });

    $("#mailingForm").submit(async function (e) {
        e.preventDefault()

        await $.ajax({
            url: "/mailings/",
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                refreshMailing();
                alert("Рассылка создана!");
                $("#mailingModal").modal('hide');
                $("#mailingForm")[0].reset();
            },
            error: function (xhr, status, error) {
                if (xhr.status === 403) {
                alert('Токен CSRF устарел! Пожалуйста, перезагрузите страницу.');
                }else if (xhr.status === 400) {
                    // Извлекаем ошибку из JSON-ответа
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            alert("Ошибка: " + response.error);
                        }
                    } catch (e) {
                        console.log("Ошибка при обработке ответа: " + e);
                    }
                }
            }
        });
    });

    $("#subscriberForm").submit(function (e) {
        e.preventDefault()

        $.ajax({
            url: "/subscribers/",
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                refreshSubscribers();
                alert("Полписчик создан!");
                $("#subscriberModal").modal('hide');
                $("#subscriberForm")[0].reset();
            },
            error: function (xhr, status, error) {
                if (xhr.status === 403) {
                alert('Токен CSRF устарел! Пожалуйста, перезагрузите страницу.');
                }else if (xhr.status === 400) {
                    // Извлекаем ошибку из JSON-ответа
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            alert("Ошибка: " + response.error);
                        }
                    } catch (e) {
                        console.log("Ошибка при обработке ответа: " + e);
                    }
                }
                console.log("Ошибка:", error);
            }
        });
    });


});
async function refreshMailing(){
    await $.ajax({
        url: "/mailings/",
        type: "GET",
        data: { act: "ajax" },
        success: function (response) {
            $("#mailingTable").html(response.html);
            $("#mailingForm")[0].reset();

        },
        error: function (xhr, status, error) {
            if (xhr.status === 403) {
            alert('Токен CSRF устарел! Пожалуйста, перезагрузите страницу.');
            }
            else if (xhr.status === 400) {
                    // Извлекаем ошибку из JSON-ответа
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            alert("Ошибка: " + response.error);
                        }
                    } catch (e) {
                        console.log("Ошибка при обработке ответа: " + e);
                    }
                }
        }
    });
}

async function refreshSubscribers(){
    await $.ajax({
        url: "/subscribers/",
        type: "GET",
        data: { act: "ajax" },
        success: function (response) {
            $("#subscriberTable").html(response.html);
            $("#subscriberForm")[0].reset();

        },
        error: function (xhr, status, error) {
            if (xhr.status === 403) {
            alert('Токен CSRF устарел! Пожалуйста, перезагрузите страницу.');
            }
            else if (xhr.status === 400) {
                    // Извлекаем ошибку из JSON-ответа
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            alert("Ошибка: " + response.error);
                        }
                    } catch (e) {
                        console.log("Ошибка при обработке ответа: " + e);
                    }
                }
        }
    });
}