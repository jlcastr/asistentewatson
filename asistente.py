from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configurar el servicio del asistente.
authenticator = IAMAuthenticator('u4PvmIrnVTKwUpCYRi8ckgQUKuToVFDCa6OmAcaZ-SOv') # sustituir por clave de API
service = AssistantV2(
    version = '2019-02-28',
    authenticator = authenticator
)

assistant_id = '54de3c29-c479-4377-a080-91774a9f3f70' # sustituir por el ID de asistente

# Crear sesión.
session_id = service.create_session(
    assistant_id = assistant_id
).get_result()['session_id']

# Inicializar con un valor vacío para empezar la conversación.
message_input = {
    'message_type:': 'text',
    'text': ''
    }

# Main input/output loop
while message_input['text'] != 'quit':

    # Enviar mensaje al asistente.
    response = service.message(
        assistant_id,
        session_id,
        input = message_input
    ).get_result()

    # Si se detecta una intención, imprimirla en la consola.
    if response['output']['intents']:
        print('Detected intent: #' + response['output']['intents'][0]['intent'])

    # Imprimir la salida del diálogo, si hay. Solo se admite una única
    # respuesta de texto.
    if response['output']['generic']:
        if response['output']['generic'][0]['response_type'] == 'text':
            print(response['output']['generic'][0]['text'])

    # Solicitud para la siguiente ronda de entrada.
    user_input = input('>> ')
    message_input = {
        'text': user_input
    }

# Hemos terminado, así que suprimimos la sesión.
service.delete_session(
    assistant_id = assistant_id,
    session_id = session_id
)