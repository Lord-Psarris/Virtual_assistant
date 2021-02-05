import wolframalpha

app_id = ""
client = wolframalpha.Client(app_id)



def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']


def removeBrackets(variable):
    print(variable)
    return variable.split('(')[0]


def search(text=''):
    res = client.query(text)
    # Wolfram cannot resolve the question
    if res['@success'] == 'false':
        print('Question cannot be resolved')
    # Wolfram was able to resolve question
    else:
        result = ''
        # pod[0] is the question
        pod0 = res['pod'][0]
        # pod[1] may contains the answer
        pod1 = res['pod'][1]
        # checking if pod1 has primary=true or title=result|definition
        if (('definition' in pod1['@title'].lower()) or ('result' in pod1['@title'].lower()) or (
                pod1.get('@primary', 'false') == 'true')):
            # extracting result from pod1
            result = resolveListOrDict(pod1['subpod'])
            print(result)
            question = resolveListOrDict(pod0['subpod'])
            question = removeBrackets(question)
        else:
            # extracting wolfram question interpretation from pod0
            question = resolveListOrDict(pod0['subpod'])
            # removing unnecessary parenthesis
            question = removeBrackets(question)
            # searching for response from wikipedia


search('who is donald trump?')
