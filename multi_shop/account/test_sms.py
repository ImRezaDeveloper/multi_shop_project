import gh

sms_api = ghasedak_sms.Ghasedak(apikey='7970555b045c815109d105e824fd44c9efe1816ee8796d2f115ad21a7e462e4aLrEff7ubDppbNXfU')

response = sms_api.send_single_sms(
    ghasedak_sms.SendSingleSmsInput(
        message='hello, world!',
        receptor='09939611789',
        line_number='09939611789',
        send_date='',
        client_reference_id=''
    )
)

print(response)
