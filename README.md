# telegrambot_DMZstatuskey
Shows the status of the key to the DMZ room for our group in telegrams.
install:
```sh
yay -S python-pytelegrambotapi
```
and copy:
```sh
cp dmsbot@.service /etc/systemd/user/
systemctl daemon-reload --user
```
