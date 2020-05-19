import pandas as pd

#import questions
long = pd.read_excel('../ftr_questions/questionnaire_long.xlsx')

##one time top of survey text
survey_format = '[[AdvancedFormat]]'
block_name = '[[Block: FTR_question_block_{}]]'

##repeated question text
question_type = '[[Question:TE:SingleLine]]'
context = '<strong>CONTEXT:</strong><br />'
qid = '[[ID:uneek_{}]]'

target = {'dutch':'<strong>Doelzin: </strong><br />',
          'english': '<strong>Target sentence:</strong><br />'
          }

certainty = {'english':'<strong>Certainty information:</strong><br />',
             'dutch':'<strong>Zekerheidinformatie:</strong><br />'}

response = {'english':'<strong>Enter your response below:</strong>',
            'dutch':'<strong>Geef hieronder je reactie:</strong>'
            }

none = {'english':'None',
        'dutch':'Geen'}

trip_break = '<br />\n<br />\n<br />\n'

#functions
def format_question(question,lang):
    pq = context
    cert_prime = False
    if question.endswith(').'):
        cert_prime = True
        if ']' in question:
            target_sent = question[question.index(']'):]
        else:
            target_sent = question
        cert_info = target_sent[target_sent.index('('):]
        question = question.replace(cert_info,'').rstrip()+'.'
        cert_info = cert_info.strip('().')
    if question.startswith('['):
        pq += question.strip('[')[:question.index(']')-1]+trip_break
        if cert_prime:
            pq += certainty[lang] + '\n'
            pq += cert_info + trip_break
        pq += target[lang]+'\n'
        pq += question[question.index(']')+2:]+trip_break
    else:
        pq += none[lang]+trip_break
        if cert_prime:
            pq += certainty[lang] + '\n'
            pq += cert_info + trip_break
        pq += target[lang]+'\n'
        pq += question + trip_break
        print('WTF'+question)
    pq += response[lang] + '\n\n'
    return pq     


##writes the questions by crossing the delay amounts with the dollar amounts
def write_FTR_block(long,lim=None):
    df = long.copy()
    dfg = df.groupby(['language'])
    for lang,dx in dfg:
        if lim:
            count = 0
        with open('../qualtrics_question_block/FTR_block_{}.txt'.format(lang),'w') as f:
            f.write(survey_format + '\n')
            f.write(block_name.format(lang) + '\n')
            for idx in dx.index:
                if lim:
                    count += 1
                    if count > lim:
                        break
                f.write(question_type +'\n')
                f.write(qid.format(dx.uneek[idx])+'\n')
                question = dx.question[idx]
                pq = format_question(question,lang)
                f.write(pq)

if __name__ == '__main__':
    write_FTR_block(long)
