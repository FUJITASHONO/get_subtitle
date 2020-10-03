class Text_process
    def remove_bracket(text):
        check = True                                            # whileループの終了条件に使用
        word_s = '<'                                            # タグの先頭<を検索する時に使用
        word_e = '>'                                            # タグの末尾>を検索する時に使用
     
        # 「<>」のセットが無くなるまでループ
        while check == True:
            start = text.find(word_s)                           # <が何番目の指標かを検索
            # もしword_sが無い場合はcheckをFにしてwhileを終了
            if start == -1:
                check = False
            # word_sが存在する場合
            else:
                end = text.find(word_e)                         # >が何番目の指標かを検索
                # もしword_eが無い場合はcheckをFにしてwhileを終了
                if end == -1:
                    check = False
                # word_sとword_eの両方がセットである場合は<と>で囲まれた範囲を空白に置換（削除）する。
                else:
                    remove_word = text[start:end + 1]           # 削除するワード（<と>で囲まれた所）をスライス
                    text = text.replace(remove_word, '')        # remove_wordを空白に置換
        return text

    def clean_word(word):
        word = word.replace('\u200c','')
        word = word.replace('-','')
        word = word.replace('\\ N ','')
        word = word.replace('\n','')
        word = word.replace('!', '')
        word = word.replace('?','')
        word = word.replace('♪', '')
        word = word.replace('？', '')
        word = word.replace('!', '')
        word = word.replace('"', '')
        word = word.replace('…', '')
        return word