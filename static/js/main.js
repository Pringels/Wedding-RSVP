
$( document ).ready(function() {

    $('.search-song').on('input', function(){

        var value = $(this).val();

        if ($('.search-results').html() == ''){
            $('.search-loader').addClass('active');
        }

        if (value == ''){
            $('.search-results').html('');
            return;
        }

        $.ajax({
         type: "GET",
         url: "/song-search/",
         data: { title: value}
       })
         .done(function(data) {

             if ($('.search-song').val() == ''){
                 $('.search-results').html('');
                 return;
             }

            $('.search-loader').removeClass('active');
            data = JSON.parse(data);

            var list = '<ul>';
            for (var key in data){
                list += '<li><button class="add-song" data-title="' + key + '" data-name="' + data[key] + '">Add</button>' + data[key] + '</li>';
            }
            list += '</ul>';
           $('.search-results').html(list);
        });
    });

    $(document).on('click', '.add-song', function(){

        var ref = $('.invite-ref').data('ref');
        var songName = $(this).data('name');

        $.ajax({
         type: "GET",
         url: "/add-song/",
         data: { title: $(this).data('title'), ref: ref, name: songName}
       })
         .done(function(msg) {
             var str = '<h3>Song added!</h3>';
             str += '<h1>' + songName + '</h1>';
            $('.song-select').html(str);
        });
    });

});
