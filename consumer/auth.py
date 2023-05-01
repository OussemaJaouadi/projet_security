import kerberos

def getTicket():
	headers = ""
	try:
		_, krb_context = kerberos.authGSSClientInit("host@server.projet.tn")
		#print("step : "+str(kerberos.authGSSClientStep(krb_context, "")))
		kerberos.authGSSClient(krb_context,"")
		#print("Creating auth header......")
		negotiate_details = kerberos.authGSSClientResponse(krb_context)
		headers = {"Authorization": "Negotiate "+ negotiate_details}
	except Exception as err:
		headers = ""
	return headers