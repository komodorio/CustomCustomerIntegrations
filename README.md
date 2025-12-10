# Launch Darkly Event Puller
The repo contains public facing integrations and implementations. 

#ReadMe This function ingests a Launch Darkly notification via webhook, translates it into readable fashion by Komodor and sends it to the Komodor Events tab
#Requirements: Create a lambda with the below functions
#Create a lambda function URL to give to Launch Darkly https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html#create-url-console
#Feed that to Launch Darkly to send a webhook to it when events trigger
#Insert your own Komodor API key as a value on line 14 or as a value from vault or other source
