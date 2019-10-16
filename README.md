# Konfiguracja slack bota

### Przykładowy plik konfiguracyjny

```
[BOT]
token = xoxb-()
signing_secret = Klucz 16-stkowy
url = https://nasza_domena
port = 4002
host = 0.0.0.0
debug_mode = false
name = examplebot
```

### Zakładasz nową aplikację

Klik na url: [slack new_app](https://api.slack.com/apps?new_app=1)
![01. Create a slack app](docs/01-create-a-slack-app.png)

### Dodaj bot usera

![02. add bot](docs/02-add-bot-user.png)

### Nazwania i zaproszenie bota

Następnie nazywamy naszego bota oraz dodajemy go na serwer

![03. invite bot](docs/03-name-and-invite-bot.png)

### Aktywacja funkcji bota

Następnie wchodzimy w zakładkę " Interactive Components " i przełanczamy z "off" na "on"

![04. enable componets](docs/04-enabling-c.png)

### Podpięcie bota do serwera http

Następnie podajemy "Request URL" np. https://Nasza_domena/slack/message_actions
I zapisujemy zmiany
Aby to wykonać należy włączyć skrypt bota

![05. requst url](docs/05-add-rp-url.png)

### Uprawnienia bota

W tym momencie w zakładce OAuth w sekcji "scopes" nadajemy mu permise 'admin' i klikamy "save changes"

![06. add admin](docs/06-admin-add.png)

### Instalacja aplikacji na serwerze slacka

Natępnie instaluje go na swoim serwerze

![07. add to server](docs/07-add-to-server.png)

### Redirect URL

Potem w zakładce  "OAuth Tokens & Redirect URLs" dodajemy redirect URLs np. https://example.com/path
Jest to strona która pojawi się gdy zainstalujemy bota.

![08. add url](docs/08-url-addd.png)

### Publikowanie bota

Następnie w "Manage Distribution" zaznaczamy "I’ve reviewed and removed any hard-coded information" i publikujemy bota:
![09. publish bot](docs/09-publish-bot.png)




Następnie w zakładce 'Event Subscriptions' włączamy eventy i podajemy następujący ades "https://Nasz_domena/slack/events

![10. event](docs/12-event-url.png)

Aby to zadziałało trzeba mieć uruchiomony skrypt bota
Po właczeniu eventów należy dodać:
w "Subscribe to Bot Event" oraz "Subscribe to Workspace Events" nastepujące eventy

 * message.im
 * message.channels
 * group_history_changed

Dodatkowo należy nadać mu uprawnienia admina oraz message.channels , poniżej załączam ofcjialną dokumnetacja aplikacji na slacku:
[sack bot tut](https://github.com/slackapi/python-slackclient/tree/master/tutorial)