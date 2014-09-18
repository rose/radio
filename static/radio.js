;
function enter_now(parent_elem) {
  now = new Date();
  parent_elem.find("#id_time").val(now.getHours()+":"+now.getMinutes()+":"+now.getSeconds());
}
function enter_last(parent_elem, time) {
  parent_elem.find("#id_time").val(time);
}
