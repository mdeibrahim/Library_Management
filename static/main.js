console.log("Sanity check!");


fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  
   let submitBtn = document.querySelector("#submitBtn");
  if (submitBtn !== null) {
    submitBtn.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }
  
});


