// TODO: create factory function for markers
//
// const createMarker = ({ id, latlng, draggable=true }) => ({
//   id,
//   latlng,
//   draggable,
//   getId() {
//     return this.id;
//   }
//   setId(id) {
//       this.id = id;
//   }
//   toggleDraggable() {
//       this.draggable = !this.draggable;
//   }
// });

function sendMarkerCreateRequest(lat, lng, title="") {
    $.post($SCRIPT_ROOT + '/create_marker_request', {title: title, lat: lat, lng: lng},
        function(response) {
            console.log(response);
    });
}

function sendMarkerDeleteRequest(lat, lng) {
    $.post($SCRIPT_ROOT + '/delete_marker_request', {lat: lat, lng: lng},
        function(response) {
            console.log(response);
    });
}
