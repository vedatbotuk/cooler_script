# cooler_script

## Preparation
### GPIO Pins
With transistors.
```bash
PIN_STRONG_FAN = 21  # Pin, der zum Transistor fuehrt
PIN_LIGHT_FAN = 19
```

## Install
### Create, enable and start services
- Copy ```cooler_script.sevices``` file.
  ```bash
  cd home_remote
  sudo cp linux-services/cooler_script.service /etc/systemd/system/cooler_script.service
  ```
- Customize path to ```main.py``` and the ```WorkingDirectory```.
  ```bash
  sudo nano /etc/systemd/system/cooler_script.service
  ```
- Start and enable service.
  ```bash
  sudo systemctl enable cooler_script.service
  sudo systemctl start cooler_script.service
  ```
