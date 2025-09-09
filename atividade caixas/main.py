from machine import Pin, time_pulse_us
import time

# --- Configuração dos Pinos ---
PINO_TRIG = 25
PINO_ECHO = 27
PINO_LED_INTRUSO = 26

trig = Pin(PINO_TRIG, Pin.OUT)
echo = Pin(PINO_ECHO, Pin.IN)
led_intruso = Pin(PINO_LED_INTRUSO, Pin.OUT)

# --- Variáveis de Contagem ---
contador_itens = 0
contador_caixas = 0
distancia_limite = 10  # Distância em cm para detecção do objeto
detectar_ativo = False  # Variável para evitar contagem múltipla do mesmo item

# --- Função de Medição de Distância ---
def obter_distancia():
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duracao = time_pulse_us(echo, 1, 30000)
    if duracao < 0:  # Nenhum pulso detectado
        return 1000  # Valor alto para ignorar
    distancia = (duracao / 2) * 0.0343
    return distancia

# --- Loop Principal ---
while True:
    dist = obter_distancia()
    print("Distância:", dist, "cm")

    if dist <= distancia_limite:
        led_intruso.value(1)  # Acende o LED

        if not detectar_ativo:
            contador_itens += 1
            detectar_ativo = True
            print("Item detectado! Total de itens:", contador_itens)

            # Verifica se atingiu 10 itens
            if contador_itens >= 10:
                contador_caixas += 1
                contador_itens = 0  # Zera o contador de itens
                print("Caixa completa! Total de caixas:", contador_caixas)

        time.sleep(1)  # Delay para evitar múltiplas leituras do mesmo item

    else:
        led_intruso.value(0)  # Apaga o LED
        detectar_ativo = False  # Permite detectar o próximo item

    time.sleep(0.5)
