/**
 * @description
 * This file need to replace with passport.mobile.js while testing with native app
 */

function selectEmail() {
    if (window.webkit != undefined) {
        if (window.webkit.messageHandlers.receiveMessageFromJS != undefined) {
            webkit.messageHandlers.receiveMessageFromJS.postMessage(
                "openEmailSelection"
            );
        }
    } else if (myJSHandler.receiveMessageFromJS != undefined) {
        myJSHandler.receiveMessageFromJS("openEmailSelection", "");
    }
}

function selectAddress() {
    if (window.webkit != undefined) {
        if (window.webkit.messageHandlers.receiveMessageFromJS != undefined) {
            webkit.messageHandlers.receiveMessageFromJS.postMessage(
                "openAddressSelection"
            );
        }
    } else if (myJSHandler.receiveMessageFromJS != undefined) {
        myJSHandler.receiveMessageFromJS("openAddressSelection", "");
    }
}

function selectPhone() {
    if (window.webkit != undefined) {
        if (window.webkit.messageHandlers.receiveMessageFromJS != undefined) {
            webkit.messageHandlers.receiveMessageFromJS.postMessage(
                "openPhoneSelection"
            );
        }
    } else if (myJSHandler.receiveMessageFromJS != undefined) {
        myJSHandler.receiveMessageFromJS("openPhoneSelection", "");
    }
}

function readQRCode() {
    if (window.webkit != undefined) {
        if (window.webkit.messageHandlers.receiveMessageFromJS != undefined) {
            webkit.messageHandlers.receiveMessageFromJS.postMessage(
                "openQRCodeReader"
            );
        }
    } else if (myJSHandler.receiveMessageFromJS != undefined) {
        myJSHandler.receiveMessageFromJS("openQRCodeReader", "");
    }
}

function startPayment(paymentToken) {
    if (window.webkit != undefined) {
        if (window.webkit.messageHandlers.receiveMessageFromJS != undefined) {
            webkit.messageHandlers.receiveMessageFromJS.postMessage({
                trx: "startPayment",
                paymentToken: paymentToken,
            });
        }
    } else if (myJSHandler.receiveMessageFromJS != undefined) {
        myJSHandler.receiveMessageFromJS("startPayment", paymentToken);
    }
}

function orderCompleted() {
    if (window.webkit != undefined) {
        if (window.webkit.messageHandlers.receiveMessageFromJS != undefined) {
            webkit.messageHandlers.receiveMessageFromJS.postMessage(
                "completePayment"
            );
        }
    } else if (myJSHandler.receiveMessageFromJS != undefined) {
        myJSHandler.receiveMessageFromJS("completePayment", "");
    }
}