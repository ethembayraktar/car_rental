window.addEventListener(
  "message",
  function (e) {
    if (typeof window[e.data] == "function") {
      window[e.data].call();
    }
  },
  false
);

/**
 * @description
 * Triggers merchant application after email selection is completed
 */
function emailSelected() {
  console.log("Email selected.");
  document.getElementById('mailInformationBtn').classList.add('selected');

  setTimeout(getParameters, 300);

}

/**
 * @description
 * Triggers merchant application after address selection is completed
 */
function addressSelected() {
  console.log("Address selected.");
  document.getElementById('addressInformationBtn').classList.add('selected');

  setTimeout(getParameters, 300);

}

/**
 * @description
 * Triggers merchant application after phone number selection is completed
 */
function phoneNoSelected() {
  console.log("Phone no selected.");
  document.getElementById('phoneInformationBtn').classList.add('selected');

  setTimeout(getParameters, 300);

}

/**
 * @description
 * Triggers merchant application after qr code reading operation is completed
 */
function qrCodeRead() {
  console.log("QR code read.");
}

/**
 * @description
 * Triggers merchant application after payment operation is completed
 */
function paymentCompleted() {
  console.log("Payment completed.");
  reconcileProcessIgnition();
}