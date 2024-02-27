from fcom.settings import env


def generate_order_id(paytm_transaction_amt, main_order, order_stage):
    ENV = env('ENV')
    order_prefix = env("PAYTM_ORDER_ID_PREFIX")
    
    order_prefix = order_prefix + "-" + order_stage + "-"
    
    if ENV == 'development':
        if paytm_transaction_amt.id:            
            paytm_transaction_amt.generated_order_id = order_prefix + f"{main_order.id:03}" + f"-{paytm_transaction_amt.id}"
        else:
            paytm_transaction_amt.generated_order_id = order_prefix + f"{main_order.id:03}"
            
    else:       
        # production env
        if paytm_transaction_amt.id:
            paytm_transaction_amt.generated_order_id = order_prefix + f"{main_order.id:03}" + f"-{paytm_transaction_amt.id}"
        else:
            paytm_transaction_amt.generated_order_id = order_prefix + f"{main_order.id:03}" 
            
    print(f"Generated Order Id: {paytm_transaction_amt.generated_order_id}")
    return paytm_transaction_amt
