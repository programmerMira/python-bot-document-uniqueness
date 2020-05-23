#логика проверки уникальности файла

def canonize(source):
    stop_symbols = '.,!?:;-\n\r()'
     
    stop_words = (u'это', u'как', u'так',
    u'и', u'в', u'над',
    u'к', u'до', u'не',
    u'на', u'но', u'за',
    u'то', u'с', u'ли',
    u'а', u'во', u'от',
    u'со', u'для', u'о',
    u'же', u'ну', u'вы',
    u'бы', u'что', u'кто',
    u'он', u'она')
    result = ( [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)] )
    print(result)
    return result

def genshingle(source):
    import binascii
    shingleLen = 10 #длина шингла
    out = []
    for i in range(len(source)-(shingleLen-1)):
        out.append (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))
    print(out)
    return out

def compaire (source1,source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
     
    return same*2/float(len(source1) + len(source2))*100

def check_files(initial_file, compared_file):
    import docx2txt
    text1 = docx2txt.process(initial_file)
    text2=docx2txt.process(compared_file[0])
    res1=genshingle(canonize(text1))
    res2=genshingle(canonize(text2))
    
    return compaire(res1,res2)