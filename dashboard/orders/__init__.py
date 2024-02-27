CARD_STAGES = {

    1: "Booking",
    2: "Consultation",
    3: "Estimations",
    4: "Order"  # once this stage reach switch it to order
}

ORDER_STAGES = {
    1: "In-Progress",
    2: "Complete",
    3: "Invoice Payment",
    4: "Out For Delivery",
    5: "Delivered"
}

# Here there are two stages of status one with the cart and other with the order
# cart stage will progress through - Booking, Consultation, Estimations, Order
# once Cart Stage reaches to Order then it will progress to -> In Progress -> Complete -> Invoice Generations -> Out for delivery -> Delivered

# Estimation has to be approved by the Customer to move to order status
# once order status is reached it will be in progress once user makes payment it will move to complete then generate invoice


#Stages
#cart   #order
# 1        1
# 2        1
# 3        1
# 4        2
# 4        3
# 4        4
# 4        5