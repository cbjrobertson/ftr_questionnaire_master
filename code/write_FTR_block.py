import pandas as pd

#import questions
long = pd.read_excel('../ftr_questionnaire/questionnaire_long.xlsx')


##one time top of survey text
survey_format = '[[AdvancedFormat]]'
block_name = '[[Block: syntax_block_{}]]'

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
def format_question(question,lang,cert_perc,cert_word):
    pq = context
    cert_prime = False
    if cert_perc != -999:
        cert_prime = True
        cert_info = '{}% {}'.format(cert_perc,cert_word)
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
    pq += response[lang] + '\n\n'
    return pq  


##writes the questions by crossing the delay amounts with the dollar amounts
def write_FTR_questions(long):
    df = long.copy()
    dfg = df.groupby(['language'])
    for lang,dx in dfg:
        with open('../qualtrics_question_blocks/FTR_block_{}.txt'.format(lang),'w') as f:
            f.write(survey_format + '\n')
            f.write(block_name.format(lang) + '\n')
            for idx in dx.index:
                f.write(question_type +'\n')
                f.write(qid.format(dx.uneek[idx])+'\n')
                question = dx.question[idx]
                cert_word = dx.word[idx]
                cert_perc = dx.certainty[idx]
                pq = format_question(question,lang,cert_perc,cert_word)
                f.write(pq)

if __name__ == '__main__':
    write_FTR_questions(long)