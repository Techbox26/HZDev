$(function() {
      $('#btnSignUp').click(function() {

          $.ajax({
              url: '/signUp',
              data: $('form').serialize(),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              type: 'POST',
              success: function(response) {
                  console.log(response);
              },
              error: function(error) {
                  console.log(error);
              }
          });
      });
  });

$(function() {
      $('#btnAddAssign').click(function() {

          $.ajax({
              url: '/tabletests2',
              data: $('form').serialize(),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              type: 'POST',
              success: function(response) {
                  console.log(response);
              },
              error: function(error) {
                  console.log(error);
              }
          });
      });
  });










<script type="text/javascript">
    $(document).ready(function () {
        $("#sidebar").mCustomScrollbar({
            theme: "minimal"
        });

        $('#dismiss, .overlay').on('click', function () {
            // hide sidebar
            $('#sidebar').removeClass('active');
            // hide overlay
            $('.overlay').removeClass('active');
        });

        $('#sidebarCollapse').on('click', function () {
            // open sidebar
            $('#sidebar').addClass('active');
            // fade in the overlay
            $('.overlay').addClass('active');
            $('.collapse.in').toggleClass('in');
            $('a[aria-expanded=true]').attr('aria-expanded', 'false');
        });
    });
</script>