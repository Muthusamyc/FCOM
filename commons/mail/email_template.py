
def signup_content(otp):     
    html = f'''
        <html>
            <body>
                <h3>Dear customer, use {otp} as OTP for FcomIndia registration.</h3>
              
                <br><br>
                Yours sincerely<br>
                Team FCOM India,<br>
                +91 910890-2222
            </body>
        </html>
        '''
    return html 


def login_content(customer_name, otp):     
    html = f'''
        <html>
            <body>
                <h3>Dear { customer_name },</h3>
                Dear {customer_name}, use {otp} as OTP for FcomIndia Login
                <br><br>
                Yours sincerely<br>
                Team FCOM India,<br>
                +91 910890-2222
            </body>
        </html>
        '''
    return html 





def consultation_content(customer_name, consultation_date):     
    html = f'''
        <html>
            <body>
                <h3>Dear { customer_name },</h3>
                Thanks for choosing <span style="color:#f28077">FCOM India</span>- your doorstep tailors!.
                <br><br>
                Our representative will be visiting  you on <b>{ consultation_date }</b>. 
                Please ensure you are available at the address given while registering.
                <br><br>
                Feel free to call us if you would like to reschedule the visit/consultation date before 48hrs.
                <br><br>
                Yours sincerely<br>
                Team FCOM India,<br>
                +91 910890-2222
            </body>
        </html>
        '''
    return html 



def waiting_for_approval_content(customer_name, order_id):     
    html = f'''
        <html>
            <body>
                <h3>Dear { customer_name },</h3>
                <span style="color:#f28077">FCOM India</span> believes in giving you the best experience!
                <br><br>
                Our representative has received the order, discussed the order details and worked on the estimate. 
                Please approve the same for us to start working. Your order number is  <a href="https://fcomindia.com/bookings/order-history/{order_id}">{order_id}</a>.
                <br><br>
                Only after the approval, we will start executing the order.
                <br><br>
                Feel free to call us may you have any queries.
                <br><br>
                Yours sincerely<br>
                Team FCOM India,<br>
                +91 910890-2222
            </body>
        </html>
        '''
    return html 

def ready_for_dispatch_content(customer_name, order_id, delivery_date):     
    html = f'''
        <html>
            <body>
                <h3>Dear { customer_name },</h3>
                <span style="color:#f28077">FCOM India</span> believes in giving you the best experience!
                <br><br>
                Your order number is <a href="https://fcomindia.com/bookings/order-history/{order_id}">{order_id}</a>.
                is complete and ready for dispatch on <b>{delivery_date}</b>. Request you to make the full payement.
                <br><br>
                Feel free to call us may you have any queries.
                <br><br>
                Yours sincerely<br>
                Team FCOM India,<br>
                +91 910890-2222
            </body>
        </html>
        '''
    return html 

def dispatched_content(customer_name, order_id):     
    html = f'''
        <html>
            <body>
                <h3>Dear { customer_name },</h3>
                <span style="color:#f28077">FCOM India</span> believes in giving you the best experience!
                <br><br>
                Your order number is <a href="https://fcomindia.com/bookings/order-history/{order_id}">{order_id}</a> dispatched. 
                Please leave your feedback once received.
                <br><br>
                Feel free to call us.
                <br><br>
                Yours sincerely<br>
                Team FCOM India,<br>
                +91 910890-2222
            </body>
        </html>
        '''
    return html 
