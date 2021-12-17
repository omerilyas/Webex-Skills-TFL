from webex_skills.api import SimpleAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState

api = SimpleAPI()


@api.handle(pattern=r'.*\sline\s?.*')
async def turn_off(current_state: DialogueState) -> DialogueState:
    new_state = current_state.copy()
    text = new_state.text
    a = re.findall('.*?(\w*?)\sline\s?.*',text)[0]
    headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    'Content-type' : 'application/json'
            }
    url = f'https://api.tfl.gov.uk/Line/{a}/Status'
    req1 = requests.get(url= url , headers = headers).json()
    ser = req1[0]['lineStatuses'][0]['statusSeverityDescription']
    
    if ser == 'Severe Delays':
        ser = f"There are {ser} on {a} line"
    else:
        ser = f"There is a {ser} on {a} line"
    new_state.directives = [
        responses.Reply(ser),
        responses.Speak(ser),
        responses.Sleep(10)
    ]
    return new_state