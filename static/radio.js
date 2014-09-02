;
function enter_now(element) {
  now = new Date();
  element.find("#id_time").val(now.getHours()+":"+now.getMinutes());
}
function enter_last(element, time) {
  element.find("#id_time").val(time);
}
