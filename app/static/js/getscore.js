<script>
     document.getElementsByName('radio').forEach(function(radio) {
          radio.addEventListener('change', function() {
               if (this.checked) {
                    console.log(this.value);
               }
          })
     })
</script>