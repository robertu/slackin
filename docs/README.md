# Konfiguracja slack bota

### Zakładasz nową aplikację

Klik na url: [slack new_app](https://api.slack.com/apps?new_app=1)
![01. Create a slack app](01-create-a-slack-app.png)

### Dodaj bot usera

![02. add bot](02-add-bot-user.png)

### Nazwania i zaproszenie bota

Następnie nazywamy naszego bota oraz dodajemy go na serwer

![03. invite bot](03-name-and-invite-bot.png)

### Aktywacja funkcji bota

Następnie wchodzimy w zakładkę " Interactive Components " i przełanczamy z "off" na "on"

![04. enable componets](04-enabling-c.png)

### Podpięcie bota do serwera http

Następnie podajemy "Request URL" np. https://<Nasza domena>/slack/message_actions
I zapisujemy zmiany

![05. requst url](05-add-rp-url.png)

### Uprawnienia bota

W tym momencie w zakładce OAuth w sekcji "scopes" nadajemy mu permise 'admin' i klikamy "save changes"

![06. add admin](06-admin-add.png)

### Instalacja aplikacji na serwerze slacka

Natępnie instaluje go na swoim serwerze

![07. add to server](07-add-to-server.png)

### Redirect URL

Potem w zakładce  "OAuth Tokens & Redirect URLs" dodajemy redirect URLs np. https://example.com/path

![08. add url](08-url-addd.png)

### Publikowanie bota

Następnie w "Manage Distribution" zaznaczamy "I’ve reviewed and removed any hard-coded information" i publikujemy bota:
![09. publish bot](09-publish-bot.png)


Teraz zmieniamy:

### Token

![10. bot token](10-bot-token.png)
To jest nasz token "Bot User OAuth Access Token"

### Klucz

A to jest nasz klucz "Signing Secret":
![11. kluc](11-klucz.png)


```
slack_event_listen = SlackEventAdapter(signing_secret='Nasz klucz', endpoint="/slack/events", server=app)
token = 'Nasz token'
```


Teraz muszimy przypisać w kodzie te dwie wartości

Następnie uruchamiamy kod bota "python event.py" albo "./event.py"

Następnie w zakładce 'Event Subscriptions' włączamy eventy i podajemy następujący ades "https://<Nasz domena>/slack/events

![12. event](12-event-url.png)

Dodatkowo można nadać mu uprawnienia admina, poniżej załączam ofcjialną dokumnetacja aplikacji na slacku:
[sack bot tut](https://github.com/slackapi/python-slackclient/tree/master/tutorial)