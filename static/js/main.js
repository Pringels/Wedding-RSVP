
console.log("Dont mess with my site please Werner? Same goes for you Chris :P");



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
                list += '<li class="add-song"><button data-title="' + key + '" data-name="' + data[key] + '"></button><p>' + data[key] + '</p></li>';
            }
            list += '</ul>';
           $('.search-results').html(list);
        });
    });

    $(document).on('click', '.add-song', function(){

        var ref = $('.invite-ref').data('ref');
        var $this = $(this).find('button');
        var songName = $this.data('name');

        $.ajax({
         type: "GET",
         url: "/add-song/",
         data: { title: $this.data('title'), ref: ref, name: songName}
       })
         .done(function(msg) {
             var str = '<div class="col-lg-12 detail">';
             str += '<br/>';
              str += '<h2>Your song dedication to us</h2>';
             str += '<h1 class="track-name">' + songName + '</h1>';
            $('.song-select').html(str);
        });
    });

});
