class BookingStage:
    ORDER_BOOKED = 1
    ORDER_UPDATED = 2
    APPROVAL_ACCEPTED = 3
    APPROVAL_REJECTED = 4
    ESTIMATED_PAYMENT = 5
    ESTIMATED_PAYMENT_PAID = 6
    ORDER_IN_PROGRESS = 7
    ORDER_SHIPPED = 8
    ORDER_DELIVERED = 9
    ORDER_CANCELED = 10
    REFUND_INITIATED = 11
    REFUND_PENDING = 12
    REFUND_COMPLETED = 13
    ORDER_FAILED = 14
    ORDER_INITIATED = 15
    CART_CREATED = 16
    ORDER_ASSINGED = 17
    BALANCE_AMOUNT_PAID = 18
    ORDER_PICKEDUP = 19
    ORDER_CONSULTED = 20
    WAIT_FOR_APPROVAL = 21
    READY_FOR_DISPATCH = 22
    ORDER_DISPATCHED = 23
    ORDER_CANCELED_READY_FOR_DISPATCH = 24
    ORDER_CANCELED_DISPATCHED = 25
    ORDER_CANCELED_DELIVERED = 26
    

STAGES = {
    BookingStage.ORDER_BOOKED : "Order Booked",
    BookingStage.ORDER_UPDATED : "Order Updated",
    BookingStage.ORDER_FAILED : "Failed",
    BookingStage.ORDER_INITIATED : "Initiated",
    BookingStage.ORDER_CANCELED : "Order Canceled",
    BookingStage.APPROVAL_ACCEPTED : "Estimation Approved",
    BookingStage.APPROVAL_REJECTED: "Estimation Rejected",
    BookingStage.ESTIMATED_PAYMENT_PAID : "Estimation Paid",
    BookingStage.ORDER_ASSINGED : "Order Assigned",
    BookingStage.BALANCE_AMOUNT_PAID : 'Payment Completed',  
    BookingStage.ORDER_IN_PROGRESS : 'In progress',
    BookingStage.ORDER_PICKEDUP : 'Picked Up',
    BookingStage.ORDER_DELIVERED : 'Delivered',
    BookingStage.ORDER_CONSULTED : 'Visit / Consultation',
    BookingStage.WAIT_FOR_APPROVAL : 'Approval Pending',
    BookingStage.READY_FOR_DISPATCH : 'Ready for Dispatch',
    BookingStage.ORDER_DISPATCHED : 'Dispatched',
    BookingStage.REFUND_INITIATED : 'Refund Initiated',
    BookingStage.REFUND_COMPLETED : 'Refund Completed',
    BookingStage.ORDER_CANCELED_READY_FOR_DISPATCH : 'Canceled Order Ready for Dispatch',
    BookingStage.ORDER_CANCELED_DISPATCHED : 'Canceled Order Dispatched',
    BookingStage.ORDER_CANCELED_DELIVERED : 'Canceled Order Delivered',
}

BOOKING_STAGES_FOR_USER = {
    BookingStage.ORDER_BOOKED : "Order Booked",
    BookingStage.ORDER_CANCELED : "Order Canceled",
    BookingStage.APPROVAL_ACCEPTED : "Order Approved",
    BookingStage.ORDER_IN_PROGRESS : 'In progress',
    BookingStage.ORDER_DELIVERED : 'Delivered',
}



STAGE_GROUP = {
    "ORDER_BOOKED" : BookingStage.ORDER_BOOKED ,
    "ORDER_UPDATED" : BookingStage.ORDER_UPDATED,
    "ORDER_FAILED" :  BookingStage.ORDER_FAILED,
    "ORDER_INITIATED" : BookingStage.ORDER_INITIATED,
    "ORDER_CANCELED" : BookingStage.ORDER_CANCELED,
    "APPROVAL_ACCEPTED" : BookingStage.APPROVAL_ACCEPTED,
    "APPROVAL_REJECTED" : BookingStage.APPROVAL_REJECTED,
    "ESTIMATED_PAYMENT_PAID" : BookingStage.ESTIMATED_PAYMENT_PAID,
    "ORDER_ASSINGED" : BookingStage.ORDER_ASSINGED,
    'BALANCE_AMOUNT_PAID' : BookingStage.BALANCE_AMOUNT_PAID,
    'ORDER_PICKEDUP' : BookingStage.ORDER_PICKEDUP,
    'ORDER_DELIVERED' : BookingStage.ORDER_DELIVERED,
    'ORDER_CONSULTED' : BookingStage.ORDER_CONSULTED,
    'ORDER_IN_PROGRESS' : BookingStage.ORDER_IN_PROGRESS,
    'WAIT_FOR_APPROVAL' : BookingStage.WAIT_FOR_APPROVAL,
    'READY_FOR_DISPATCH' : BookingStage.READY_FOR_DISPATCH,
    'ORDER_DISPATCHED' : BookingStage.ORDER_DISPATCHED,
    'REFUND_INITIATED' : BookingStage.REFUND_INITIATED,
    'REFUND_COMPLETED' : BookingStage.REFUND_COMPLETED,
    'ORDER_CANCELED_READY_FOR_DISPATCH' : BookingStage.ORDER_CANCELED_READY_FOR_DISPATCH,
    'ORDER_CANCELED_DISPATCHED' : BookingStage.ORDER_CANCELED_DISPATCHED ,
    'ORDER_CANCELED_DELIVERED':    BookingStage.ORDER_CANCELED_DELIVERED,

}