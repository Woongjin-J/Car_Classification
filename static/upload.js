function readURL(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#car')
              .attr('src', e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
  }
}

function identify(input) {
  alert(input[0]['tagName']);
}