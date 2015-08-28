$(function() {
    $('.google-map').each(function() {
        var $this = $(this);
        GoogleMapsLoader.load(function(google) {
            new google.maps.Map($this[0], {center: new google.maps.LatLng($this.data('longitude'), $this.data('latitude')), zoom: $this.data('zoom'), disableDefaultUI: true, disableDoubleClickZoom: true, draggable: false, keyboardShortcuts: false, zoomControl: false});
        });
    });
});