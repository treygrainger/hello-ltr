try:
    from judgments import Judgment, judgments_from_file, judgments_to_file, judgments_by_qid
    from butterfingers import butterfingers
except ImportError:
    from .judgments import Judgment, judgments_from_file, judgments_to_file, judgments_by_qid
    from .butterfingers import butterfingers



def typoIt(judgmentInFile, judgmentOutFile, rounds=100):
    currJudgments = [judg for judg in judgments_from_file(judgmentInFile)]
    lastQid = currJudgments[-1].qid
    judgDict = judgments_by_qid(currJudgments)

    existingTypos = set()

    for i in range(0, rounds):

        for qid, judglist in judgDict.items():
            keywords = judglist[0].keywords
            keywordsWTypo = butterfingers(keywords)

            if keywordsWTypo != keywords and keywordsWTypo not in existingTypos:
                newQid = lastQid+1
                print("%s => %s" % (keywords, keywordsWTypo))
                lastQid += 1
                for judg in judglist:
                    typoJudg = Judgment(grade=judg.grade,
                                        qid=newQid,
                                        keywords=keywordsWTypo,
                                        docId=judg.docId)
                    currJudgments.append(typoJudg)
                existingTypos.add(keywordsWTypo)

    judgments_to_file(filename=judgmentOutFile, judgmentsList=currJudgments)


if __name__ == "__main__":
    typoIt(judgmentInFile='title_judgments.txt', judgmentOutFile='title_fuzzy_judgments.txt')


    # Clone a judgment, inject random typos
