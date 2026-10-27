from time import sleep
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()

class LoRaTransmitter(LoRa):
    def __init__(self, verbose=False):
        super(LoRaTransmitter, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def send(self, message):
        print(f"Transmitting: {message}")
        self.set_mode(MODE.STDBY)
        self.write_payload([ord(c) for c in message])
        self.set_mode(MODE.TX)
        while self.get_irq_flags()['tx_done'] == 0:
            sleep(0.1)  # Wait until transmission is done
        self.clear_irq_flags(TxDone=1)
        print("Message sent!")
        self.set_mode(MODE.SLEEP)

lora = LoRaTransmitter(verbose=False)
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)

try:
    while True:
        lora.send("Hello LoRa!")
        sleep(5)  # Wait 5 seconds before sending next message
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nTransmission stopped by user.")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
