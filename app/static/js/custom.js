

$(document).ready(function() {
    $("#avatar").click(function() {
        $("input[id='my_file']").click();
    });
    
    var readURL = function(input) {
        if (input.files && input.files[0]) {
            new Promise(function(resolve, reject) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#avatar').attr('src', e.target.result);
                resolve(e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
            reader.onerror = reject;
            })
            .then(processFileContent)
            .catch(function(err) {
            console.log(err)
            });
        }
    }

    function processFileContent(data) {
        var list = data.split('\n');
        $('#image').val(list);
    }
    

    $("#my_file").on('change', function(){
        readURL(this);
    });

    $('select').selectpicker();

});