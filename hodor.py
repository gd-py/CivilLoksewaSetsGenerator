def name_rank(name, score1):
    count=list(score1.values())
    percent=(count.index(score1[name])+1)/len(count)
    return percent

def score(ans, name, score1):
    score=0    
    if len(ans)<140 and len(ans)>100:
        score=score+3
    elif len(ans)>140 and len(ans)<200:
        score=score+2
    elif len(ans)>200 and len(ans)<250:
        score=score+1
    elif len(ans)>250 and len(ans)<500:
        score=score-1
    elif len(ans)>500:
        score=score-10
    if ans.find('?')!=-1:
        score=score-10
    if ans.lower().find('@')!=-1:
        score=score-10
    if ans.lower().find('perhaps')!=-1:
        score=score-10
    if ans.lower().find('maybe')!=-1:
        score=score-10
    if ans.lower().find('presumably')!=-1:
        score=score-10
    if ans.lower().find('reportedly')!=-1:
        score=score-10
    if ans.lower().find('rumor')!=-1:
        score=score-10
    if ans.lower().find('legend has it that')!=-1:
        score=score-10
    if ans.lower().find('word has it that')!=-1:
        score=score-10
    if ans.lower().find('depends')!=-1:
        score=score-10
    if ans.lower().find("not that i'm aware of")!=-1:
        score=score-10
    if ans.lower().find('i dare say')!=-1:
        score=score-10
    if ans.lower().find('rumor')!=-1:
        score=score-10
    if ans.lower().find('think')!=-1:
        score=score-10
    if ans.lower().find('imagine')!=-1:
        score=score-10
    if ans.lower().find('hope')!=-1:
        score=score-10
    if ans.lower().find('to my knowledge')!=-1:
        score=score-10
    if ans.lower().find('to the best of my knowledge')!=-1:
        score=score-10
    if ans.lower().find('to the best of my belief')!=-1:
        score=score-10
    if ans.lower().find('you never can tell')!=-1:
        score=score-10
    if ans.lower().find('certain')!=-1:
        score=score+1
    if ans.lower().find('sure')!=-1:
        score=score+1
    if ans.lower().find('positive')!=-1:
        score=score+1
    if ans.lower().find('definite')!=-1:
        score=score+1
    if ans.lower().find('confident')!=-1:
        score=score+1
    if ans.lower().find('convinced')!=-1:
        score=score+1
    if ans.lower().find('for example')!=-1:
        score=score+3
    if ans.lower().find('@')!=-1:
        score=score-3
    if ans.lower().find('satisfied')!=-1:
        score=score+1
    if ans.lower().find('dogmatic')!=-1:
        score=score+1
    if ans.lower().find('assured')!=-1:
        score=score+1
    if ans.lower().find('decidedly')!=-1:
        score=score+1
    if ans.lower().find('positively')!=-1:
        score=score+1
    if len(ans)<100:
        score=score-10
    if ans.lower().find('question')!=-1:
        score=score-10
    if ans.lower().find('answer')!=-1:
        score=score-10
    if ans.lower().find('please')!=-1:
        score=score-10
    if ans.lower().find('help')!=-1:
        score=score-10
    if ans.lower().find('thank')!=-1:
        score=score-10
    if ans.lower().find('fuck')!=-1:
        score=score-10
    if ans.lower().find('might')!=-1:
        score=score-1
    if ans.lower().find('chod')!=-1:
        score=score-10
    return score*name_rank(name, score1)
    
file_main=open('quens_coll.txt','r', encoding='utf-8')
file_main_txt=file_main.read()
file_main.close()
main_list=[]
main_file=file_main_txt.split('\n\n\n\n')
for i in range(0,len(main_file)):
    a = main_file[i].split('\n\t')
    qn = [a[0]]
    discuss = [x.split(', ', 2) for x in a[1:]]
    discuss.insert(0, qn)
    main_list.append(discuss)

question_list=[]
answers_list=[]
best_list=[]

for i in range(0,len(main_list)):
    temp_list=[]
    for j in range(0,len(main_list[i])):
        if j==0:
            question_list.append(main_list[i][j])
            continue
        else:
            temp_list.append(main_list[i][j])
    answers_list.append(temp_list)

name_file=open('name-list.txt','w', encoding='utf-8')
for i in range(0,len(answers_list)):
    for j in range(0,len(answers_list[i])):
        name_file.writelines(answers_list[i][j][0])
        name_file.write('\n')
name_file.close()  

file1=open('name-list.txt','r',encoding='utf-8')
file_txt = file1.read().split('\n')
file1.close()
score1={}
file_txt1 = file_txt.copy()
for i, j in enumerate(file_txt):
    if j not in score1.keys():
        score1[j]=file_txt1.count(j)
    file_txt1[:] = [x for x in file_txt1 if x!=j]

def main(answers_list):
    temp_best_list=['']
    temp=0
    for j in range(0,len(answers_list)):
        best_user=''
        temp_ans=[x.lower() for x in answers_list[j][-1].split()]

        value=score(answers_list[j][-1],answers_list[j][0], score1)
        if value>temp and value>-9*name_rank(answers_list[j][0],score1):
            temp=value
            if 'thnak' in temp_ans or 'thank' in temp_ans or 'thankyou' in temp_ans  or 'thanks' in temp_ans:
                for k in temp_ans:
                    if k.find('@')!=-1:
                        best_user=answers_list[j][0].lower()
     
                for l in answers_list[j]:
                    if '.' in best_user or '!' in best_user:
                        best_user=best_user[:-1]
                    if best_user in l[0].lower():
                        temp_best_list=l[-1]
            
        temp=0
        if value>temp and value>-9*name_rank(answers_list[j][0],score1):
            temp=value
            temp_best_list=answers_list[j][-1]
        
    return temp_best_list
            
best_ans=[]
for i in range(len(question_list)):
    best_ans=main(answers_list[i])
    best_list.append(best_ans)
# for i in range(0,len(answers_list)):
#     for j in range(0,len(answers_list[i])):

print(len(best_list) - best_list.count(['']))

# file=open('optimized.txt','w',encoding='utf-8')
# for i in range(0,len(question_list)):
#     file.writelines(best_list[i])
#     file.write('\n')
# file.close()