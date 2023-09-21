# telegrambot_DMZstatuskey
Shows the status of the key to the DMZ room for our group in telegrams.

```
cp /etc/xdg/systemd/user/dmzbot@.service
systemctl --user daemon-reload    
systemctl --user restart dmzbot@1000.service
systemctl --user enable dmzbot@1000.service
```
