// TODO: create factory function for markers

const createMarker = ({ id, latlng, draggable=true }) => ({
  id,
  latlng,
  draggable,
  getId() {
    return this.id;
  }
  setId(id) {
      this.id = id;
  }
  toggleDraggable() {
      this.draggable = !this.draggable;
  }
});
