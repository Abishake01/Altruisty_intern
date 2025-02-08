import { initDialog } from "/static/js/calender/dialog.js";

export function initMobileSidebar() {
  const dialog = initDialog("mobile-sidebar");

  document.addEventListener("mobile-sidebar-open-request", () => {
    dialog.open();
  });

  document.addEventListener("date-change", () => {
    dialog.close();
  });
}