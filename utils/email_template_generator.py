from constants.general import General


URL = General.LOCAL_URL if not General.RELEASE else General.REMOTE_URL


def generate_account_activation_template(verification_token: str, otp: str):

    template = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,300&display=swap" rel="stylesheet">
                <title>Activate account</title>
                <style>

                    *{
                        font-family: 'Nunito Sans', sans-serif;
                    }

                    .container{
                        max-width: 40%%;
                        margin-left: auto;
                        margin-right: auto;
                        margin-top: 10em;
                        border: 1px sold #ccc;
                        background: whitesmoke;
                        padding: 10px;
                        border-radius: 5px;
                    }

                    .container h1{
                        text-align: center;
                    }

                    .info-1{
                        font-size: 13px;
                    }

                    .activate-link{
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-decoration: none;
                        color: white;
                        background-color: #3742fa;
                        border-radius: 5px;
                        font-size: 12px;
                        margin-bottom: 200px;
                    }

                    small{
                        font-size: 10px;
                        text-align: center;
                        font-weight: 600;
                    }

                    .otp-container{
                        display: flex;
                        align-items: center;
                        gap: 20px;
                    }

                    .otp-container p{
                        font-size: 13px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Activate your Passit account</h1>
                    <p class="info-1">Tap the button below and use to code to confirm your email address. If you didn't create an account with <a
                        href="#">passit.io</a>, you can safely delete this email.</p>
                    <div class="otp-container">
                        <p>Use this code to activate your account</p><h3>%s</h3>
                    </div>
                    <a href="%s/activate/%s" class="activate-link" target="_blank">Activate account</a>
                    <p><small>You received this email because we received a request for activation for your account. If you didn't request activation
                    you can safely delete this email.</small></p>
                </div>
            </body>
            </html>

    """ %(otp, URL, verification_token) 
    return template


def generate_account_verification_template(verification_token: str, otp: str):

    template = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,300&display=swap" rel="stylesheet">
                <title>Verify account</title>
                <style>

                    *{
                        font-family: 'Nunito Sans', sans-serif;
                    }

                    .container{
                        max-width: 40%%;
                        margin-left: auto;
                        margin-right: auto;
                        margin-top: 10em;
                        border: 1px sold #ccc;
                        background: whitesmoke;
                        padding: 10px;
                        border-radius: 5px;
                    }

                    .container h1{
                        text-align: center;
                    }

                    .info-1{
                        font-size: 13px;
                    }

                    .activate-link{
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-decoration: none;
                        color: white;
                        background-color: #3742fa;
                        border-radius: 5px;
                        font-size: 12px;
                        margin-bottom: 200px;
                    }

                    small{
                        font-size: 10px;
                        text-align: center;
                        font-weight: 600;
                    }

                    .otp-container{
                        display: flex;
                        align-items: center;
                        gap: 20px;
                    }

                    .otp-container p{
                        font-size: 13px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Verify Account</h1>
                    <p class="info-1">Tap the button below and use to code to verify your account. If you didn't create an account with <a
                        href="#">passit.io</a>, you can safely delete this email.</p>
                    <div class="otp-container">
                        <p>Use this code to activate your account</p><h3>%s</h3>
                    </div>
                    <a href="%s/verify/%s" class="activate-link" target="_blank">Verify account</a>
                    <p><small>You received this email because we received a request for verification for your account. If you didn't request verification
                    you can safely delete this email.</small></p>
                </div>
            </body>
            </html>

    """ %(otp, URL, verification_token) 
    return template


def generate_forgot_password_template(token: str):

    template = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,300&display=swap" rel="stylesheet">
                <title>Forgot Password</title>
                <style>

                    *{
                        font-family: 'Nunito Sans', sans-serif;
                    }

                    .container{
                        max-width: 40%%;
                        margin-left: auto;
                        margin-right: auto;
                        margin-top: 10em;
                        border: 1px sold #ccc;
                        background: whitesmoke;
                        padding: 10px;
                        border-radius: 5px;
                    }

                    .container h1{
                        text-align: center;
                    }

                    .info-1{
                        font-size: 13px;
                    }

                    .activate-link{
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-decoration: none;
                        color: white;
                        background-color: #3742fa;
                        border-radius: 5px;
                        font-size: 12px;
                        margin-bottom: 200px;
                    }

                    small{
                        font-size: 10px;
                        text-align: center;
                        font-weight: 600;
                    }

                    .otp-container{
                        display: flex;
                        align-items: center;
                        gap: 20px;
                    }

                    .otp-container p{
                        font-size: 13px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Forgot Password</h1>
                    <p class="info-1">Tap the button below to change password for your account. If you didn't create an account with <a
                        href="#">passit.io</a>, you can safely delete this email.</p>
                    <a href="%s/reset/%s" class="activate-link" target="_blank">Change password</a>
                    <p><small>You received this email because we received a request for changing password to your account. If you didn't this request
                    you can safely delete this email.</small></p>
                </div>
            </body>
            </html>

    """ %(URL, token) 
    return template