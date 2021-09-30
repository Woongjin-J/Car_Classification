// Takes in the input object and return the image path back to the img tag with
// an id equaled to car in local_file.html
function display(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#car')
              .attr('src', e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
  }
}
