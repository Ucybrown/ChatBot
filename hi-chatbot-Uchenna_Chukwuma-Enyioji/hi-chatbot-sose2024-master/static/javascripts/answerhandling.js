$(function() {
    $("#chatbot-form").submit(function(e){
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/ask",
            data: $(this).serialize(),
            success: function (response) {
                $('#textInput').val('');
                var answer = response.answer;
                console.log(response);
                var botHtml = '<p><span>' + answer + '</span></p>';
                $(".media-list").append(botHtml);
                $(".fixed-panel").stop().animate({
                    scrollTop: $(".fixed-panel")[0].scrollHeight
                }, 1000);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
})
